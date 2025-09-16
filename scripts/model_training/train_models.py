#ViewTrendsSL\scripts\model_training\train_models.py
"""
Model Training Script for ViewTrendsSL

This script handles the training of machine learning models for YouTube viewership prediction.
It supports both Shorts and Long-form video models with comprehensive evaluation.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import logging
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from src.business.ml.training.data_loader import DataLoader
from src.business.ml.preprocessing.feature_pipeline import FeaturePipeline
from src.business.ml.training.trainer import ModelTrainer
from src.business.ml.evaluation.evaluator import ModelEvaluator
from src.business.ml.models.shorts_model import ShortsModel
from src.business.ml.models.longform_model import LongFormModel
from src.business.utils.time_utils import get_current_utc_time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ModelTrainingPipeline:
    """Complete pipeline for training ViewTrendsSL models."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the training pipeline.
        
        Args:
            config: Training configuration dictionary
        """
        self.config = config
        self.data_loader = DataLoader()
        self.feature_pipeline = FeaturePipeline()
        self.trainer = ModelTrainer()
        self.evaluator = ModelEvaluator()
        
        # Create output directories
        self.output_dir = Path(config.get('output_dir', 'models/trained'))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_dir = Path(config.get('metrics_dir', 'models/metrics'))
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Training pipeline initialized with output dir: {self.output_dir}")
    
    def load_and_prepare_data(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Load and prepare training data.
        
        Returns:
            Tuple of (shorts_data, longform_data) dictionaries
        """
        logger.info("Loading and preparing training data...")
        
        # Load raw data
        data_path = self.config.get('data_path', 'data/processed/training_data.csv')
        raw_data = self.data_loader.load_training_data(data_path)
        
        if raw_data is None or raw_data.empty:
            raise ValueError(f"No data found at {data_path}")
        
        logger.info(f"Loaded {len(raw_data)} records")
        
        # Separate shorts and long-form videos
        shorts_data = raw_data[raw_data['is_short'] == True].copy()
        longform_data = raw_data[raw_data['is_short'] == False].copy()
        
        logger.info(f"Shorts videos: {len(shorts_data)}")
        logger.info(f"Long-form videos: {len(longform_data)}")
        
        if len(shorts_data) < 100:
            logger.warning(f"Limited shorts data: {len(shorts_data)} samples")
        
        if len(longform_data) < 100:
            logger.warning(f"Limited long-form data: {len(longform_data)} samples")
        
        # Process features for each dataset
        shorts_processed = None
        longform_processed = None
        
        if len(shorts_data) >= 50:  # Minimum threshold
            logger.info("Processing Shorts features...")
            shorts_processed = self.feature_pipeline.process_features(
                shorts_data, 
                video_type='shorts'
            )
        
        if len(longform_data) >= 50:  # Minimum threshold
            logger.info("Processing Long-form features...")
            longform_processed = self.feature_pipeline.process_features(
                longform_data, 
                video_type='longform'
            )
        
        return shorts_processed, longform_processed
    
    def train_shorts_model(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Train the Shorts prediction model.
        
        Args:
            data: Processed shorts data
            
        Returns:
            Training results dictionary or None if training failed
        """
        if data is None:
            logger.warning("No Shorts data available for training")
            return None
        
        logger.info("Training Shorts model...")
        
        try:
            # Initialize model
            shorts_model = ShortsModel()
            
            # Train model
            training_results = self.trainer.train_model(
                model=shorts_model,
                X_train=data['X_train'],
                y_train=data['y_train'],
                X_val=data['X_val'],
                y_val=data['y_val'],
                model_type='shorts'
            )
            
            # Evaluate model
            evaluation_results = self.evaluator.evaluate_model(
                model=shorts_model,
                X_test=data['X_test'],
                y_test=data['y_test'],
                model_type='shorts'
            )
            
            # Save model
            model_path = self.output_dir / 'shorts_model.joblib'
            shorts_model.save_model(str(model_path))
            
            # Combine results
            results = {
                'model_type': 'shorts',
                'training_results': training_results,
                'evaluation_results': evaluation_results,
                'model_path': str(model_path),
                'training_samples': len(data['X_train']),
                'validation_samples': len(data['X_val']),
                'test_samples': len(data['X_test']),
                'features_used': data.get('feature_names', []),
                'trained_at': get_current_utc_time().isoformat()
            }
            
            # Save metrics
            metrics_path = self.metrics_dir / 'shorts_metrics.json'
            with open(metrics_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Shorts model training completed. MAPE: {evaluation_results.get('mape', 'N/A'):.2f}%")
            return results
            
        except Exception as e:
            logger.error(f"Error training Shorts model: {e}")
            return None
    
    def train_longform_model(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Train the Long-form prediction model.
        
        Args:
            data: Processed long-form data
            
        Returns:
            Training results dictionary or None if training failed
        """
        if data is None:
            logger.warning("No Long-form data available for training")
            return None
        
        logger.info("Training Long-form model...")
        
        try:
            # Initialize model
            longform_model = LongFormModel()
            
            # Train model
            training_results = self.trainer.train_model(
                model=longform_model,
                X_train=data['X_train'],
                y_train=data['y_train'],
                X_val=data['X_val'],
                y_val=data['y_val'],
                model_type='longform'
            )
            
            # Evaluate model
            evaluation_results = self.evaluator.evaluate_model(
                model=longform_model,
                X_test=data['X_test'],
                y_test=data['y_test'],
                model_type='longform'
            )
            
            # Save model
            model_path = self.output_dir / 'longform_model.joblib'
            longform_model.save_model(str(model_path))
            
            # Combine results
            results = {
                'model_type': 'longform',
                'training_results': training_results,
                'evaluation_results': evaluation_results,
                'model_path': str(model_path),
                'training_samples': len(data['X_train']),
                'validation_samples': len(data['X_val']),
                'test_samples': len(data['X_test']),
                'features_used': data.get('feature_names', []),
                'trained_at': get_current_utc_time().isoformat()
            }
            
            # Save metrics
            metrics_path = self.metrics_dir / 'longform_metrics.json'
            with open(metrics_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Long-form model training completed. MAPE: {evaluation_results.get('mape', 'N/A'):.2f}%")
            return results
            
        except Exception as e:
            logger.error(f"Error training Long-form model: {e}")
            return None
    
    def run_complete_training(self) -> Dict[str, Any]:
        """
        Run the complete training pipeline.
        
        Returns:
            Dictionary with training results for both models
        """
        logger.info("Starting complete model training pipeline...")
        start_time = datetime.now()
        
        try:
            # Load and prepare data
            shorts_data, longform_data = self.load_and_prepare_data()
            
            # Train models
            shorts_results = self.train_shorts_model(shorts_data)
            longform_results = self.train_longform_model(longform_data)
            
            # Compile final results
            end_time = datetime.now()
            training_duration = (end_time - start_time).total_seconds()
            
            final_results = {
                'pipeline_status': 'completed',
                'training_duration_seconds': training_duration,
                'started_at': start_time.isoformat(),
                'completed_at': end_time.isoformat(),
                'shorts_model': shorts_results,
                'longform_model': longform_results,
                'config_used': self.config
            }
            
            # Save final results
            final_results_path = self.metrics_dir / 'training_summary.json'
            with open(final_results_path, 'w') as f:
                json.dump(final_results, f, indent=2, default=str)
            
            # Log summary
            self._log_training_summary(final_results)
            
            return final_results
            
        except Exception as e:
            logger.error(f"Training pipeline failed: {e}")
            raise
    
    def _log_training_summary(self, results: Dict[str, Any]):
        """Log a summary of training results."""
        logger.info("=" * 60)
        logger.info("TRAINING PIPELINE SUMMARY")
        logger.info("=" * 60)
        
        logger.info(f"Duration: {results['training_duration_seconds']:.1f} seconds")
        
        if results['shorts_model']:
            shorts_mape = results['shorts_model']['evaluation_results'].get('mape', 'N/A')
            shorts_samples = results['shorts_model']['training_samples']
            logger.info(f"Shorts Model - MAPE: {shorts_mape:.2f}%, Samples: {shorts_samples}")
        else:
            logger.info("Shorts Model - Not trained (insufficient data)")
        
        if results['longform_model']:
            longform_mape = results['longform_model']['evaluation_results'].get('mape', 'N/A')
            longform_samples = results['longform_model']['training_samples']
            logger.info(f"Long-form Model - MAPE: {longform_mape:.2f}%, Samples: {longform_samples}")
        else:
            logger.info("Long-form Model - Not trained (insufficient data)")
        
        logger.info(f"Models saved to: {self.output_dir}")
        logger.info(f"Metrics saved to: {self.metrics_dir}")
        logger.info("=" * 60)


def load_training_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load training configuration from file or use defaults.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    default_config = {
        'data_path': 'data/processed/training_data.csv',
        'output_dir': 'models/trained',
        'metrics_dir': 'models/metrics',
        'test_size': 0.2,
        'validation_size': 0.2,
        'random_state': 42,
        'target_columns': ['views_at_24h', 'views_at_7d', 'views_at_30d'],
        'model_params': {
            'shorts': {
                'n_estimators': 100,
                'max_depth': 10,
                'learning_rate': 0.1
            },
            'longform': {
                'n_estimators': 150,
                'max_depth': 12,
                'learning_rate': 0.1
            }
        }
    }
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
            
            # Merge with defaults
            default_config.update(file_config)
            logger.info(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            logger.warning(f"Error loading config file {config_path}: {e}")
            logger.info("Using default configuration")
    
    return default_config


def main():
    """Main training script entry point."""
    parser = argparse.ArgumentParser(description='Train ViewTrendsSL prediction models')
    
    parser.add_argument(
        '--config', 
        type=str, 
        help='Path to training configuration file'
    )
    
    parser.add_argument(
        '--data-path', 
        type=str, 
        help='Path to training data CSV file'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        help='Directory to save trained models'
    )
    
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Validate data and configuration without training'
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_training_config(args.config)
        
        # Override with command line arguments
        if args.data_path:
            config['data_path'] = args.data_path
        
        if args.output_dir:
            config['output_dir'] = args.output_dir
        
        # Validate data path exists
        if not os.path.exists(config['data_path']):
            logger.error(f"Training data not found: {config['data_path']}")
            logger.info("Please run data collection and preprocessing first")
            return 1
        
        # Initialize pipeline
        pipeline = ModelTrainingPipeline(config)
        
        if args.dry_run:
            logger.info("Dry run mode - validating data and configuration...")
            shorts_data, longform_data = pipeline.load_and_prepare_data()
            
            logger.info("Data validation completed successfully")
            if shorts_data:
                logger.info(f"Shorts data ready: {len(shorts_data['X_train'])} training samples")
            if longform_data:
                logger.info(f"Long-form data ready: {len(longform_data['X_train'])} training samples")
            
            return 0
        
        # Run training
        results = pipeline.run_complete_training()
        
        # Check if any models were trained successfully
        success = False
        if results['shorts_model'] and results['shorts_model']['evaluation_results'].get('mape', float('inf')) < 50:
            success = True
        if results['longform_model'] and results['longform_model']['evaluation_results'].get('mape', float('inf')) < 50:
            success = True
        
        if success:
            logger.info("Training completed successfully!")
            return 0
        else:
            logger.warning("Training completed but model performance may be poor")
            return 1
            
    except Exception as e:
        logger.error(f"Training failed: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
