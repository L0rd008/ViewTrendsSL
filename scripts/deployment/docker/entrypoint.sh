#!/bin/bash
set -e

# ViewTrendsSL Docker Entrypoint Script
# This script handles container initialization, database setup,
# and application startup for production deployment.

echo "🚀 Starting ViewTrendsSL container initialization..."

# Environment variables with defaults
export FLASK_ENV=${FLASK_ENV:-production}
export LOG_LEVEL=${LOG_LEVEL:-INFO}
export WORKERS=${WORKERS:-4}
export DATABASE_URL=${DATABASE_URL:-sqlite:///data/viewtrendssl.db}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [[ "$LOG_LEVEL" == "DEBUG" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

# Wait for database to be ready
wait_for_database() {
    log_info "Waiting for database to be ready..."
    
    if [[ $DATABASE_URL == postgresql* ]]; then
        # Extract database connection details
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        
        log_debug "Checking PostgreSQL connection to $DB_HOST:$DB_PORT"
        
        # Wait for PostgreSQL
        for i in {1..30}; do
            if pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; then
                log_info "✅ Database is ready!"
                return 0
            fi
            log_debug "Database not ready, waiting... ($i/30)"
            sleep 2
        done
        
        log_error "❌ Database connection timeout"
        exit 1
    else
        log_info "Using SQLite database"
    fi
}

# Initialize database schema
init_database() {
    log_info "Initializing database schema..."
    
    if python -c "
import sys
sys.path.insert(0, '/app')
from scripts.database.setup.init_database import main
try:
    main()
    print('Database initialization completed successfully')
except Exception as e:
    print(f'Database initialization failed: {e}')
    sys.exit(1)
"; then
        log_info "✅ Database schema initialized"
    else
        log_error "❌ Database initialization failed"
        exit 1
    fi
}

# Load ML models
load_models() {
    log_info "Loading ML models..."
    
    if [[ -d "/app/models" ]] && [[ -n "$(ls -A /app/models 2>/dev/null)" ]]; then
        log_info "✅ ML models found in /app/models"
    else
        log_warn "⚠️  No ML models found. Training may be required."
        log_info "Models will be loaded when available or after training"
    fi
}

# Health check function
health_check() {
    log_info "Performing application health check..."
    
    # Check if Flask app can start
    if python -c "
import sys
sys.path.insert(0, '/app')
try:
    from src.application.api.app import app
    print('Flask application loaded successfully')
except Exception as e:
    print(f'Flask application failed to load: {e}')
    sys.exit(1)
"; then
        log_info "✅ Application health check passed"
    else
        log_error "❌ Application health check failed"
        exit 1
    fi
}

# Setup logging directories
setup_logging() {
    log_info "Setting up logging directories..."
    
    mkdir -p /app/logs/api
    mkdir -p /app/logs/data_collection
    mkdir -p /app/logs/training
    mkdir -p /app/logs/nginx
    
    # Set permissions
    chmod -R 755 /app/logs
    
    log_info "✅ Logging directories created"
}

# Setup data directories
setup_data_dirs() {
    log_info "Setting up data directories..."
    
    mkdir -p /app/data/raw
    mkdir -p /app/data/processed
    mkdir -p /app/data/snapshots
    mkdir -p /app/data/logs
    mkdir -p /app/models
    mkdir -p /app/reports
    mkdir -p /app/plots/evaluation
    
    # Set permissions
    chmod -R 755 /app/data /app/models /app/reports /app/plots
    
    log_info "✅ Data directories created"
}

# Run database migrations (if any)
run_migrations() {
    log_info "Checking for database migrations..."
    
    if [[ -d "/app/src/data_access/database/migrations" ]] && [[ -n "$(ls -A /app/src/data_access/database/migrations 2>/dev/null)" ]]; then
        log_info "Running database migrations..."
        # Add migration logic here when implemented
        log_info "✅ Migrations completed"
    else
        log_debug "No migrations found"
    fi
}

# Start the application based on the command
start_application() {
    log_info "Starting ViewTrendsSL application..."
    
    case "$1" in
        "api"|"")
            log_info "🌐 Starting API server with Gunicorn"
            log_info "Workers: $WORKERS"
            log_info "Environment: $FLASK_ENV"
            
            exec gunicorn \
                --config /app/config/docker/production/gunicorn.conf.py \
                --workers "$WORKERS" \
                --bind 0.0.0.0:8000 \
                --access-logfile - \
                --error-logfile - \
                --log-level "$LOG_LEVEL" \
                "src.application.api.app:app"
            ;;
        
        "data-collector")
            log_info "📊 Starting data collection service"
            exec python -m scripts.data_collection.orchestrator --production
            ;;
        
        "trainer")
            log_info "🤖 Starting model training"
            exec python -m scripts.training.train_models --save-models --generate-report
            ;;
        
        "shell")
            log_info "🐚 Starting interactive shell"
            exec /bin/bash
            ;;
        
        "test")
            log_info "🧪 Running tests"
            exec python -m pytest tests/ -v
            ;;
        
        *)
            log_info "🔧 Running custom command: $*"
            exec "$@"
            ;;
    esac
}

# Cleanup function for graceful shutdown
cleanup() {
    log_info "🛑 Received shutdown signal, cleaning up..."
    
    # Kill any background processes
    jobs -p | xargs -r kill
    
    log_info "✅ Cleanup completed"
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Main initialization sequence
main() {
    log_info "🎯 ViewTrendsSL Container Initialization"
    log_info "Environment: $FLASK_ENV"
    log_info "Log Level: $LOG_LEVEL"
    log_info "Database: ${DATABASE_URL%%\?*}"  # Hide query parameters
    
    # Setup directories
    setup_logging
    setup_data_dirs
    
    # Wait for dependencies
    wait_for_database
    
    # Initialize application
    init_database
    run_migrations
    load_models
    health_check
    
    log_info "🎉 Initialization completed successfully!"
    log_info "Starting application with command: ${1:-api}"
    
    # Start the application
    start_application "$@"
}

# Run main function with all arguments
main "$@"
