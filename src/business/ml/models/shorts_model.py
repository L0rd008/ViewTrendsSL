"""
YouTube Shorts Prediction Model

This module contains the machine learning model specifically designed
for predicting viewership of YouTube Shorts videos.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import pickle
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from sklearn.ensemble import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logger = logging.getLogger(__name__)


class ShortsModel:
    """Machine learning model for YouTube Shorts viewership prediction."""
    
    def __init__(self, model_path: str = 'data/models/shorts/shorts_model.pkl'):
        """
        Initialize the Shorts model.
        
        Args:
            model_path: Path to the saved model file
        """
        self.model_path = model_path
        self.model = None
        self.preprocessor = None
        self.feature_names = []
        self.model_metadata = {}
        self.is_loaded = False
        
        # Model configuration
        self.model_config = {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42
        }
    
    def load_model(self) -> bool:
        """
        Load the trained model from disk.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            # Load model and metadata
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.preprocessor = model_data.get('preprocessor')
            self.feature_names = model_data.get('feature_names', [])
            self.model_metadata = model_data.get('metadata', {})
            
            self.is_loaded = True
            logger.info("Shorts model loaded successfully")
            return True
            
        except FileNotFoundError:
            logger.warning(f"Model file not found: {self.model_path}")
            # Initialize with default model for development
            self._initialize_default_model()
            return True
            
        except Exception as e:
            logger.error(f"Failed to load Shorts model: {str(e)}")
            return False
    
    def save_model(self) -> bool:
        """
        Save the trained model to disk.
        
        Returns:
            True if model saved successfully, False otherwise
        """
        try:
            import os
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            model_data = {
                'model': self.model,
                'preprocessor': self.preprocessor,
                'feature_names': self.feature_names,
                'metadata': self.model_metadata
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Shorts model saved to {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save Shorts model: {str(e)}")
            return False
    
    def predict(self, features: Dict[str, Any], timeframe: int = 7) -> Dict[str, Any]:
        """
        Make a prediction for a YouTube Short.
        
        Args:
            features: Feature dictionary
            timeframe: Prediction timeframe in days
            
        Returns:
            Dictionary containing prediction and confidence
        """
        try:
            if not self.is_loaded:
                raise ValueError("Model not loaded")
            
            # Convert features to DataFrame
            feature_df = self._prepare_features(features)
            
            # Make prediction
            prediction = self.model.predict(feature_df)[0]
            
            # Calculate confidence score
            confidence = self._calculate_confidence(feature_df, prediction)
            
            # Apply timeframe adjustment
            adjusted_prediction = self._adjust_for_timeframe(prediction, timeframe)
            
            return {
                'prediction': max(0, int(adjusted_prediction)),
                'confidence': confidence,
                'timeframe_days': timeframe,
                'model_version': self.get_version()
            }
            
        except Exception as e:
            logger.error(f"Shorts prediction error: {str(e)}")
            raise
    
    def predict_batch(self, features_list: List[Dict[str, Any]], timeframe: int = 7) -> List[Dict[str, Any]]:
        """
        Make predictions for multiple YouTube Shorts.
        
        Args:
            features_list: List of feature dictionaries
            timeframe: Prediction timeframe in days
            
        Returns:
            List of prediction results
        """
        try:
            if not self.is_loaded:
                raise ValueError("Model not loaded")
            
            results = []
            
            for features in features_list:
                try:
                    result = self.predict(features, timeframe)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Batch prediction error for features {features}: {str(e)}")
                    results.append({
                        'prediction': 0,
                        'confidence': 0.0,
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Batch prediction error: {str(e)}")
            raise
    
    def train(self, training_data: pd.DataFrame, target_column: str = 'views_7_days') -> Dict[str, Any]:
        """
        Train the Shorts model.
        
        Args:
            training_data: Training dataset
            target_column: Target column name
            
        Returns:
            Training results and metrics
        """
        try:
            logger.info("Starting Shorts model training")
            
            # Prepare features and target
            X, y = self._prepare_training_data(training_data, target_column)
            
            # Initialize model
            self.model = XGBRegressor(**self.model_config)
            
            # Train model
            self.model.fit(X, y)
            
            # Make predictions for evaluation
            y_pred = self.model.predict(X)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y, y_pred)
            
            # Update metadata
            self.model_metadata.update({
                'trained_at': datetime.now().isoformat(),
                'training_samples': len(training_data),
                'target_column': target_column,
                'metrics': metrics,
                'version': self._generate_version()
            })
            
            self.is_loaded = True
            
            logger.info(f"Shorts model training completed. R² Score: {metrics['r2_score']:.4f}")
            
            return {
                'success': True,
                'metrics': metrics,
                'training_samples': len(training_data),
                'feature_importance': self._get_feature_importance()
            }
            
        except Exception as e:
            logger.error(f"Shorts model training error: {str(e)}")
            raise
    
    def evaluate(self, test_data: pd.DataFrame, target_column: str = 'views_7_days') -> Dict[str, Any]:
        """
        Evaluate the model on test data.
        
        Args:
            test_data: Test dataset
            target_column: Target column name
            
        Returns:
            Evaluation metrics
        """
        try:
            if not self.is_loaded:
                raise ValueError("Model not loaded")
            
            # Prepare test data
            X_test, y_test = self._prepare_training_data(test_data, target_column)
            
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred)
            
            return {
                'test_samples': len(test_data),
                'metrics': metrics,
                'feature_importance': self._get_feature_importance()
            }
            
        except Exception as e:
            logger.error(f"Model evaluation error: {str(e)}")
            raise
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance scores.
        
        Returns:
            Dictionary of feature importance scores
        """
        return self._get_feature_importance()
    
    def get_version(self) -> str:
        """
        Get model version.
        
        Returns:
            Model version string
        """
        return self.model_metadata.get('version', '1.0.0')
    
    def get_accuracy_metrics(self) -> Dict[str, float]:
        """
        Get model accuracy metrics.
        
        Returns:
            Dictionary of accuracy metrics
        """
        return self.model_metadata.get('metrics', {})
    
    def get_feature_names(self) -> List[str]:
        """
        Get list of feature names used by the model.
        
        Returns:
            List of feature names
        """
        return self.feature_names.copy()
    
    def get_last_trained_date(self) -> Optional[str]:
        """
        Get the date when the model was last trained.
        
        Returns:
            ISO format date string or None
        """
        return self.model_metadata.get('trained_at')
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get comprehensive model information.
        
        Returns:
            Dictionary containing model information
        """
        return {
            'model_type': 'YouTube Shorts Prediction',
            'algorithm': 'XGBoost Regressor',
            'version': self.get_version(),
            'is_loaded': self.is_loaded,
            'feature_count': len(self.feature_names),
            'last_trained': self.get_last_trained_date(),
            'metrics': self.get_accuracy_metrics(),
            'config': self.model_config
        }
    
    # Private helper methods
    def _initialize_default_model(self):
        """Initialize a default model for development."""
        logger.info("Initializing default Shorts model")
        
        self.model = XGBRegressor(**self.model_config)
        self.feature_names = [
            'duration_seconds', 'title_length', 'description_length',
            'publish_hour', 'publish_day_of_week', 'channel_subscriber_count',
            'channel_video_count', 'category_id', 'has_tags'
        ]
        self.model_metadata = {
            'version': '1.0.0-dev',
            'trained_at': datetime.now().isoformat(),
            'training_samples': 0,
            'metrics': {'r2_score': 0.0, 'mae': 0.0, 'rmse': 0.0}
        }
        self.is_loaded = True
    
    def _prepare_features(self, features: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare features for prediction.
        
        Args:
            features: Raw features dictionary
            
        Returns:
            Prepared feature DataFrame
        """
        # Create feature vector based on expected features
        feature_vector = {}
        
        # Duration (should be <= 60 seconds for Shorts)
        feature_vector['duration_seconds'] = min(features.get('duration_seconds', 30), 60)
        
        # Title and description features
        feature_vector['title_length'] = len(features.get('title', ''))
        feature_vector['description_length'] = len(features.get('description', ''))
        
        # Time-based features
        published_at = features.get('published_at', datetime.now())
        if isinstance(published_at, str):
            published_at = pd.to_datetime(published_at)
        
        feature_vector['publish_hour'] = published_at.hour
        feature_vector['publish_day_of_week'] = published_at.weekday()
        
        # Channel features
        feature_vector['channel_subscriber_count'] = features.get('channel_subscriber_count', 1000)
        feature_vector['channel_video_count'] = features.get('channel_video_count', 10)
        
        # Category
        feature_vector['category_id'] = features.get('category_id', 24)  # Entertainment default
        
        # Tags
        tags = features.get('tags', [])
        feature_vector['has_tags'] = 1 if tags else 0
        
        return pd.DataFrame([feature_vector])
    
    def _prepare_training_data(self, data: pd.DataFrame, target_column: str) -> tuple:
        """
        Prepare training data.
        
        Args:
            data: Raw training data
            target_column: Target column name
            
        Returns:
            Tuple of (X, y) for training
        """
        # Select feature columns
        feature_columns = [col for col in self.feature_names if col in data.columns]
        X = data[feature_columns].copy()
        
        # Handle missing values
        X = X.fillna(0)
        
        # Target variable
        y = data[target_column].values
        
        # Update feature names
        self.feature_names = feature_columns
        
        return X, y
    
    def _calculate_confidence(self, features: pd.DataFrame, prediction: float) -> float:
        """
        Calculate confidence score for prediction.
        
        Args:
            features: Feature DataFrame
            prediction: Model prediction
            
        Returns:
            Confidence score between 0 and 1
        """
        # Simple confidence calculation based on feature completeness
        # In a real implementation, this could use prediction intervals
        
        feature_completeness = (features.notna().sum().sum()) / (len(features.columns))
        
        # Base confidence on feature completeness and prediction magnitude
        base_confidence = 0.7
        feature_bonus = feature_completeness * 0.2
        
        # Adjust based on prediction range (lower confidence for extreme predictions)
        if prediction > 100000:  # Very high prediction
            prediction_penalty = 0.1
        elif prediction < 100:  # Very low prediction
            prediction_penalty = 0.1
        else:
            prediction_penalty = 0.0
        
        confidence = base_confidence + feature_bonus - prediction_penalty
        
        return max(0.1, min(1.0, confidence))
    
    def _adjust_for_timeframe(self, prediction: float, timeframe: int) -> float:
        """
        Adjust prediction based on timeframe.
        
        Args:
            prediction: Base prediction (7-day default)
            timeframe: Target timeframe in days
            
        Returns:
            Adjusted prediction
        """
        # Simple timeframe adjustment
        # Shorts typically get most views in first few days
        
        if timeframe <= 1:
            return prediction * 0.6  # 60% of 7-day views in first day
        elif timeframe <= 3:
            return prediction * 0.8  # 80% of 7-day views in first 3 days
        elif timeframe <= 7:
            return prediction  # Base prediction is for 7 days
        elif timeframe <= 30:
            return prediction * 1.2  # 20% more views by 30 days
        else:
            return prediction * 1.3  # 30% more views for longer periods
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate evaluation metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100
        
        return {
            'mae': float(mae),
            'mse': float(mse),
            'rmse': float(rmse),
            'r2_score': float(r2),
            'mape': float(mape)
        }
    
    def _get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the trained model.
        
        Returns:
            Dictionary of feature importance scores
        """
        if not self.model or not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importance_dict = {}
        for i, importance in enumerate(self.model.feature_importances_):
            if i < len(self.feature_names):
                importance_dict[self.feature_names[i]] = float(importance)
        
        return importance_dict
    
    def _generate_version(self) -> str:
        """
        Generate a version string for the model.
        
        Returns:
            Version string
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"1.0.{timestamp}"
