"""
Base Model Class for ViewTrendsSL ML Models

This module provides the abstract base class that all ML models inherit from,
ensuring consistent interfaces and shared functionality across the system.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import pickle
import joblib
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """Abstract base class for all ViewTrendsSL ML models."""
    
    def __init__(self, model_path: str, model_type: str):
        """
        Initialize the base model.
        
        Args:
            model_path: Path to the saved model file
            model_type: Type of model (e.g., 'shorts', 'longform')
        """
        self.model_path = Path(model_path)
        self.model_type = model_type
        self.model = None
        self.preprocessor = None
        self.feature_names = []
        self.model_metadata = {}
        self.is_loaded = False
        self.training_config = {}
        
        # Ensure model directory exists
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize logging
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default model configuration.
        
        Returns:
            Dictionary of default configuration parameters
        """
        pass
    
    @abstractmethod
    def _initialize_model(self, config: Dict[str, Any]):
        """
        Initialize the ML model with given configuration.
        
        Args:
            config: Model configuration parameters
        """
        pass
    
    @abstractmethod
    def _prepare_features(self, features: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare features for prediction.
        
        Args:
            features: Raw features dictionary
            
        Returns:
            Prepared feature DataFrame
        """
        pass
    
    @abstractmethod
    def _get_expected_features(self) -> List[str]:
        """
        Get list of expected feature names.
        
        Returns:
            List of feature names
        """
        pass
    
    def load_model(self) -> bool:
        """
        Load the trained model from disk.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not self.model_path.exists():
                self.logger.warning(f"Model file not found: {self.model_path}")
                self._initialize_default_model()
                return True
            
            # Load model and metadata
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.preprocessor = model_data.get('preprocessor')
            self.feature_names = model_data.get('feature_names', [])
            self.model_metadata = model_data.get('metadata', {})
            self.training_config = model_data.get('training_config', {})
            
            self.is_loaded = True
            self.logger.info(f"{self.model_type} model loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load {self.model_type} model: {str(e)}")
            return False
    
    def save_model(self) -> bool:
        """
        Save the trained model to disk.
        
        Returns:
            True if model saved successfully, False otherwise
        """
        try:
            # Ensure directory exists
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            
            model_data = {
                'model': self.model,
                'preprocessor': self.preprocessor,
                'feature_names': self.feature_names,
                'metadata': self.model_metadata,
                'training_config': self.training_config,
                'model_type': self.model_type,
                'saved_at': datetime.now().isoformat()
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            # Also save metadata as JSON for easy inspection
            metadata_path = self.model_path.with_suffix('.json')
            with open(metadata_path, 'w') as f:
                json.dump({
                    'model_type': self.model_type,
                    'metadata': self.model_metadata,
                    'training_config': self.training_config,
                    'feature_names': self.feature_names,
                    'saved_at': model_data['saved_at']
                }, f, indent=2)
            
            self.logger.info(f"{self.model_type} model saved to {self.model_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save {self.model_type} model: {str(e)}")
            return False
    
    def predict(self, features: Dict[str, Any], timeframe: int = 7) -> Dict[str, Any]:
        """
        Make a prediction.
        
        Args:
            features: Feature dictionary
            timeframe: Prediction timeframe in days
            
        Returns:
            Dictionary containing prediction and confidence
        """
        try:
            if not self.is_loaded:
                if not self.load_model():
                    raise ValueError("Model not loaded and failed to load")
            
            # Validate features
            self._validate_features(features)
            
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
                'confidence': float(confidence),
                'timeframe_days': timeframe,
                'model_version': self.get_version(),
                'model_type': self.model_type,
                'features_used': list(feature_df.columns)
            }
            
        except Exception as e:
            self.logger.error(f"{self.model_type} prediction error: {str(e)}")
            raise
    
    def predict_batch(self, features_list: List[Dict[str, Any]], 
                     timeframe: int = 7) -> List[Dict[str, Any]]:
        """
        Make predictions for multiple items.
        
        Args:
            features_list: List of feature dictionaries
            timeframe: Prediction timeframe in days
            
        Returns:
            List of prediction results
        """
        try:
            if not self.is_loaded:
                if not self.load_model():
                    raise ValueError("Model not loaded and failed to load")
            
            results = []
            
            for i, features in enumerate(features_list):
                try:
                    result = self.predict(features, timeframe)
                    result['batch_index'] = i
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Batch prediction error for item {i}: {str(e)}")
                    results.append({
                        'batch_index': i,
                        'prediction': 0,
                        'confidence': 0.0,
                        'error': str(e),
                        'model_type': self.model_type
                    })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Batch prediction error: {str(e)}")
            raise
    
    def train(self, training_data: pd.DataFrame, 
              target_column: str = 'views_7_days',
              validation_data: Optional[pd.DataFrame] = None,
              config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Train the model.
        
        Args:
            training_data: Training dataset
            target_column: Target column name
            validation_data: Optional validation dataset
            config: Optional training configuration
            
        Returns:
            Training results and metrics
        """
        try:
            self.logger.info(f"Starting {self.model_type} model training")
            
            # Use provided config or default
            if config is None:
                config = self._get_default_config()
            self.training_config = config
            
            # Prepare features and target
            X_train, y_train = self._prepare_training_data(training_data, target_column)
            
            # Prepare validation data if provided
            X_val, y_val = None, None
            if validation_data is not None:
                X_val, y_val = self._prepare_training_data(validation_data, target_column)
            
            # Initialize model
            self._initialize_model(config)
            
            # Train model
            if X_val is not None and hasattr(self.model, 'fit'):
                # Use validation data if model supports it
                try:
                    self.model.fit(X_train, y_train, 
                                 eval_set=[(X_val, y_val)], 
                                 verbose=False)
                except:
                    # Fallback to simple fit
                    self.model.fit(X_train, y_train)
            else:
                self.model.fit(X_train, y_train)
            
            # Calculate training metrics
            y_train_pred = self.model.predict(X_train)
            train_metrics = self._calculate_metrics(y_train, y_train_pred)
            
            # Calculate validation metrics if available
            val_metrics = {}
            if X_val is not None:
                y_val_pred = self.model.predict(X_val)
                val_metrics = self._calculate_metrics(y_val, y_val_pred)
            
            # Update metadata
            self.model_metadata.update({
                'trained_at': datetime.now().isoformat(),
                'training_samples': len(training_data),
                'validation_samples': len(validation_data) if validation_data is not None else 0,
                'target_column': target_column,
                'train_metrics': train_metrics,
                'val_metrics': val_metrics,
                'version': self._generate_version(),
                'model_type': self.model_type
            })
            
            self.is_loaded = True
            
            # Log results
            train_r2 = train_metrics.get('r2_score', 0)
            val_r2 = val_metrics.get('r2_score', 0) if val_metrics else 0
            self.logger.info(f"{self.model_type} model training completed. "
                           f"Train R²: {train_r2:.4f}, Val R²: {val_r2:.4f}")
            
            return {
                'success': True,
                'train_metrics': train_metrics,
                'val_metrics': val_metrics,
                'training_samples': len(training_data),
                'validation_samples': len(validation_data) if validation_data is not None else 0,
                'feature_importance': self._get_feature_importance(),
                'model_type': self.model_type
            }
            
        except Exception as e:
            self.logger.error(f"{self.model_type} model training error: {str(e)}")
            raise
    
    def evaluate(self, test_data: pd.DataFrame, 
                target_column: str = 'views_7_days') -> Dict[str, Any]:
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
                if not self.load_model():
                    raise ValueError("Model not loaded and failed to load")
            
            # Prepare test data
            X_test, y_test = self._prepare_training_data(test_data, target_column)
            
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred)
            
            return {
                'test_samples': len(test_data),
                'metrics': metrics,
                'feature_importance': self._get_feature_importance(),
                'model_type': self.model_type,
                'evaluated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Model evaluation error: {str(e)}")
            raise
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores."""
        return self._get_feature_importance()
    
    def get_version(self) -> str:
        """Get model version."""
        return self.model_metadata.get('version', '1.0.0')
    
    def get_accuracy_metrics(self) -> Dict[str, float]:
        """Get model accuracy metrics."""
        return self.model_metadata.get('val_metrics', 
                                     self.model_metadata.get('train_metrics', {}))
    
    def get_feature_names(self) -> List[str]:
        """Get list of feature names used by the model."""
        return self.feature_names.copy()
    
    def get_last_trained_date(self) -> Optional[str]:
        """Get the date when the model was last trained."""
        return self.model_metadata.get('trained_at')
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information."""
        return {
            'model_type': self.model_type,
            'algorithm': self.training_config.get('algorithm', 'Unknown'),
            'version': self.get_version(),
            'is_loaded': self.is_loaded,
            'feature_count': len(self.feature_names),
            'last_trained': self.get_last_trained_date(),
            'train_metrics': self.model_metadata.get('train_metrics', {}),
            'val_metrics': self.model_metadata.get('val_metrics', {}),
            'config': self.training_config,
            'model_path': str(self.model_path)
        }
    
    # Protected helper methods
    def _initialize_default_model(self):
        """Initialize a default model for development."""
        self.logger.info(f"Initializing default {self.model_type} model")
        
        config = self._get_default_config()
        self._initialize_model(config)
        
        self.feature_names = self._get_expected_features()
        self.model_metadata = {
            'version': '1.0.0-dev',
            'trained_at': datetime.now().isoformat(),
            'training_samples': 0,
            'train_metrics': {'r2_score': 0.0, 'mae': 0.0, 'rmse': 0.0, 'mape': 0.0},
            'model_type': self.model_type
        }
        self.training_config = config
        self.is_loaded = True
    
    def _validate_features(self, features: Dict[str, Any]):
        """
        Validate input features.
        
        Args:
            features: Features to validate
            
        Raises:
            ValueError: If features are invalid
        """
        if not isinstance(features, dict):
            raise ValueError("Features must be a dictionary")
        
        if not features:
            raise ValueError("Features dictionary cannot be empty")
        
        # Check for required features (can be overridden by subclasses)
        required_features = getattr(self, 'required_features', [])
        missing_features = [f for f in required_features if f not in features]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
    
    def _prepare_training_data(self, data: pd.DataFrame, 
                             target_column: str) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Prepare training data.
        
        Args:
            data: Raw training data
            target_column: Target column name
            
        Returns:
            Tuple of (X, y) for training
        """
        # Get expected features
        expected_features = self._get_expected_features()
        
        # Select available feature columns
        available_features = [col for col in expected_features if col in data.columns]
        
        if not available_features:
            raise ValueError(f"No expected features found in data. "
                           f"Expected: {expected_features}, "
                           f"Available: {list(data.columns)}")
        
        X = data[available_features].copy()
        
        # Handle missing values
        X = X.fillna(0)
        
        # Target variable
        if target_column not in data.columns:
            raise ValueError(f"Target column '{target_column}' not found in data")
        
        y = data[target_column].values
        
        # Update feature names
        self.feature_names = available_features
        
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
        # Base confidence calculation
        feature_completeness = (features.notna().sum().sum()) / (len(features.columns))
        
        # Base confidence
        base_confidence = 0.7
        feature_bonus = feature_completeness * 0.2
        
        # Adjust based on prediction magnitude
        if prediction > 1000000:  # Very high prediction
            prediction_penalty = 0.15
        elif prediction < 10:  # Very low prediction
            prediction_penalty = 0.15
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
        # Default timeframe adjustment (can be overridden by subclasses)
        if timeframe <= 1:
            return prediction * 0.5
        elif timeframe <= 3:
            return prediction * 0.75
        elif timeframe <= 7:
            return prediction
        elif timeframe <= 30:
            return prediction * 1.3
        else:
            return prediction * 1.5
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate evaluation metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        # Avoid division by zero
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
