"""
Model Evaluation Script for ViewTrendsSL

This script provides comprehensive evaluation and analysis of trained models,
including performance metrics, feature importance, and prediction analysis.

Author: ViewTrendsSL Team
Date: 2025
"""

import os
import sys
import logging
import argparse
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from src.business.ml.models.shorts_model import ShortsModel
from src.business.ml.models.longform_model import LongFormModel
from src.business.ml.evaluation.evaluator import ModelEvaluator
from src.business.ml.training.data_loader import DataLoader
from src.business.ml.preprocessing.feature_pipeline import FeaturePipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelEvaluationSuite:
    """Comprehensive model evaluation and analysis suite."""
    
    def __init__(self, models_dir: str = 'models/trained', output_dir: str = 'models/evaluation'):
        """
        Initialize the evaluation suite.
        
        Args:
            models_dir: Directory containing trained models
            output_dir: Directory to save evaluation results
        """
        self.models_dir = Path(models_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.evaluator = ModelEvaluator()
        self.data_loader = DataLoader()
        self.feature_pipeline = FeaturePipeline()
        
        # Create subdirectories
        (self.output_dir / 'plots').mkdir(exist_ok=True)
        (self.output_dir / 'reports').mkdir(exist_ok=True)
        (self.output_dir / 'metrics').mkdir(exist_ok=True)
        
        logger.info(f"Evaluation suite initialized. Output: {self.output_dir}")
    
    def load_models(self) -> Dict[str, Any]:
        """
        Load trained models from the models directory.
        
        Returns:
            Dictionary containing loaded models
        """
        models = {}
        
        # Load Shorts model
        shorts_model_path = self.models_dir / 'shorts_model.joblib'
        if shorts_model_path.exists():
            try:
                shorts_model = ShortsModel()
                shorts_model.load_model(str(shorts_model_path))
                models['shorts'] = shorts_model
                logger.info("Loaded Shorts model")
            except Exception as e:
                logger.error(f"Error loading Shorts model: {e}")
        
        # Load Long-form model
        longform_model_path = self.models_dir / 'longform_model.joblib'
        if longform_model_path.exists():
            try:
                longform_model = LongFormModel()
                longform_model.load_model(str(longform_model_path))
                models['longform'] = longform_model
                logger.info("Loaded Long-form model")
            except Exception as e:
                logger.error(f"Error loading Long-form model: {e}")
        
        if not models:
            raise ValueError("No trained models found. Please train models first.")
        
        return models
    
    def load_test_data(self, data_path: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Load and prepare test data.
        
        Args:
            data_path: Path to test data CSV
            
        Returns:
            Tuple of (shorts_data, longform_data)
        """
        logger.info(f"Loading test data from {data_path}")
        
        # Load raw data
        raw_data = self.data_loader.load_training_data(data_path)
        
        if raw_data is None or raw_data.empty:
            raise ValueError(f"No test data found at {data_path}")
        
        # Separate by video type
        shorts_data = raw_data[raw_data['is_short'] == True].copy()
        longform_data = raw_data[raw_data['is_short'] == False].copy()
        
        logger.info(f"Test data - Shorts: {len(shorts_data)}, Long-form: {len(longform_data)}")
        
        # Process features
        shorts_processed = None
        longform_processed = None
        
        if len(shorts_data) > 0:
            shorts_processed = self.feature_pipeline.process_features(
                shorts_data, video_type='shorts'
            )
        
        if len(longform_data) > 0:
            longform_processed = self.feature_pipeline.process_features(
                longform_data, video_type='longform'
            )
        
        return shorts_processed, longform_processed
    
    def evaluate_model_performance(
        self, 
        model: Any, 
        test_data: Dict[str, Any], 
        model_type: str
    ) -> Dict[str, Any]:
        """
        Evaluate model performance on test data.
        
        Args:
            model: Trained model instance
            test_data: Test dataset
            model_type: Type of model ('shorts' or 'longform')
            
        Returns:
            Dictionary with evaluation results
        """
        logger.info(f"Evaluating {model_type} model performance...")
        
        # Basic evaluation
        evaluation_results = self.evaluator.evaluate_model(
            model=model,
            X_test=test_data['X_test'],
            y_test=test_data['y_test'],
            model_type=model_type
        )
        
        # Additional analysis
        y_pred = model.predict(test_data['X_test'])
        
        # Prediction analysis
        prediction_analysis = self._analyze_predictions(
            y_true=test_data['y_test'],
            y_pred=y_pred,
            model_type=model_type
        )
        
        # Feature importance
        feature_importance = self._get_feature_importance(
            model=model,
            feature_names=test_data.get('feature_names', []),
            model_type=model_type
        )
        
        # Combine results
        complete_results = {
            'model_type': model_type,
            'test_samples': len(test_data['X_test']),
            'evaluation_metrics': evaluation_results,
            'prediction_analysis': prediction_analysis,
            'feature_importance': feature_importance,
            'evaluated_at': datetime.now().isoformat()
        }
        
        return complete_results
    
    def _analyze_predictions(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        model_type: str
    ) -> Dict[str, Any]:
        """Analyze prediction patterns and errors."""
        
        # Calculate residuals
        residuals = y_true - y_pred
        
        # Percentage errors
        percentage_errors = np.abs(residuals) / np.maximum(y_true, 1) * 100
        
        # Prediction ranges
        pred_ranges = {
            'low': np.sum(y_pred < 1000),
            'medium': np.sum((y_pred >= 1000) & (y_pred < 10000)),
            'high': np.sum((y_pred >= 10000) & (y_pred < 100000)),
            'very_high': np.sum(y_pred >= 100000)
        }
        
        # Error analysis by prediction range
        error_by_range = {}
        for range_name, mask in [
            ('low', y_pred < 1000),
            ('medium', (y_pred >= 1000) & (y_pred < 10000)),
            ('high', (y_pred >= 10000) & (y_pred < 100000)),
            ('very_high', y_pred >= 100000)
        ]:
            if np.sum(mask) > 0:
                range_errors = percentage_errors[mask]
                error_by_range[range_name] = {
                    'count': int(np.sum(mask)),
                    'mean_error': float(np.mean(range_errors)),
                    'median_error': float(np.median(range_errors)),
                    'std_error': float(np.std(range_errors))
                }
        
        analysis = {
            'residual_stats': {
                'mean': float(np.mean(residuals)),
                'std': float(np.std(residuals)),
                'min': float(np.min(residuals)),
                'max': float(np.max(residuals))
            },
            'percentage_error_stats': {
                'mean': float(np.mean(percentage_errors)),
                'median': float(np.median(percentage_errors)),
                'std': float(np.std(percentage_errors)),
                'q25': float(np.percentile(percentage_errors, 25)),
                'q75': float(np.percentile(percentage_errors, 75))
            },
            'prediction_ranges': pred_ranges,
            'error_by_range': error_by_range,
            'correlation': float(np.corrcoef(y_true, y_pred)[0, 1])
        }
        
        # Create prediction plots
        self._create_prediction_plots(y_true, y_pred, residuals, model_type)
        
        return analysis
    
    def _get_feature_importance(
        self, 
        model: Any, 
        feature_names: List[str], 
        model_type: str
    ) -> Dict[str, Any]:
        """Extract and analyze feature importance."""
        
        try:
            # Get feature importance from model
            if hasattr(model.model, 'feature_importances_'):
                importances = model.model.feature_importances_
            elif hasattr(model.model, 'coef_'):
                importances = np.abs(model.model.coef_)
            else:
                logger.warning(f"Cannot extract feature importance for {model_type} model")
                return {}
            
            # Create importance dataframe
            if len(feature_names) == len(importances):
                importance_df = pd.DataFrame({
                    'feature': feature_names,
                    'importance': importances
                }).sort_values('importance', ascending=False)
                
                # Top features
                top_features = importance_df.head(10).to_dict('records')
                
                # Create feature importance plot
                self._create_feature_importance_plot(importance_df, model_type)
                
                return {
                    'top_features': top_features,
                    'total_features': len(feature_names),
                    'importance_sum': float(np.sum(importances))
                }
            else:
                logger.warning(f"Feature names length mismatch for {model_type} model")
                return {}
                
        except Exception as e:
            logger.error(f"Error extracting feature importance: {e}")
            return {}
    
    def _create_prediction_plots(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        residuals: np.ndarray, 
        model_type: str
    ):
        """Create prediction analysis plots."""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'{model_type.title()} Model - Prediction Analysis', fontsize=16)
        
        # Actual vs Predicted
        axes[0, 0].scatter(y_true, y_pred, alpha=0.6)
        axes[0, 0].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
        axes[0, 0].set_xlabel('Actual Views')
        axes[0, 0].set_ylabel('Predicted Views')
        axes[0, 0].set_title('Actual vs Predicted')
        axes[0, 0].set_xscale('log')
        axes[0, 0].set_yscale('log')
        
        # Residuals vs Predicted
        axes[0, 1].scatter(y_pred, residuals, alpha=0.6)
        axes[0, 1].axhline(y=0, color='r', linestyle='--')
        axes[0, 1].set_xlabel('Predicted Views')
        axes[0, 1].set_ylabel('Residuals')
        axes[0, 1].set_title('Residuals vs Predicted')
        axes[0, 1].set_xscale('log')
        
        # Residuals histogram
        axes[1, 0].hist(residuals, bins=50, alpha=0.7)
        axes[1, 0].set_xlabel('Residuals')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Residuals Distribution')
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot (Residuals)')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'plots' / f'{model_type}_prediction_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved prediction analysis plots for {model_type} model")
    
    def _create_feature_importance_plot(self, importance_df: pd.DataFrame, model_type: str):
        """Create feature importance plot."""
        
        plt.figure(figsize=(12, 8))
        
        # Top 15 features
        top_features = importance_df.head(15)
        
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Feature Importance')
        plt.title(f'{model_type.title()} Model - Top Feature Importance')
        plt.gca().invert_yaxis()
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'plots' / f'{model_type}_feature_importance.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved feature importance plot for {model_type} model")
    
    def generate_comparison_report(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a comparison report between models."""
        
        logger.info("Generating model comparison report...")
        
        comparison = {
            'models_compared': list(results.keys()),
            'comparison_metrics': {},
            'performance_summary': {},
            'recommendations': []
        }
        
        # Extract key metrics for comparison
        for model_type, result in results.items():
            metrics = result['evaluation_metrics']
            comparison['performance_summary'][model_type] = {
                'mape': metrics.get('mape', 'N/A'),
                'rmse': metrics.get('rmse', 'N/A'),
                'mae': metrics.get('mae', 'N/A'),
                'r2_score': metrics.get('r2_score', 'N/A'),
                'test_samples': result['test_samples']
            }
        
        # Generate recommendations
        if 'shorts' in results and 'longform' in results:
            shorts_mape = results['shorts']['evaluation_metrics'].get('mape', float('inf'))
            longform_mape = results['longform']['evaluation_metrics'].get('mape', float('inf'))
            
            if shorts_mape < 30:
                comparison['recommendations'].append("Shorts model shows good performance (MAPE < 30%)")
            elif shorts_mape < 50:
                comparison['recommendations'].append("Shorts model shows acceptable performance (MAPE < 50%)")
            else:
                comparison['recommendations'].append("Shorts model needs improvement (MAPE >= 50%)")
            
            if longform_mape < 30:
                comparison['recommendations'].append("Long-form model shows good performance (MAPE < 30%)")
            elif longform_mape < 50:
                comparison['recommendations'].append("Long-form model shows acceptable performance (MAPE < 50%)")
            else:
                comparison['recommendations'].append("Long-form model needs improvement (MAPE >= 50%)")
        
        return comparison
    
    def run_complete_evaluation(self, test_data_path: str) -> Dict[str, Any]:
        """
        Run complete evaluation suite.
        
        Args:
            test_data_path: Path to test data
            
        Returns:
            Complete evaluation results
        """
        logger.info("Starting complete model evaluation...")
        
        try:
            # Load models
            models = self.load_models()
            
            # Load test data
            shorts_data, longform_data = self.load_test_data(test_data_path)
            
            # Evaluate each model
            results = {}
            
            if 'shorts' in models and shorts_data is not None:
                results['shorts'] = self.evaluate_model_performance(
                    model=models['shorts'],
                    test_data=shorts_data,
                    model_type='shorts'
                )
            
            if 'longform' in models and longform_data is not None:
                results['longform'] = self.evaluate_model_performance(
                    model=models['longform'],
                    test_data=longform_data,
                    model_type='longform'
                )
            
            # Generate comparison report
            comparison_report = self.generate_comparison_report(results)
            
            # Compile final results
            final_results = {
                'evaluation_summary': {
                    'evaluated_at': datetime.now().isoformat(),
                    'models_evaluated': list(results.keys()),
                    'test_data_path': test_data_path
                },
                'model_results': results,
                'comparison_report': comparison_report
            }
            
            # Save results
            results_path = self.output_dir / 'evaluation_results.json'
            with open(results_path, 'w') as f:
                json.dump(final_results, f, indent=2, default=str)
            
            # Generate summary report
            self._generate_summary_report(final_results)
            
            logger.info("Complete evaluation finished successfully")
            return final_results
            
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            raise
    
    def _generate_summary_report(self, results: Dict[str, Any]):
        """Generate a human-readable summary report."""
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("VIEWTRENDSSL MODEL EVALUATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {results['evaluation_summary']['evaluated_at']}")
        report_lines.append(f"Models Evaluated: {', '.join(results['evaluation_summary']['models_evaluated'])}")
        report_lines.append("")
        
        # Model performance summary
        for model_type, model_results in results['model_results'].items():
            report_lines.append(f"{model_type.upper()} MODEL PERFORMANCE:")
            report_lines.append("-" * 40)
            
            metrics = model_results['evaluation_metrics']
            report_lines.append(f"Test Samples: {model_results['test_samples']}")
            report_lines.append(f"MAPE: {metrics.get('mape', 'N/A'):.2f}%")
            report_lines.append(f"RMSE: {metrics.get('rmse', 'N/A'):.2f}")
            report_lines.append(f"MAE: {metrics.get('mae', 'N/A'):.2f}")
            report_lines.append(f"R² Score: {metrics.get('r2_score', 'N/A'):.4f}")
            
            # Top features
            if 'feature_importance' in model_results and 'top_features' in model_results['feature_importance']:
                report_lines.append("\nTop 5 Important Features:")
                for i, feature in enumerate(model_results['feature_importance']['top_features'][:5], 1):
                    report_lines.append(f"  {i}. {feature['feature']}: {feature['importance']:.4f}")
            
            report_lines.append("")
        
        # Recommendations
        if 'recommendations' in results['comparison_report']:
            report_lines.append("RECOMMENDATIONS:")
            report_lines.append("-" * 40)
            for rec in results['comparison_report']['recommendations']:
                report_lines.append(f"• {rec}")
            report_lines.append("")
        
        report_lines.append("=" * 80)
        
        # Save report
        report_path = self.output_dir / 'reports' / 'evaluation_summary.txt'
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))
        
        # Also log to console
        for line in report_lines:
            logger.info(line)


def main():
    """Main evaluation script entry point."""
    parser = argparse.ArgumentParser(description='Evaluate ViewTrendsSL prediction models')
    
    parser.add_argument(
        '--test-data', 
        type=str, 
        required=True,
        help='Path to test data CSV file'
    )
    
    parser.add_argument(
        '--models-dir', 
        type=str, 
        default='models/trained',
        help='Directory containing trained models'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default='models/evaluation',
        help='Directory to save evaluation results'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate test data exists
        if not os.path.exists(args.test_data):
            logger.error(f"Test data not found: {args.test_data}")
            return 1
        
        # Initialize evaluation suite
        evaluator = ModelEvaluationSuite(
            models_dir=args.models_dir,
            output_dir=args.output_dir
        )
        
        # Run evaluation
        results = evaluator.run_complete_evaluation(args.test_data)
        
        # Check if evaluation was successful
        if results['model_results']:
            logger.info("Model evaluation completed successfully!")
            logger.info(f"Results saved to: {args.output_dir}")
            return 0
        else:
            logger.error("No models were successfully evaluated")
            return 1
            
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
