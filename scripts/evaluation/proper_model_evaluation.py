#!/usr/bin/env python3
"""
Proper Model Evaluation Script for ViewTrendsSL

This script is MODIFIED to be compatible with the 'at-upload' training pipeline.

Author: ViewTrendsSL Team
Date: 2025
"""

import pandas as pd
import numpy as np
import joblib
import json
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error, handling edge cases."""
    mask = y_true > 1
    if mask.sum() == 0:
        return float('inf')
    
    y_true_filtered = y_true[mask]
    y_pred_filtered = y_pred[mask]
    
    return np.mean(np.abs((y_true_filtered - y_pred_filtered) / y_true_filtered)) * 100

# --- MODIFIED FUNCTION ---
def prepare_at_upload_features_and_targets(df, feature_info):
    """
    Prepares features and targets specifically for the 'at-upload' models.
    This reuses the exact same feature selection logic as the training script.
    """
    logger.info("Preparing features and targets for 'at-upload' models...")
    
    # 1. Define the explicit list of METADATA-ONLY features using feature_info.json
    METADATA_FEATURES = [
        col for col in feature_info.get('content_features', [])
        if col in df.columns
    ] + [
        col for col in feature_info.get('channel_features', [])
        if col in df.columns
    ]
    leaky_patterns = ['view', 'like', 'comment', 'growth', 'velocity', 'peak', 'consistency', 'ratio']
    METADATA_FEATURES = [
        f for f in METADATA_FEATURES 
        if not any(leak in f for leak in leaky_patterns)
    ]
    
    # Add 'is_short' which is critical for splitting but might not be in the lists
    if 'is_short' in df.columns and 'is_short' not in METADATA_FEATURES:
        METADATA_FEATURES.append('is_short')

    features_df = df[METADATA_FEATURES].copy()
    logger.info(f"Selected {len(features_df.columns)} metadata-only features.")

    # 2. Prepare targets
    target_columns = ['views_at_24h', 'views_at_7d', 'views_at_30d']
    targets = {}
    for target in target_columns:
        if target in df.columns:
            targets[target] = df[target].copy().fillna(0).clip(lower=0)
            
    return features_df, targets

def evaluate_model_properly(model_path, X_test, y_test, model_name):
    """
    Evaluate a single model properly.
    (This function remains unchanged, it's already good)
    """
    try:
        model = joblib.load(model_path)
        
        # --- FIX: Ensure columns are in the same order as during training ---
        # The preprocessor inside the pipeline handles this, but it's good practice
        # to ensure the DataFrame passed to it is consistent.
        if hasattr(model.named_steps['preprocessor'], 'feature_names_in_'):
             X_test = X_test[model.named_steps['preprocessor'].feature_names_in_]

        # The model expects log-transformed predictions, so we must inverse transform
        y_pred_log = model.predict(X_test)
        y_pred = np.expm1(y_pred_log)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mape = calculate_mape(y_test, y_pred)
        
        metrics = {
            'model_name': model_name, 'mae': mae, 'rmse': rmse, 'r2': r2, 'mape': mape
        }
        return metrics
        
    except Exception as e:
        logger.error(f"Error evaluating {model_name}: {e}")
        return None

# --- MODIFIED FUNCTION ---
def main():
    """Main evaluation function."""
    logger.info("Starting 'at-upload' model evaluation...")
    
    # Load test data and the crucial feature_info JSON
    try:
        test_data = pd.read_csv('data/processed/validation/val_data.csv') # Use validation data for consistency
        with open('data/processed/features/feature_info.json', 'r') as f:
            feature_info = json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Required file not found: {e}. Please run the processing script first.")
        return

    # Prepare features and targets using the unified logic
    X_test, y_test = prepare_at_upload_features_and_targets(test_data, feature_info)
    
    shorts_mask = X_test['is_short'] == True
    longform_mask = X_test['is_short'] == False
    
    X_test_shorts = X_test[shorts_mask]
    X_test_longform = X_test[longform_mask]
    
    model_dir = Path('models')
    results = []
    
    for target_name, target_series in y_test.items():
        logger.info(f"\n=== Evaluating models for {target_name} ===")
        
        # Shorts model - Use the CORRECT filename
        shorts_model_path = model_dir / f'at_upload_shorts_{target_name}_model.joblib'
        if shorts_model_path.exists() and not X_test_shorts.empty:
            metrics = evaluate_model_properly(
                shorts_model_path, X_test_shorts, target_series[shorts_mask], f'Shorts_{target_name}'
            )
            if metrics:
                results.append(metrics)
                logger.info(f"Shorts {target_name} - MAPE: {metrics['mape']:.2f}%, R²: {metrics['r2']:.4f}")

        # Long-form model - Use the CORRECT filename
        longform_model_path = model_dir / f'at_upload_longform_{target_name}_model.joblib'
        if longform_model_path.exists() and not X_test_longform.empty:
            metrics = evaluate_model_properly(
                longform_model_path, X_test_longform, target_series[longform_mask], f'Longform_{target_name}'
            )
            if metrics:
                results.append(metrics)
                logger.info(f"Long-form {target_name} - MAPE: {metrics['mape']:.2f}%, R²: {metrics['r2']:.4f}")
    
    # Print and save results
    print("\n" + "="*80 + "\nAT-UPLOAD MODEL EVALUATION RESULTS\n" + "="*80)
    if results:
        results_df = pd.DataFrame(results)
        print(results_df.to_string(index=False))
        results_df.to_csv('results/at_upload_evaluation_results.csv', index=False)
        logger.info("Evaluation results saved to results/at_upload_evaluation_results.csv")
    else:
        print("No valid evaluation results obtained. Check if models exist and test data is available.")
    print("="*80)

if __name__ == '__main__':
    main()