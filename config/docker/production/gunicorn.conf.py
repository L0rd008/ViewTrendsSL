"""
Gunicorn Configuration for ViewTrendsSL Production

This configuration file optimizes Gunicorn for production deployment
of the ViewTrendsSL API with proper worker management, logging, and
performance settings.

Author: ViewTrendsSL Team
Date: 2025
"""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Worker timeout
graceful_timeout = 30
timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'viewtrendssl_api'

# Server mechanics
daemon = False
pidfile = '/tmp/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = None
certfile = None

# Application
wsgi_module = "src.application.api.app:app"

# Preload application for better performance
preload_app = True

# Worker process management
worker_tmp_dir = "/dev/shm"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance tuning
worker_rlimit_nofile = 1024
worker_rlimit_core = 0

# Environment variables
raw_env = [
    'FLASK_ENV=production',
    'PYTHONPATH=/app',
]

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("ViewTrendsSL API server is ready. Listening on: %s", server.address)

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT signal")
