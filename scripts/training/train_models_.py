#ViewTrendsSL\scripts\training\train_models_.py
"""
ViewTrendsSL Model Training Script

This script orchestrates the complete model training pipeline including
data loading, feature engineering, model training, and evaluation.

Usage:
    python scripts/training/train_models.py [options]

Author: ViewTrendsSL Team
Date: 2025
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.business.ml.training.trainer import ModelTrainer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Train ViewTrendsSL ML models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Train all models with default settings
    python scripts/training/train_models.py

    # Train only shorts model for 3-day prediction
    python scripts/training/train_models.py --model-type shorts --target-days 3

    # Train with custom database and save models
    python scripts/training/train_models.py --database-path data/custom.db --save-models

    # Evaluate existing models
    python scripts/training/train_models.py --evaluate-only --models-dir models/
        """
    )
    
    parser.add_argument(
        '--model-type',
        choices=['all', 'shorts', 'longform'],
        default='all',
        help='Type of model to train (default: all)'
    )
    
    parser.add_argument(
        '--target-days',
        type=int,
        default=7,
        help='Target prediction timeframe in days (default: 7)'
    )
    
    parser.add_argument(
        '--database-path',
        type=str,
        default='data/viewtrendssl.db',
        help='Path to the database file (default: data/viewtrendssl.db)'
    )
    
    parser.add_argument(
        '--models-dir',
        type=str,
        default='models',
        help='Directory to save/load models (default: models)'
    )
    
    parser.add_argument(
        '--config-file',
        type=str,
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--save-models',
        action='store_true',
        default=True,
        help='Save trained models to disk (default: True)'
    )
    
    parser.add_argument(
        '--save-data',
        action='store_true',
        default=True,
        help='Save processed training data (default: True)'
    )
    
    parser.add_argument(
        '--evaluate-only',
        action='store_true',
        help='Only evaluate existing models without training'
    )
    
    parser.add_argument(
        '--generate-report',
        action='store_true',
        default=True,
        help='Generate evaluation report (default: True)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def load_config(config_file: str = None) -> dict:
    """Load configuration from file or use defaults."""
    
    default_config = {
        'database_path': 'data/viewtrendssl.db',
        'models_dir': 'models',
        'data': {
            'min_age_days': 30,
            'max_age_days': 365,
            'min_views_threshold': 10
        },
        'training': {
            'time_based_split': True,
            'test_size': 0.2,
            'val_size': 0.2,
            'random_state': 42
        },
        'feature_config': {
            'max_duration_shorts': 60,
            'min_duration_longform': 61
        },
        'model_config': {
            'shorts': {
                'algorithm': 'xgboost',
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42
            },
            'longform': {
                'algorithm': 'xgboost',
                'n_estimators': 150,
                'max_depth': 8,
                'learning_rate': 0.1,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'random_state': 42
            }
        }
    }
    
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, 'r') as f:
                custom_config = json.load(f)
            
            # Merge configurations
            def merge_dicts(default, custom):
                for key, value in custom.items():
                    if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                        merge_dicts(default[key], value)
                    else:
                        default[key] = value
            
            merge_dicts(default_config, custom_config)
            logger.info(f"Loaded configuration from {config_file}")
            
        except Exception as e:
            logger.warning(f"Failed to load config file {config_file}: {e}")
            logger.info("Using default configuration")
    
    return default_config


def setup_directories():
    """Create necessary directories."""
    directories = [
        'models',
        'data/processed',
        'logs',
        'results',
        'reports',
        'plots/evaluation'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory: {directory}")


def train_models(args, config):
    """Train the ML models."""
    
    logger.info("=" * 60)
    logger.info("VIEWTRENDSSL MODEL TRAINING PIPELINE")
    logger.info("=" * 60)
    
    # Update config with command line arguments
    config['database_path'] = args.database_path
    config['models_dir'] = args.models_dir
    
    # Initialize trainer
    trainer = ModelTrainer(config)
    
    try:
        if args.model_type == 'all':
            logger.info("Training all models (Shorts and Long-form)")
            results = trainer.train_all_models(
                target_timeframe=args.target_days,
                save_models=args.save_models,
                save_data=args.save_data
            )
        else:
            logger.info(f"Training {args.model_type} model only")
            results = trainer.train_single_model(
                model_type=args.model_type,
                target_timeframe=args.target_days,
                save_model=args.save_models
            )
        
        # Print summary
        print_training_summary(results)
        
        return results, trainer
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise


def evaluate_models(args, config):
    """Evaluate existing models."""
    
    logger.info("=" * 60)
    logger.info("VIEWTRENDSSL MODEL EVALUATION")
    logger.info("=" * 60)
    
    # Update config with command line arguments
    config['database_path'] = args.database_path
    config['models_dir'] = args.models_dir
    
    # Initialize trainer and load models
    trainer = ModelTrainer(config)
    
    if not trainer.load_models(args.models_dir):
        logger.error("Failed to load models for evaluation")
        return None, trainer
    
    try:
        results = trainer.evaluate_models()
        
        # Print evaluation summary
        print_evaluation_summary(results)
        
        return results, trainer
        
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}")
        raise


def print_training_summary(results):
    """Print training results summary."""
    
    print("\n" + "=" * 60)
    print("TRAINING RESULTS SUMMARY")
    print("=" * 60)
    
    if results.get('success', False):
        print("✅ Training completed successfully!")
        
        # Data summary
        if 'data_summary' in results:
            data = results['data_summary']
            print(f"\n📊 Dataset Summary:")
            print(f"   Total samples: {data.get('total_samples', 'N/A'):,}")
            print(f"   Shorts samples: {data.get('shorts_samples', 'N/A'):,}")
            print(f"   Long-form samples: {data.get('longform_samples', 'N/A'):,}")
            print(f"   Features: {data.get('features', 'N/A')}")
        
        # Model performance
        if 'models' in results:
            print(f"\n🎯 Model Performance:")
            
            for model_type, model_results in results['models'].items():
                if 'test_evaluation' in model_results:
                    metrics = model_results['test_evaluation'].get('basic_metrics', {})
                    print(f"   {model_type.title()} Model:")
                    print(f"     R² Score: {metrics.get('r2_score', 'N/A'):.4f}")
                    print(f"     MAPE: {metrics.get('mape', 'N/A'):.2f}%")
                    print(f"     MAE: {metrics.get('mae', 'N/A'):.2f}")
        
        # Feature importance
        if 'feature_importance' in results:
            print(f"\n🔍 Feature Analysis:")
            shorts_features = results['feature_importance'].get('shorts_importance', {})
            longform_features = results['feature_importance'].get('longform_importance', {})
            
            if shorts_features:
                top_shorts = sorted(shorts_features.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   Top Shorts features: {', '.join([f[0] for f in top_shorts])}")
            
            if longform_features:
                top_longform = sorted(longform_features.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   Top Long-form features: {', '.join([f[0] for f in top_longform])}")
        
        print(f"\n⏱️  Training time: {results.get('started_at', '')} to {results.get('completed_at', '')}")
        
    else:
        print("❌ Training failed!")
        if 'error' in results:
            print(f"   Error: {results['error']}")


def print_evaluation_summary(results):
    """Print evaluation results summary."""
    
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS SUMMARY")
    print("=" * 60)
    
    for model_type, model_results in results.items():
        if isinstance(model_results, dict) and 'basic_metrics' in model_results:
            metrics = model_results['basic_metrics']
            print(f"\n🎯 {model_type.title()} Model Performance:")
            print(f"   R² Score: {metrics.get('r2_score', 'N/A'):.4f}")
            print(f"   MAPE: {metrics.get('mape', 'N/A'):.2f}%")
            print(f"   MAE: {metrics.get('mae', 'N/A'):.2f}")
            print(f"   RMSE: {metrics.get('rmse', 'N/A'):.2f}")
            print(f"   Samples: {model_results.get('sample_count', 'N/A'):,}")


def generate_report(results, trainer, args):
    """Generate comprehensive evaluation report."""
    
    if not args.generate_report:
        return
    
    logger.info("Generating evaluation report...")
    
    try:
        # Create report data
        report_data = {
            'training_results': results,
            'model_info': trainer.get_model_info(),
            'configuration': {
                'target_days': args.target_days,
                'model_type': args.model_type,
                'database_path': args.database_path
            },
            'generated_at': datetime.now().isoformat()
        }
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        results_file = f"results/training_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Detailed results saved to {results_file}")
        
        # Generate HTML report if evaluator is available
        try:
            from src.business.ml.evaluation.evaluator import ModelEvaluator
            evaluator = ModelEvaluator()
            
            html_report_path = f"reports/evaluation_report_{timestamp}.html"
            if evaluator.generate_evaluation_report(report_data, html_report_path):
                logger.info(f"HTML report generated: {html_report_path}")
        except Exception as e:
            logger.warning(f"Could not generate HTML report: {e}")
        
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")


def main():
    """Main function."""
    
    # Parse arguments
    args = parse_arguments()
    
    # Set up logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load configuration
    config = load_config(args.config_file)
    
    # Setup directories
    setup_directories()
    
    # Check if database exists
    if not Path(args.database_path).exists():
        logger.error(f"Database not found: {args.database_path}")
        logger.info("Please run data collection scripts first to create the database")
        sys.exit(1)
    
    try:
        if args.evaluate_only:
            # Evaluation only
            results, trainer = evaluate_models(args, config)
        else:
            # Training (and evaluation)
            results, trainer = train_models(args, config)
        
        # Generate report
        if results:
            generate_report(results, trainer, args)
        
        logger.info("Pipeline completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
