#!/usr/bin/env python3
"""
Proper Model Evaluation Script for ViewTrendsSL

This script performs proper evaluation of the trained models by:
1. Removing data leakage (excluding raw time-series columns from features)
2. Using proper target variables
3. Calculating meaningful MAPE scores

Author: ViewTrendsSL Team
Date: 2025
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error, handling edge cases."""
    # Avoid division by zero and very small values
    mask = y_true > 1  # Only calculate MAPE for videos with > 1 view
    if mask.sum() == 0:
        return float('inf')
    
    y_true_filtered = y_true[mask]
    y_pred_filtered = y_pred[mask]
    
    return np.mean(np.abs((y_true_filtered - y_pred_filtered) / y_true_filtered)) * 100

def prepare_clean_features_and_targets(df):
    """
    Prepare features and targets WITHOUT data leakage.
    
    Args:
        df: Raw processed DataFrame
        
    Returns:
        Tuple of (features_df, targets_dict)
    """
    logger.info("Preparing clean features and targets (removing data leakage)...")
    
    # Define target columns - these should be our prediction targets
    target_columns = ['views_at_24h', 'views_at_7d', 'views_at_30d']
    
    # CRITICAL: Remove ALL raw time-series columns to prevent data leakage
    time_series_raw_cols = [col for col in df.columns if 
                           col.startswith('day_') and 
                           (col.endswith('_views') or col.endswith('_likes') or col.endswith('_comments'))]
    
    # Also exclude other non-feature columns
    exclude_columns = target_columns + time_series_raw_cols + [
        'video_id', 'channel_id', 'title', 'description', 'tags',
        'published_at', 'inserted_at', 'localized_title', 'localized_description',
        'thumbnail_default', 'thumbnail_medium', 'thumbnail_high',
        'default_language', 'default_audio_language', 'live_broadcast_content'
    ]
    
    logger.info(f"Excluding {len(time_series_raw_cols)} raw time-series columns to prevent data leakage")
    logger.info(f"Raw time-series columns: {time_series_raw_cols[:5]}...")
    
    # Prepare clean features
    feature_columns = [col for col in df.columns if col not in exclude_columns]
    features_df = df[feature_columns].copy()
    
    # Prepare targets with proper handling
    targets = {}
    for target in target_columns:
        if target in df.columns:
            target_series = df[target].copy()
            # Handle NaN and infinite values
            target_series = target_series.fillna(0)
            target_series = target_series.replace([np.inf, -np.inf], 0)
            target_series = target_series.clip(lower=0)
            targets[target] = target_series
    
    logger.info(f"Clean features: {len(feature_columns)} columns")
    logger.info(f"Available targets: {list(targets.keys())}")
    
    # Check for remaining data leakage
    potential_leakage = [col for col in feature_columns if 'day_' in col and ('view' in col or 'like' in col or 'comment' in col)]
    if potential_leakage:
        logger.warning(f"Potential data leakage detected in features: {potential_leakage}")
    
    return features_df, targets

def evaluate_model_properly(model_path, X_test, y_test, model_name):
    """
    Evaluate a single model properly.
    
    Args:
        model_path: Path to the saved model
        X_test: Test features
        y_test: Test targets
        model_name: Name of the model for logging
        
    Returns:
        Dictionary of evaluation metrics
    """
    try:
        # Load model
        model = joblib.load(model_path)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        mape = calculate_mape(y_test, y_pred)
        
        # Additional metrics
        median_ae = np.median(np.abs(y_test - y_pred))
        mean_pred = np.mean(y_pred)
        mean_actual = np.mean(y_test)
        
        metrics = {
            'model_name': model_name,
            'test_samples': len(X_test),
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'mape': mape,
            'median_ae': median_ae,
            'mean_prediction': mean_pred,
            'mean_actual': mean_actual,
            'prediction_bias': mean_pred - mean_actual
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error evaluating {model_name}: {e}")
        return None

def main():
    """Main evaluation function."""
    logger.info("Starting proper model evaluation...")
    
    # Load test data
    test_data = pd.read_csv('data/processed/test_data.csv')
    logger.info(f"Loaded test data: {test_data.shape}")
    
    # Prepare clean features and targets
    X_test, y_test = prepare_clean_features_and_targets(test_data)
    
    # Split by content type
    shorts_mask = X_test['is_short'] == True
    longform_mask = X_test['is_short'] == False
    
    X_test_shorts = X_test[shorts_mask]
    X_test_longform = X_test[longform_mask]
    
    logger.info(f"Test samples - Shorts: {len(X_test_shorts)}, Long-form: {len(X_test_longform)}")
    
    # Model paths
    model_dir = Path('models')
    
    # Evaluate all models
    results = []
    
    for target_name, target_series in y_test.items():
        logger.info(f"\n=== Evaluating models for {target_name} ===")
        
        # Check if target has valid data
        valid_data_count = (target_series > 0).sum()
        logger.info(f"Valid data points for {target_name}: {valid_data_count}")
        
        if valid_data_count < 10:
            logger.warning(f"Insufficient valid data for {target_name}, skipping...")
            continue
        
        # Shorts model
        shorts_model_path = model_dir / f'shorts_{target_name}_model.joblib'
        if shorts_model_path.exists() and len(X_test_shorts) > 0:
            y_test_shorts = target_series[shorts_mask]
            valid_shorts = (y_test_shorts > 0).sum()
            
            if valid_shorts >= 5:
                metrics = evaluate_model_properly(
                    shorts_model_path, X_test_shorts, y_test_shorts, 
                    f'Shorts_{target_name}'
                )
                if metrics:
                    results.append(metrics)
                    logger.info(f"Shorts {target_name} - MAPE: {metrics['mape']:.2f}%, R²: {metrics['r2']:.4f}")
            else:
                logger.warning(f"Insufficient valid Shorts data for {target_name}: {valid_shorts}")
        
        # Long-form model
        longform_model_path = model_dir / f'longform_{target_name}_model.joblib'
        if longform_model_path.exists() and len(X_test_longform) > 0:
            y_test_longform = target_series[longform_mask]
            valid_longform = (y_test_longform > 0).sum()
            
            if valid_longform >= 5:
                metrics = evaluate_model_properly(
                    longform_model_path, X_test_longform, y_test_longform,
                    f'Longform_{target_name}'
                )
                if metrics:
                    results.append(metrics)
                    logger.info(f"Long-form {target_name} - MAPE: {metrics['mape']:.2f}%, R²: {metrics['r2']:.4f}")
            else:
                logger.warning(f"Insufficient valid Long-form data for {target_name}: {valid_longform}")
    
    # Print comprehensive results
    print("\n" + "="*80)
    print("PROPER MODEL EVALUATION RESULTS")
    print("="*80)
    
    if results:
        for result in results:
            print(f"\n{result['model_name']}:")
            print(f"  Test Samples: {result['test_samples']:,}")
            print(f"  MAPE: {result['mape']:.2f}%")
            print(f"  R²: {result['r2']:.4f}")
            print(f"  RMSE: {result['rmse']:.2f}")
            print(f"  MAE: {result['mae']:.2f}")
            print(f"  Mean Actual: {result['mean_actual']:.2f}")
            print(f"  Mean Predicted: {result['mean_prediction']:.2f}")
            print(f"  Prediction Bias: {result['prediction_bias']:.2f}")
    else:
        print("No valid evaluation results obtained.")
    
    print("\n" + "="*80)
    
    # Save results
    if results:
        results_df = pd.DataFrame(results)
        results_df.to_csv('results/proper_evaluation_results.csv', index=False)
        logger.info("Evaluation results saved to results/proper_evaluation_results.csv")
    
    return results

if __name__ == '__main__':
    main()
