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
        Prepare features and return ALL target series.
        """
        logger.info("Preparing features and targets...")

        original_target_cols = ['views_at_24h', 'views_at_7d', 'views_at_30d']
        targets = {}
        for t in original_target_cols:
            if t in df.columns:
                targets[t] = df[t].copy().fillna(0).clip(lower=0)

        # Exclude ALL possible target columns from the feature set, plus raw data
        exclude_columns = list(targets.keys()) + [
            'video_id', 'channel_id', 'title', 'description', 'tags',
            'published_at', 'inserted_at', 'localized_title', 'localized_description',
            'thumbnail_default', 'thumbnail_medium', 'thumbnail_high',
            'default_language', 'default_audio_language', 'live_broadcast_content',
            'view_count', 'like_count', 'comment_count', 'favourite_count'
        ]

        time_series_raw_cols = [col for col in df.columns if col.startswith('day_')]
        exclude_columns.extend(time_series_raw_cols)

        # Return all other columns as potential features
        feature_columns = [col for col in df.columns if col not in exclude_columns]
        features_df = df[feature_columns].copy()

        logger.info(f"Prepared {len(features_df.columns)} potential features and {len(targets)} target series.")
        return features_df, targets
    
    def create_preprocessor(self, features_df: pd.DataFrame, feature_info: Dict[str, Any]) -> ColumnTransformer:
        """
        Create a robust preprocessing pipeline for features that handles dynamically added columns.
        """
        logger.info("Creating preprocessing pipeline...")
        
        numerical_features = feature_info.get('numerical_features', [])
        categorical_features = feature_info.get('categorical_features', [])

        numerical_features = [col for col in numerical_features if col in features_df.columns]
        categorical_features = [col for col in categorical_features if col in features_df.columns]
        
        for col in features_df.columns:
            if col not in numerical_features and col not in categorical_features:
                logger.info(f"Found new dynamic feature '{col}', categorizing it now.")
                if features_df[col].dtype in ['int64', 'float64']:
                    numerical_features.append(col)
                else:
                    categorical_features.append(col)
        
        logger.info(f"Final Numerical features: {len(numerical_features)}")
        logger.info(f"Final Categorical features: {len(categorical_features)}")
        
        preprocessor_steps = []
        if numerical_features:
            preprocessor_steps.append(('num', StandardScaler(), numerical_features))
        if categorical_features:
            # Add sparse_output=False to ensure a dense array is returned
            preprocessor_steps.append(
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
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
        X_train: pd.DataFrame, 
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        target_name: str,
        model_type: str = 'xgboost'
    ) -> Tuple[Pipeline, Dict[str, Any]]:
        """
        Train a model for a specific target variable using pre-split data.
        """
        logger.info(f"Training {model_type} model for {target_name}...")
        
        preprocessor = self.create_preprocessor(X_train, self.feature_info)
        
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
        else: # Simplified for brevity, your other models remain here
            model = LinearRegression()

        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        logger.info(f"Applying log transform to target variable: {target_name}")
        y_train_log = np.log1p(y_train)
        y_val_log = np.log1p(y_val) # For log R² calculation

        pipeline.fit(X_train, y_train_log)
        
        y_train_pred_log = pipeline.predict(X_train)
        y_val_pred_log = pipeline.predict(X_val)
        
        y_train_pred = np.expm1(y_train_pred_log)
        y_val_pred = np.expm1(y_val_pred_log)
        
        def calculate_smape(y_true, y_pred):
            denom = (np.abs(y_true) + np.abs(y_pred)) / 2
            return np.mean(np.abs(y_true - y_pred) / np.maximum(denom, 1)) * 100

        metrics = {
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'train_r2': r2_score(y_train, y_train_pred),
            'val_mae': mean_absolute_error(y_val, y_val_pred),
            'val_rmse': np.sqrt(mean_squared_error(y_val, y_val_pred)),
            'val_r2': r2_score(y_val, y_val_pred),
            'val_r2_log': r2_score(y_val_log, y_val_pred_log), # R² on log scale
            'train_samples': len(X_train),
            'val_samples': len(X_val),
            'train_smape': calculate_smape(y_train, y_train_pred), # Replaced MAPE
            'val_smape': calculate_smape(y_val, y_val_pred)      # Replaced MAPE
        }
        
        logger.info(f"Model training completed for {target_name}")
        logger.info(f"Validation SMAPE: {metrics['val_smape']:.2f}%")
        logger.info(f"Validation R²: {metrics['val_r2']:.4f} (Log R²: {metrics['val_r2_log']:.4f})")
        
        return pipeline, metrics
    
    def train_separate_models_by_target(
        self, 
        features_df_train: pd.DataFrame, 
        target_series_train: pd.Series,
        features_df_val: pd.DataFrame,
        target_series_val: pd.Series,
        target_name: str
    ) -> Dict[str, Any]:
        """
        Trains Shorts/Long-form models for a SINGLE given target, with safeguards for empty data.
        """
        results = { 'shorts_models': {}, 'longform_models': {}, 'shorts_metrics': {}, 'longform_metrics': {} }
        
        if 'is_short' not in features_df_train.columns:
            logger.warning("No 'is_short' column found, cannot split by content type.")
            return {}

        # Split both train and validation sets by content type
        shorts_mask_train = features_df_train['is_short'] == True
        longform_mask_train = features_df_train['is_short'] == False
        shorts_mask_val = features_df_val['is_short'] == True
        longform_mask_val = features_df_val['is_short'] == False

        shorts_features_train = features_df_train[shorts_mask_train]
        longform_features_train = features_df_train[longform_mask_train]
        shorts_features_val = features_df_val[shorts_mask_val]
        longform_features_val = features_df_val[longform_mask_val]
        
        # --- NEW: Safeguard for Shorts model ---
        if not shorts_features_train.empty and not shorts_features_val.empty:
            logger.info(f"Training Shorts model for {target_name} with {len(shorts_features_train)} train and {len(shorts_features_val)} val samples.")
            shorts_pipeline, shorts_metrics = self.train_model_for_target(
                shorts_features_train, target_series_train[shorts_mask_train],
                shorts_features_val, target_series_val[shorts_mask_val],
                f"{target_name}_shorts"
            )
            results['shorts_models'][target_name] = shorts_pipeline
            results['shorts_metrics'][target_name] = shorts_metrics
        else:
            logger.warning(f"Skipping Shorts model for '{target_name}' due to empty train or validation set after filtering.")

        # --- NEW: Safeguard for Long-form model ---
        if not longform_features_train.empty and not longform_features_val.empty:
            logger.info(f"Training Long-form model for {target_name} with {len(longform_features_train)} train and {len(longform_features_val)} val samples.")
            longform_pipeline, longform_metrics = self.train_model_for_target(
                longform_features_train, target_series_train[longform_mask_train],
                longform_features_val, target_series_val[longform_mask_val],
                f"{target_name}_longform"
            )
            results['longform_models'][target_name] = longform_pipeline
            results['longform_metrics'][target_name] = longform_metrics
        else:
            logger.warning(f"Skipping Long-form model for '{target_name}' due to empty train or validation set after filtering.")

        return results
    
    def train_unified_models(
        self, 
        features_df_train: pd.DataFrame, 
        targets_train: Dict[str, pd.Series],
        features_df_val: pd.DataFrame,
        targets_val: Dict[str, pd.Series]
    ) -> Dict[str, Any]:
        """
        Train unified models for all content types using pre-split data.
        
        Args:
            features_df_train, targets_train: Training data
            features_df_val, targets_val: Validation data
            
        Returns:
            Training results dictionary
        """
        logger.info("Training unified models for all content types...")
        
        results = {
            'unified_models': {},
            'unified_metrics': {},
            'training_info': {}
        }
        
        # Train models for each target using the pre-split data
        for target_name, target_series_train in targets_train.items():
            logger.info(f"\nTraining unified model for target: {target_name}")
            
            # Get the corresponding validation target series
            target_series_val = targets_val[target_name]
            
            pipeline, metrics = self.train_model_for_target(
                X_train=features_df_train, 
                y_train=target_series_train,
                X_val=features_df_val,
                y_val=target_series_val,
                target_name=f"{target_name}_unified"
            )
            results['unified_models'][target_name] = pipeline
            results['unified_metrics'][target_name] = metrics
        
        # Store training info
        results['training_info'] = {
            'train_samples': len(features_df_train),
            'val_samples': len(features_df_val),
            'targets_trained': list(targets_train.keys()),
            'training_timestamp': datetime.now().isoformat()
        }
        
        return results
    
    def save_models(self, results: Dict[str, Any], prefix: str) -> None:
        """
        Save trained models to disk with a given prefix.
        
        Args:
            results: Training results dictionary
            prefix: A prefix for the model filename (e.g., 'at_upload')
        """
        logger.info(f"Saving trained models with prefix '{prefix}'...")
        
        model_types = ['shorts_models', 'longform_models', 'unified_models']
        for model_type in model_types:
            if model_type in results:
                for target_name, model in results[model_type].items():
                    # e.g., models/at_upload_shorts_views_at_30d_model.joblib
                    model_path = self.models_dir / f'{prefix}_{model_type.replace("_models", "")}_{target_name}_model.joblib'
                    joblib.dump(model, model_path)
                    logger.info(f"Saved model for {target_name}: {model_path}")
    
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
        """
        logger.info("Generating training report...")
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("VIEWTRENDSSL MODEL TRAINING REPORT")

        # Training info
        training_info = results.get('training_info', {})
        report_lines.append("TRAINING SUMMARY:")
        report_lines.append(f"  Training samples: {training_info.get('train_samples', 0):,}")
        report_lines.append(f"  Validation samples: {training_info.get('val_samples', 0):,}")
        report_lines.append(f"  - Shorts samples (train): {training_info.get('shorts_samples_train', 0):,}")
        report_lines.append(f"  - Long-form samples (train): {training_info.get('longform_samples_train', 0):,}")
        report_lines.append(f"  Targets trained: {', '.join(training_info.get('targets_trained', []))}")
        report_lines.append(f"  Training timestamp: {training_info.get('training_timestamp', 'N/A')}")
        report_lines.append("")
        
        # Display SMAPE and Log R²
        # Shorts model performance
        if 'shorts_metrics' in results and results['shorts_metrics']:
            report_lines.append("SHORTS MODEL PERFORMANCE:")
            for target, metrics in results['shorts_metrics'].items():
                report_lines.append(f"  {target}:")
                report_lines.append(f"    Validation SMAPE: {metrics.get('val_smape', 0):.2f}%")
                report_lines.append(f"    Validation R² (Log): {metrics.get('val_r2_log', 0):.4f}")
                report_lines.append(f"    Validation R² (Raw): {metrics.get('val_r2', 0):.4f}")
                report_lines.append(f"    Validation RMSE: {metrics.get('val_rmse', 0):.2f}")
            report_lines.append("")
        
        # Long-form model performance
        if 'longform_metrics' in results and results['longform_metrics']:
            report_lines.append("LONG-FORM MODEL PERFORMANCE:")
            for target, metrics in results['longform_metrics'].items():
                report_lines.append(f"  {target}:")
                report_lines.append(f"    Validation SMAPE: {metrics.get('val_smape', 0):.2f}%")
                report_lines.append(f"    Validation R² (Log): {metrics.get('val_r2_log', 0):.4f}")
                report_lines.append(f"    Validation R² (Raw): {metrics.get('val_r2', 0):.4f}")
                report_lines.append(f"    Validation RMSE: {metrics.get('val_rmse', 0):.2f}")
            report_lines.append("")
        
        report_lines.append("=" * 80)
        return "\n".join(report_lines)
    
    def run_complete_training_pipeline(
        self,
        train_data_path: str,
        val_data_path: str,
        feature_info_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run the "At-Upload" model training pipeline.
        This trains models to predict 24h, 7d, and 30d views using ONLY
        metadata available before a video is published.
        """
        logger.info("Starting 'At-Upload' model training pipeline...")
        start_time = datetime.now()

        try:
            # 1. Load data and feature information
            df_train = self.load_processed_data(train_data_path)
            df_val = self.load_processed_data(val_data_path)
            if feature_info_path:
                self.feature_info = self.load_feature_info(feature_info_path)

            base_features_train, all_targets_train = self.prepare_features_and_targets(df_train)
            base_features_val, all_targets_val = self.prepare_features_and_targets(df_val)

            # 2. Define the explicit list of METADATA-ONLY features
            METADATA_FEATURES = [
                col for col in self.feature_info.get('content_features', [])
                if col in base_features_train.columns
            ] + [
                col for col in self.feature_info.get('channel_features', [])
                if col in base_features_train.columns
            ]
            leaky_patterns = ['view', 'like', 'comment', 'growth', 'velocity', 'peak', 'consistency', 'ratio']
            METADATA_FEATURES = [
                f for f in METADATA_FEATURES 
                if not any(leak in f for leak in leaky_patterns)
            ]
            
            # --- FIX 1: Manually add 'is_short' to the feature set ---
            # This is critical for splitting models by content type.
            if 'is_short' in base_features_train.columns and 'is_short' not in METADATA_FEATURES:
                METADATA_FEATURES.append('is_short')

            logger.info(f"Defined {len(METADATA_FEATURES)} metadata-only features for training.")
            X_train = base_features_train[METADATA_FEATURES].copy()
            X_val = base_features_val[METADATA_FEATURES].copy()

            # 3. Loop through targets and train one model for each
            final_results = {'shorts_models': {}, 'longform_models': {}, 'shorts_metrics': {}, 'longform_metrics': {}}
            targets_to_train = ['views_at_24h', 'views_at_7d', 'views_at_30d']
            
            for target_name in targets_to_train:
                logger.info("=" * 50)
                logger.info(f"STARTING TRAINING FOR TARGET: {target_name}")
                logger.info("=" * 50)
                
                min_samples = self.config.get('min_samples_for_training', 50)
                if target_name not in all_targets_train or len(all_targets_train[target_name].dropna()) < min_samples:
                    logger.warning(f"Skipping '{target_name}': Not enough valid samples in the training set.")
                    continue
                if target_name not in all_targets_val or len(all_targets_val[target_name].dropna()) < min_samples:
                    logger.warning(f"Skipping '{target_name}': Not enough valid samples in the validation set.")
                    continue

                target_series_train = all_targets_train[target_name]
                target_series_val = all_targets_val[target_name]

                target_results = self.train_separate_models_by_target(
                    X_train, target_series_train, X_val, target_series_val, target_name
                )
                
                for key in final_results:
                    if key in target_results:
                        final_results[key].update(target_results[key])

            self.save_models(final_results, prefix="at_upload")
            self.save_results(final_results)
            
            end_time = datetime.now()
            processing_duration = (end_time - start_time).total_seconds()
            logger.info(f"Pipeline completed in {processing_duration:.1f} seconds.")
            
            # --- FIX 2: Add pipeline_info back to the results dictionary ---
            final_results['pipeline_info'] = {
                'pipeline_status': 'completed',
                'processing_duration_seconds': processing_duration,
                'started_at': start_time.isoformat(),
                'completed_at': end_time.isoformat(),
                'train_input_file': train_data_path,
                'val_input_file': val_data_path,
                'feature_info_file': feature_info_path,
                'models_directory': str(self.models_dir),
                'results_directory': str(self.results_dir)
            }
            
            return final_results
            
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
    
    # UPDATED: Changed to specific, required arguments
    parser.add_argument(
        '--train-data',
        type=str,
        required=True,
        help='Path to processed training data CSV file (e.g., train_data.csv)'
    )
    parser.add_argument(
        '--val-data',
        type=str,
        required=True,
        help='Path to processed validation data CSV file (e.g., val_data.csv)'
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
        
        # Validate input files
        for path in [args.train_data, args.val_data]:
            if not os.path.exists(path):
                logger.error(f"Input file not found: {path}")
                return 1
        
        # Initialize trainer
        trainer = EnhancedModelTrainer(config)
        
        # Run training pipeline with BOTH paths
        results = trainer.run_complete_training_pipeline(
            train_data_path=args.train_data, 
            val_data_path=args.val_data,
            feature_info_path=args.feature_info
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
