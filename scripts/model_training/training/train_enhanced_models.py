#!/usr/bin/env python3
"""
Enhanced Model Training Script for ViewTrendsSL

This script trains machine learning models using the processed CSV data
with comprehensive feature engineering and time-series information.

Author: ViewTrendsSL Team
Date: 2025
"""

import sys
import os
import argparse
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
import json
import joblib
import warnings
warnings.filterwarnings('ignore')

# ML libraries
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedModelTrainer:
    """Enhanced trainer for ViewTrendsSL models using processed CSV data."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the enhanced model trainer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Create output directories
        self.models_dir = Path(config.get('models_dir', 'models'))
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.results_dir = Path(config.get('results_dir', 'results'))
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize models
        self.models = {}
        self.preprocessors = {}
        self.feature_info = {}
        
        logger.info(f"Enhanced model trainer initialized")
        logger.info(f"Models directory: {self.models_dir}")
        logger.info(f"Results directory: {self.results_dir}")
    
    def load_processed_data(self, data_path: str) -> pd.DataFrame:
        """
        Load processed training data.
        
        Args:
            data_path: Path to processed training data
            
        Returns:
            Loaded DataFrame
        """
        logger.info(f"Loading processed data from {data_path}")
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Processed data not found: {data_path}")
        
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} records with {len(df.columns)} features")
        
        return df
    
    def load_feature_info(self, feature_info_path: str) -> Dict[str, Any]:
        """
        Load feature information from JSON file.
        
        Args:
            feature_info_path: Path to feature info JSON
            
        Returns:
            Feature information dictionary
        """
        if os.path.exists(feature_info_path):
            with open(feature_info_path, 'r') as f:
                feature_info = json.load(f)
            logger.info(f"Loaded feature information: {len(feature_info.get('feature_names', []))} features")
            return feature_info
        else:
            logger.warning(f"Feature info file not found: {feature_info_path}")
            return {}
    
    def prepare_features_and_targets(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, pd.Series]]:
        """
        Prepare features and target variables for training.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Tuple of (features_df, targets_dict)
        """
        logger.info("Preparing features and targets...")
        
        # Define target variables
        target_columns = ['views_at_24h', 'views_at_7d', 'views_at_30d']
        
        # Check which targets are available
        available_targets = [col for col in target_columns if col in df.columns]
        if not available_targets:
            raise ValueError(f"No target variables found. Expected: {target_columns}")
        
        logger.info(f"Available targets: {available_targets}")
        
        # Prepare targets
        targets = {}
        for target in available_targets:
            targets[target] = df[target].copy()
            # Handle NaN values - fill with 0 or drop rows
            targets[target] = targets[target].fillna(0)
            # Ensure targets are positive and finite
            targets[target] = targets[target].clip(lower=0)
            # Remove infinite values
            targets[target] = targets[target].replace([np.inf, -np.inf], 0)
        
        # Prepare features (exclude target columns and non-feature columns)
        exclude_columns = target_columns + [
            'video_id', 'channel_id', 'title', 'description', 'tags',
            'published_at', 'inserted_at', 'localized_title', 'localized_description',
            'thumbnail_default', 'thumbnail_medium', 'thumbnail_high',
            'default_language', 'default_audio_language', 'live_broadcast_content'
        ]
        
        # Also exclude raw time-series columns (day_X_views, day_X_likes, etc.)
        time_series_raw_cols = [col for col in df.columns if 
                               col.startswith('day_') and 
                               (col.endswith('_views') or col.endswith('_likes') or col.endswith('_comments'))]
        exclude_columns.extend(time_series_raw_cols)
        
        feature_columns = [col for col in df.columns if col not in exclude_columns]
        features_df = df[feature_columns].copy()
        
        logger.info(f"Prepared {len(feature_columns)} features and {len(available_targets)} targets")
        logger.info(f"Feature columns: {feature_columns[:10]}..." if len(feature_columns) > 10 else f"Feature columns: {feature_columns}")
        
        return features_df, targets
    
    def create_preprocessor(self, features_df: pd.DataFrame, feature_info: Dict[str, Any]) -> ColumnTransformer:
        """
        Create preprocessing pipeline for features.
        
        Args:
            features_df: Features DataFrame
            feature_info: Feature information dictionary
            
        Returns:
            ColumnTransformer for preprocessing
        """
        logger.info("Creating preprocessing pipeline...")
        
        # Identify feature types
        numerical_features = []
        categorical_features = []
        
        for col in features_df.columns:
            if features_df[col].dtype in ['int64', 'float64']:
                # Check if it's actually categorical (boolean or small number of unique values)
                if features_df[col].dtype == 'bool' or len(features_df[col].unique()) <= 10:
                    categorical_features.append(col)
                else:
                    numerical_features.append(col)
            else:
                categorical_features.append(col)
        
        # Use feature info if available
        if feature_info:
            if 'numerical_features' in feature_info:
                numerical_features = [col for col in feature_info['numerical_features'] if col in features_df.columns]
            if 'categorical_features' in feature_info:
                categorical_features = [col for col in feature_info['categorical_features'] if col in features_df.columns]
        
        logger.info(f"Numerical features: {len(numerical_features)}")
        logger.info(f"Categorical features: {len(categorical_features)}")
        
        # Create preprocessing steps
        preprocessor_steps = []
        
        if numerical_features:
            preprocessor_steps.append(
                ('num', StandardScaler(), numerical_features)
            )
        
        if categorical_features:
            preprocessor_steps.append(
                ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_features)
            )
        
        if not preprocessor_steps:
            raise ValueError("No features to preprocess")
        
        preprocessor = ColumnTransformer(
            transformers=preprocessor_steps,
            remainder='drop'
        )
        
        return preprocessor
    
    def train_model_for_target(
        self, 
        X: pd.DataFrame, 
        y: pd.Series, 
        target_name: str,
        model_type: str = 'xgboost'
    ) -> Tuple[Pipeline, Dict[str, Any]]:
        """
        Train a model for a specific target variable.
        
        Args:
            X: Features DataFrame
            y: Target Series
            target_name: Name of target variable
            model_type: Type of model to train
            
        Returns:
            Tuple of (trained_pipeline, metrics_dict)
        """
        logger.info(f"Training {model_type} model for {target_name}...")
        
        # Create preprocessor
        preprocessor = self.create_preprocessor(X, self.feature_info)
        
        # Select model
        if model_type == 'xgboost':
            model = xgb.XGBRegressor(
                n_estimators=self.config.get('n_estimators', 100),
                max_depth=self.config.get('max_depth', 6),
                learning_rate=self.config.get('learning_rate', 0.1),
                subsample=self.config.get('subsample', 0.8),
                colsample_bytree=self.config.get('colsample_bytree', 0.8),
                random_state=self.config.get('random_state', 42),
                n_jobs=-1
            )
        elif model_type == 'random_forest':
            model = RandomForestRegressor(
                n_estimators=self.config.get('n_estimators', 100),
                max_depth=self.config.get('max_depth', 10),
                random_state=self.config.get('random_state', 42),
                n_jobs=-1
            )
        elif model_type == 'linear':
            model = LinearRegression()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Create pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        # Split data for training and validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, 
            test_size=self.config.get('val_size', 0.2),
            random_state=self.config.get('random_state', 42)
        )
        
        # Train model
        pipeline.fit(X_train, y_train)
        
        # Make predictions
        y_train_pred = pipeline.predict(X_train)
        y_val_pred = pipeline.predict(X_val)
        
        # Calculate metrics
        metrics = {
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'train_mse': mean_squared_error(y_train, y_train_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'train_r2': r2_score(y_train, y_train_pred),
            'val_mae': mean_absolute_error(y_val, y_val_pred),
            'val_mse': mean_squared_error(y_val, y_val_pred),
            'val_rmse': np.sqrt(mean_squared_error(y_val, y_val_pred)),
            'val_r2': r2_score(y_val, y_val_pred),
            'train_samples': len(X_train),
            'val_samples': len(X_val)
        }
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        def calculate_mape(y_true, y_pred):
            return np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100
        
        metrics['train_mape'] = calculate_mape(y_train, y_train_pred)
        metrics['val_mape'] = calculate_mape(y_val, y_val_pred)
        
        logger.info(f"Model training completed for {target_name}")
        logger.info(f"Validation MAPE: {metrics['val_mape']:.2f}%")
        logger.info(f"Validation R²: {metrics['val_r2']:.4f}")
        
        return pipeline, metrics
    
    def train_separate_models_by_content_type(
        self, 
        features_df: pd.DataFrame, 
        targets: Dict[str, pd.Series]
    ) -> Dict[str, Any]:
        """
        Train separate models for Shorts and Long-form content.
        
        Args:
            features_df: Features DataFrame
            targets: Dictionary of target Series
            
        Returns:
            Training results dictionary
        """
        logger.info("Training separate models for Shorts and Long-form content...")
        
        results = {
            'shorts_models': {},
            'longform_models': {},
            'shorts_metrics': {},
            'longform_metrics': {},
            'training_info': {}
        }
        
        # Check if we have content type information
        if 'is_short' not in features_df.columns:
            logger.warning("No 'is_short' column found. Training unified models instead.")
            return self.train_unified_models(features_df, targets)
        
        # Split data by content type
        shorts_mask = features_df['is_short'] == True
        longform_mask = features_df['is_short'] == False
        
        shorts_features = features_df[shorts_mask].copy()
        longform_features = features_df[longform_mask].copy()
        
        logger.info(f"Shorts samples: {len(shorts_features)}")
        logger.info(f"Long-form samples: {len(longform_features)}")
        
        # Train models for each target and content type
        for target_name, target_series in targets.items():
            logger.info(f"\nTraining models for target: {target_name}")
            
            # Shorts models
            if len(shorts_features) >= self.config.get('min_samples', 50):
                shorts_target = target_series[shorts_mask]
                shorts_pipeline, shorts_metrics = self.train_model_for_target(
                    shorts_features, shorts_target, f"{target_name}_shorts"
                )
                results['shorts_models'][target_name] = shorts_pipeline
                results['shorts_metrics'][target_name] = shorts_metrics
            else:
                logger.warning(f"Insufficient Shorts samples for {target_name}: {len(shorts_features)}")
            
            # Long-form models
            if len(longform_features) >= self.config.get('min_samples', 50):
                longform_target = target_series[longform_mask]
                longform_pipeline, longform_metrics = self.train_model_for_target(
                    longform_features, longform_target, f"{target_name}_longform"
                )
                results['longform_models'][target_name] = longform_pipeline
                results['longform_metrics'][target_name] = longform_metrics
            else:
                logger.warning(f"Insufficient Long-form samples for {target_name}: {len(longform_features)}")
        
        # Store training info
        results['training_info'] = {
            'total_samples': len(features_df),
            'shorts_samples': len(shorts_features),
            'longform_samples': len(longform_features),
            'targets_trained': list(targets.keys()),
            'training_timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def train_unified_models(
        self, 
        features_df: pd.DataFrame, 
        targets: Dict[str, pd.Series]
    ) -> Dict[str, Any]:
        """
        Train unified models for all content types.
        
        Args:
            features_df: Features DataFrame
            targets: Dictionary of target Series
            
        Returns:
            Training results dictionary
        """
        logger.info("Training unified models for all content types...")
        
        results = {
            'unified_models': {},
            'unified_metrics': {},
            'training_info': {}
        }
        
        # Train models for each target
        for target_name, target_series in targets.items():
            logger.info(f"\nTraining unified model for target: {target_name}")
            
            pipeline, metrics = self.train_model_for_target(
                features_df, target_series, f"{target_name}_unified"
            )
            results['unified_models'][target_name] = pipeline
            results['unified_metrics'][target_name] = metrics
        
        # Store training info
        results['training_info'] = {
            'total_samples': len(features_df),
            'targets_trained': list(targets.keys()),
            'training_timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def save_models(self, results: Dict[str, Any]) -> None:
        """
        Save trained models to disk.
        
        Args:
            results: Training results dictionary
        """
        logger.info("Saving trained models...")
        
        # Save shorts models
        if 'shorts_models' in results:
            for target_name, model in results['shorts_models'].items():
                model_path = self.models_dir / f'shorts_{target_name}_model.joblib'
                joblib.dump(model, model_path)
                logger.info(f"Saved shorts model for {target_name}: {model_path}")
        
        # Save longform models
        if 'longform_models' in results:
            for target_name, model in results['longform_models'].items():
                model_path = self.models_dir / f'longform_{target_name}_model.joblib'
                joblib.dump(model, model_path)
                logger.info(f"Saved longform model for {target_name}: {model_path}")
        
        # Save unified models
        if 'unified_models' in results:
            for target_name, model in results['unified_models'].items():
                model_path = self.models_dir / f'unified_{target_name}_model.joblib'
                joblib.dump(model, model_path)
                logger.info(f"Saved unified model for {target_name}: {model_path}")
    
    def save_results(self, results: Dict[str, Any]) -> None:
        """
        Save training results and metrics.
        
        Args:
            results: Training results dictionary
        """
        logger.info("Saving training results...")
        
        # Create results summary
        results_summary = {
            'training_info': results.get('training_info', {}),
            'shorts_metrics': results.get('shorts_metrics', {}),
            'longform_metrics': results.get('longform_metrics', {}),
            'unified_metrics': results.get('unified_metrics', {}),
            'config_used': self.config
        }
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_path = self.results_dir / f'training_results_{timestamp}.json'
        
        with open(results_path, 'w') as f:
            json.dump(results_summary, f, indent=2, default=str)
        
        logger.info(f"Saved training results: {results_path}")
    
    def generate_training_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive training report.
        
        Args:
            results: Training results dictionary
            
        Returns:
            Report string
        """
        logger.info("Generating training report...")
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("VIEWTRENDSSL MODEL TRAINING REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Training info
        training_info = results.get('training_info', {})
        report_lines.append("TRAINING SUMMARY:")
        report_lines.append(f"  Total samples: {training_info.get('total_samples', 'N/A'):,}")
        report_lines.append(f"  Shorts samples: {training_info.get('shorts_samples', 'N/A'):,}")
        report_lines.append(f"  Long-form samples: {training_info.get('longform_samples', 'N/A'):,}")
        report_lines.append(f"  Targets trained: {', '.join(training_info.get('targets_trained', []))}")
        report_lines.append(f"  Training timestamp: {training_info.get('training_timestamp', 'N/A')}")
        report_lines.append("")
        
        # Shorts model performance
        if 'shorts_metrics' in results and results['shorts_metrics']:
            report_lines.append("SHORTS MODEL PERFORMANCE:")
            for target, metrics in results['shorts_metrics'].items():
                report_lines.append(f"  {target}:")
                report_lines.append(f"    Validation MAPE: {metrics.get('val_mape', 0):.2f}%")
                report_lines.append(f"    Validation R²: {metrics.get('val_r2', 0):.4f}")
                report_lines.append(f"    Validation RMSE: {metrics.get('val_rmse', 0):.2f}")
                report_lines.append(f"    Training samples: {metrics.get('train_samples', 0):,}")
                report_lines.append(f"    Validation samples: {metrics.get('val_samples', 0):,}")
            report_lines.append("")
        
        # Long-form model performance
        if 'longform_metrics' in results and results['longform_metrics']:
            report_lines.append("LONG-FORM MODEL PERFORMANCE:")
            for target, metrics in results['longform_metrics'].items():
                report_lines.append(f"  {target}:")
                report_lines.append(f"    Validation MAPE: {metrics.get('val_mape', 0):.2f}%")
                report_lines.append(f"    Validation R²: {metrics.get('val_r2', 0):.4f}")
                report_lines.append(f"    Validation RMSE: {metrics.get('val_rmse', 0):.2f}")
                report_lines.append(f"    Training samples: {metrics.get('train_samples', 0):,}")
                report_lines.append(f"    Validation samples: {metrics.get('val_samples', 0):,}")
            report_lines.append("")
        
        # Unified model performance
        if 'unified_metrics' in results and results['unified_metrics']:
            report_lines.append("UNIFIED MODEL PERFORMANCE:")
            for target, metrics in results['unified_metrics'].items():
                report_lines.append(f"  {target}:")
                report_lines.append(f"    Validation MAPE: {metrics.get('val_mape', 0):.2f}%")
                report_lines.append(f"    Validation R²: {metrics.get('val_r2', 0):.4f}")
                report_lines.append(f"    Validation RMSE: {metrics.get('val_rmse', 0):.2f}")
                report_lines.append(f"    Training samples: {metrics.get('train_samples', 0):,}")
                report_lines.append(f"    Validation samples: {metrics.get('val_samples', 0):,}")
            report_lines.append("")
        
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def run_complete_training_pipeline(
        self, 
        data_path: str, 
        feature_info_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run the complete model training pipeline.
        
        Args:
            data_path: Path to processed training data
            feature_info_path: Path to feature information JSON
            
        Returns:
            Training results dictionary
        """
        logger.info("Starting complete model training pipeline...")
        start_time = datetime.now()
        
        try:
            # Load processed data
            df = self.load_processed_data(data_path)
            
            # Load feature information
            if feature_info_path:
                self.feature_info = self.load_feature_info(feature_info_path)
            
            # Prepare features and targets
            features_df, targets = self.prepare_features_and_targets(df)
            
            # Train models
            if self.config.get('separate_by_content_type', True):
                results = self.train_separate_models_by_content_type(features_df, targets)
            else:
                results = self.train_unified_models(features_df, targets)
            
            # Save models
            if self.config.get('save_models', True):
                self.save_models(results)
            
            # Save results
            if self.config.get('save_results', True):
                self.save_results(results)
            
            # Generate and save report
            report = self.generate_training_report(results)
            
            # Save report to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = self.results_dir / f'training_report_{timestamp}.txt'
            with open(report_path, 'w') as f:
                f.write(report)
            
            logger.info(f"Training report saved: {report_path}")
            
            # Print report
            print("\n" + report)
            
            # Add pipeline info to results
            end_time = datetime.now()
            processing_duration = (end_time - start_time).total_seconds()
            
            results['pipeline_info'] = {
                'pipeline_status': 'completed',
                'processing_duration_seconds': processing_duration,
                'started_at': start_time.isoformat(),
                'completed_at': end_time.isoformat(),
                'input_file': data_path,
                'feature_info_file': feature_info_path,
                'models_directory': str(self.models_dir),
                'results_directory': str(self.results_dir)
            }
            
            logger.info(f"Model training completed in {processing_duration:.1f} seconds")
            
            return results
            
        except Exception as e:
            logger.error(f"Model training pipeline failed: {e}")
            raise


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults."""
    
    default_config = {
        'models_dir': 'models',
        'results_dir': 'results',
        'separate_by_content_type': True,
        'save_models': True,
        'save_results': True,
        'model_type': 'xgboost',
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'val_size': 0.2,
        'min_samples': 50,
        'random_state': 42
    }
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                file_config = json.load(f)
            
            default_config.update(file_config)
            logger.info(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            logger.warning(f"Error loading config file {config_path}: {e}")
            logger.info("Using default configuration")
    
    return default_config


def main():
    """Main training script entry point."""
    parser = argparse.ArgumentParser(description='Train ViewTrendsSL models using processed CSV data')
    
    parser.add_argument(
        'data_path',
        help='Path to processed training data CSV file'
    )
    
    parser.add_argument(
        '--feature-info',
        type=str,
        help='Path to feature information JSON file'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--models-dir',
        type=str,
        help='Directory to save trained models'
    )
    
    parser.add_argument(
        '--results-dir',
        type=str,
        help='Directory to save training results'
    )
    
    parser.add_argument(
        '--model-type',
        choices=['xgboost', 'random_forest', 'linear'],
        default='xgboost',
        help='Type of model to train'
    )
    
    parser.add_argument(
        '--unified',
        action='store_true',
        help='Train unified models instead of separate models for content types'
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Override with command line arguments
        if args.models_dir:
            config['models_dir'] = args.models_dir
        if args.results_dir:
            config['results_dir'] = args.results_dir
        if args.model_type:
            config['model_type'] = args.model_type
        if args.unified:
            config['separate_by_content_type'] = False
        
        # Validate input file
        if not os.path.exists(args.data_path):
            logger.error(f"Input file not found: {args.data_path}")
            return 1
        
        # Initialize trainer
        trainer = EnhancedModelTrainer(config)
        
        # Run training pipeline
        results = trainer.run_complete_training_pipeline(
            args.data_path, 
            args.feature_info
        )
        
        logger.info("Model training completed successfully!")
        logger.info(f"Models saved to: {results['pipeline_info']['models_directory']}")
        logger.info(f"Results saved to: {results['pipeline_info']['results_directory']}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Model training failed: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
