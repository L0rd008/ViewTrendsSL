"""
ML Model Training Orchestrator for ViewTrendsSL

This module provides the main training orchestrator that coordinates
data loading, feature engineering, model training, and evaluation.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json
import joblib

from src.business.ml.training.data_loader import DataLoader
from src.business.ml.preprocessing.feature_pipeline import FeaturePipeline
from src.business.ml.models.shorts_model import ShortsModel
from src.business.ml.models.longform_model import LongformModel
from src.business.ml.evaluation.evaluator import ModelEvaluator

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Main training orchestrator for ViewTrendsSL ML models."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model trainer.
        
        Args:
            config: Optional training configuration
        """
        self.config = config or self._get_default_config()
        
        # Initialize components
        self.data_loader = DataLoader(self.config.get('database_path', 'data/viewtrendssl.db'))
        self.feature_pipeline = FeaturePipeline(self.config.get('feature_config'))
        self.evaluator = ModelEvaluator()
        
        # Model instances
        self.shorts_model = None
        self.longform_model = None
        
        # Training results
        self.training_results = {}
        
        logger.info("ModelTrainer initialized")
    
    def train_all_models(self, 
                        target_timeframe: int = 7,
                        save_models: bool = True,
                        save_data: bool = True) -> Dict[str, Any]:
        """
        Train all models (Shorts and Long-form).
        
        Args:
            target_timeframe: Target prediction timeframe in days
            save_models: Whether to save trained models
            save_data: Whether to save processed data
            
        Returns:
            Dictionary with training results
        """
        try:
            logger.info(f"Starting training pipeline for {target_timeframe}-day prediction")
            
            results = {
                'target_timeframe': target_timeframe,
                'started_at': datetime.now().isoformat(),
                'models': {},
                'data_summary': {},
                'feature_importance': {},
                'evaluation_metrics': {}
            }
            
            # Step 1: Load and prepare data
            logger.info("Step 1: Loading and preparing data")
            data_results = self._prepare_training_data(target_timeframe, save_data)
            results['data_summary'] = data_results['summary']
            
            # Step 2: Train Shorts model
            logger.info("Step 2: Training Shorts model")
            shorts_results = self._train_shorts_model(
                data_results['shorts_train'],
                data_results['shorts_val'],
                data_results['shorts_test'],
                target_timeframe,
                save_models
            )
            results['models']['shorts'] = shorts_results
            
            # Step 3: Train Long-form model
            logger.info("Step 3: Training Long-form model")
            longform_results = self._train_longform_model(
                data_results['longform_train'],
                data_results['longform_val'],
                data_results['longform_test'],
                target_timeframe,
                save_models
            )
            results['models']['longform'] = longform_results
            
            # Step 4: Combined evaluation
            logger.info("Step 4: Performing combined evaluation")
            combined_results = self._evaluate_combined_models(
                data_results['shorts_test'],
                data_results['longform_test'],
                target_timeframe
            )
            results['evaluation_metrics'] = combined_results
            
            # Step 5: Feature importance analysis
            logger.info("Step 5: Analyzing feature importance")
            feature_importance = self._analyze_feature_importance()
            results['feature_importance'] = feature_importance
            
            results['completed_at'] = datetime.now().isoformat()
            results['success'] = True
            
            # Save training results
            self._save_training_results(results)
            
            logger.info("Training pipeline completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Training pipeline failed: {str(e)}")
            results['error'] = str(e)
            results['success'] = False
            return results
    
    def train_single_model(self, 
                          model_type: str,
                          target_timeframe: int = 7,
                          save_model: bool = True) -> Dict[str, Any]:
        """
        Train a single model (either Shorts or Long-form).
        
        Args:
            model_type: Type of model ('shorts' or 'longform')
            target_timeframe: Target prediction timeframe in days
            save_model: Whether to save the trained model
            
        Returns:
            Training results for the specific model
        """
        try:
            logger.info(f"Training {model_type} model for {target_timeframe}-day prediction")
            
            if model_type not in ['shorts', 'longform']:
                raise ValueError("model_type must be 'shorts' or 'longform'")
            
            # Load data for specific model type
            data = self.data_loader.load_training_data(
                video_type=model_type,
                target_timeframe=target_timeframe,
                min_age_days=self.config['data']['min_age_days'],
                max_age_days=self.config['data']['max_age_days']
            )
            
            if data.empty:
                raise ValueError(f"No training data found for {model_type} videos")
            
            # Apply feature engineering
            data = self.feature_pipeline.fit_transform(data)
            
            # Split data
            train_df, val_df, test_df = self.data_loader.split_data(
                data, 
                stratify_column='category_id',
                time_based_split=self.config['training']['time_based_split']
            )
            
            # Train model
            if model_type == 'shorts':
                results = self._train_shorts_model(train_df, val_df, test_df, target_timeframe, save_model)
            else:
                results = self._train_longform_model(train_df, val_df, test_df, target_timeframe, save_model)
            
            logger.info(f"{model_type} model training completed")
            return results
            
        except Exception as e:
            logger.error(f"Failed to train {model_type} model: {str(e)}")
            raise
    
    def evaluate_models(self, test_data_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Evaluate trained models on test data.
        
        Args:
            test_data_path: Optional path to test data file
            
        Returns:
            Evaluation results
        """
        try:
            logger.info("Evaluating trained models")
            
            # Load test data
            if test_data_path:
                test_data = pd.read_csv(test_data_path)
            else:
                # Load fresh test data
                test_data = self.data_loader.load_training_data(
                    video_type='all',
                    target_timeframe=7,
                    min_age_days=7,
                    max_age_days=30
                )
            
            if test_data.empty:
                raise ValueError("No test data available")
            
            # Apply feature engineering
            test_data = self.feature_pipeline.transform(test_data)
            
            # Split by video type
            shorts_test = test_data[test_data['is_short'] == 1]
            longform_test = test_data[test_data['is_short'] == 0]
            
            results = {}
            
            # Evaluate Shorts model
            if not shorts_test.empty and self.shorts_model:
                shorts_results = self.shorts_model.evaluate(shorts_test)
                results['shorts'] = shorts_results
            
            # Evaluate Long-form model
            if not longform_test.empty and self.longform_model:
                longform_results = self.longform_model.evaluate(longform_test)
                results['longform'] = longform_results
            
            # Combined evaluation
            if results:
                combined_results = self._evaluate_combined_models(shorts_test, longform_test, 7)
                results['combined'] = combined_results
            
            return results
            
        except Exception as e:
            logger.error(f"Model evaluation failed: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about trained models.
        
        Returns:
            Dictionary with model information
        """
        info = {
            'shorts_model': None,
            'longform_model': None,
            'feature_pipeline': {
                'is_fitted': self.feature_pipeline.is_fitted,
                'feature_count': len(self.feature_pipeline.feature_names)
            }
        }
        
        if self.shorts_model:
            info['shorts_model'] = self.shorts_model.get_model_info()
        
        if self.longform_model:
            info['longform_model'] = self.longform_model.get_model_info()
        
        return info
    
    def load_models(self, models_dir: str = "models") -> bool:
        """
        Load trained models from disk.
        
        Args:
            models_dir: Directory containing saved models
            
        Returns:
            True if models loaded successfully
        """
        try:
            models_path = Path(models_dir)
            
            # Load Shorts model
            shorts_path = models_path / "shorts_model.pkl"
            if shorts_path.exists():
                self.shorts_model = ShortsModel(str(shorts_path))
                self.shorts_model.load_model()
                logger.info("Shorts model loaded")
            
            # Load Long-form model
            longform_path = models_path / "longform_model.pkl"
            if longform_path.exists():
                self.longform_model = LongformModel(str(longform_path))
                self.longform_model.load_model()
                logger.info("Long-form model loaded")
            
            # Load feature pipeline
            pipeline_path = models_path / "feature_pipeline.pkl"
            if pipeline_path.exists():
                self.feature_pipeline.load_pipeline(str(pipeline_path))
                logger.info("Feature pipeline loaded")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load models: {str(e)}")
            return False
    
    # Private helper methods
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default training configuration."""
        return {
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
                    'learning_rate': 0.1
                },
                'longform': {
                    'algorithm': 'xgboost',
                    'n_estimators': 150,
                    'max_depth': 8,
                    'learning_rate': 0.1
                }
            }
        }
    
    def _prepare_training_data(self, target_timeframe: int, save_data: bool) -> Dict[str, Any]:
        """Prepare training data for both model types."""
        
        # Load all data
        all_data = self.data_loader.load_training_data(
            video_type='all',
            target_timeframe=target_timeframe,
            min_age_days=self.config['data']['min_age_days'],
            max_age_days=self.config['data']['max_age_days']
        )
        
        if all_data.empty:
            raise ValueError("No training data found")
        
        # Apply feature engineering
        all_data = self.feature_pipeline.fit_transform(all_data)
        
        # Split by video type
        shorts_data = all_data[all_data['is_short'] == 1].copy()
        longform_data = all_data[all_data['is_short'] == 0].copy()
        
        # Split each dataset
        shorts_train, shorts_val, shorts_test = self.data_loader.split_data(
            shorts_data, 
            stratify_column='category_id',
            time_based_split=self.config['training']['time_based_split']
        )
        
        longform_train, longform_val, longform_test = self.data_loader.split_data(
            longform_data,
            stratify_column='category_id', 
            time_based_split=self.config['training']['time_based_split']
        )
        
        # Save processed data if requested
        if save_data:
            self._save_processed_data({
                'shorts_train': shorts_train,
                'shorts_val': shorts_val,
                'shorts_test': shorts_test,
                'longform_train': longform_train,
                'longform_val': longform_val,
                'longform_test': longform_test
            })
        
        # Generate data summary
        summary = {
            'total_samples': len(all_data),
            'shorts_samples': len(shorts_data),
            'longform_samples': len(longform_data),
            'features': len(self.feature_pipeline.feature_names),
            'splits': {
                'shorts': {
                    'train': len(shorts_train),
                    'val': len(shorts_val),
                    'test': len(shorts_test)
                },
                'longform': {
                    'train': len(longform_train),
                    'val': len(longform_val),
                    'test': len(longform_test)
                }
            }
        }
        
        return {
            'shorts_train': shorts_train,
            'shorts_val': shorts_val,
            'shorts_test': shorts_test,
            'longform_train': longform_train,
            'longform_val': longform_val,
            'longform_test': longform_test,
            'summary': summary
        }
    
    def _train_shorts_model(self, train_df: pd.DataFrame, val_df: pd.DataFrame, 
                           test_df: pd.DataFrame, target_timeframe: int, 
                           save_model: bool) -> Dict[str, Any]:
        """Train the Shorts model."""
        
        model_path = Path(self.config['models_dir']) / "shorts_model.pkl"
        self.shorts_model = ShortsModel(str(model_path))
        
        # Train model
        target_col = f'views_{target_timeframe}_days'
        training_results = self.shorts_model.train(
            train_df, 
            target_column=target_col,
            validation_data=val_df,
            config=self.config['model_config']['shorts']
        )
        
        # Evaluate on test set
        test_results = self.shorts_model.evaluate(test_df, target_col)
        
        # Save model if requested
        if save_model:
            self.shorts_model.save_model()
        
        return {
            'training': training_results,
            'test_evaluation': test_results,
            'model_info': self.shorts_model.get_model_info()
        }
    
    def _train_longform_model(self, train_df: pd.DataFrame, val_df: pd.DataFrame,
                             test_df: pd.DataFrame, target_timeframe: int,
                             save_model: bool) -> Dict[str, Any]:
        """Train the Long-form model."""
        
        model_path = Path(self.config['models_dir']) / "longform_model.pkl"
        self.longform_model = LongformModel(str(model_path))
        
        # Train model
        target_col = f'views_{target_timeframe}_days'
        training_results = self.longform_model.train(
            train_df,
            target_column=target_col,
            validation_data=val_df,
            config=self.config['model_config']['longform']
        )
        
        # Evaluate on test set
        test_results = self.longform_model.evaluate(test_df, target_col)
        
        # Save model if requested
        if save_model:
            self.longform_model.save_model()
        
        return {
            'training': training_results,
            'test_evaluation': test_results,
            'model_info': self.longform_model.get_model_info()
        }
    
    def _evaluate_combined_models(self, shorts_test: pd.DataFrame, 
                                 longform_test: pd.DataFrame,
                                 target_timeframe: int) -> Dict[str, Any]:
        """Evaluate both models together."""
        
        if not self.shorts_model or not self.longform_model:
            return {}
        
        results = {
            'combined_metrics': {},
            'model_comparison': {},
            'prediction_analysis': {}
        }
        
        # Make predictions on test sets
        target_col = f'views_{target_timeframe}_days'
        
        shorts_predictions = []
        longform_predictions = []
        
        if not shorts_test.empty:
            for _, row in shorts_test.iterrows():
                features = row.to_dict()
                pred = self.shorts_model.predict(features, target_timeframe)
                shorts_predictions.append({
                    'actual': row[target_col],
                    'predicted': pred['prediction'],
                    'confidence': pred['confidence']
                })
        
        if not longform_test.empty:
            for _, row in longform_test.iterrows():
                features = row.to_dict()
                pred = self.longform_model.predict(features, target_timeframe)
                longform_predictions.append({
                    'actual': row[target_col],
                    'predicted': pred['prediction'],
                    'confidence': pred['confidence']
                })
        
        # Calculate combined metrics
        all_predictions = shorts_predictions + longform_predictions
        if all_predictions:
            actual_values = [p['actual'] for p in all_predictions]
            predicted_values = [p['predicted'] for p in all_predictions]
            
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            
            results['combined_metrics'] = {
                'mae': float(mean_absolute_error(actual_values, predicted_values)),
                'rmse': float(np.sqrt(mean_squared_error(actual_values, predicted_values))),
                'r2_score': float(r2_score(actual_values, predicted_values)),
                'mape': float(np.mean(np.abs((np.array(actual_values) - np.array(predicted_values)) / 
                                           np.maximum(np.array(actual_values), 1))) * 100)
            }
        
        return results
    
    def _analyze_feature_importance(self) -> Dict[str, Any]:
        """Analyze feature importance across models."""
        
        importance_analysis = {
            'shorts_importance': {},
            'longform_importance': {},
            'common_important_features': [],
            'feature_groups': {}
        }
        
        if self.shorts_model:
            importance_analysis['shorts_importance'] = self.shorts_model.get_feature_importance()
        
        if self.longform_model:
            importance_analysis['longform_importance'] = self.longform_model.get_feature_importance()
        
        # Get feature groups from pipeline
        importance_analysis['feature_groups'] = self.feature_pipeline.get_feature_importance_groups()
        
        return importance_analysis
    
    def _save_processed_data(self, data_splits: Dict[str, pd.DataFrame]):
        """Save processed data splits."""
        
        output_dir = Path("data/processed")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        for split_name, data in data_splits.items():
            filename = f"{split_name}_{timestamp}"
            self.data_loader.save_processed_data(data, filename, split_name)
    
    def _save_training_results(self, results: Dict[str, Any]):
        """Save training results to file."""
        
        output_dir = Path("results")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        results_file = output_dir / f"training_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Training results saved to {results_file}")
