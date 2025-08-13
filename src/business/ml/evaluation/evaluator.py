"""
Model Evaluation Utilities for ViewTrendsSL

This module provides comprehensive evaluation capabilities for ML models,
including metrics calculation, visualization, and performance analysis.

Author: ViewTrendsSL Team
Date: 2025
"""

import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json

from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    mean_absolute_percentage_error
)

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Comprehensive model evaluation utilities."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model evaluator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or self._get_default_config()
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        logger.info("ModelEvaluator initialized")
    
    def evaluate_predictions(self, 
                           y_true: np.ndarray, 
                           y_pred: np.ndarray,
                           model_name: str = "Model") -> Dict[str, Any]:
        """
        Evaluate model predictions with comprehensive metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            model_name: Name of the model being evaluated
            
        Returns:
            Dictionary with evaluation metrics
        """
        try:
            logger.info(f"Evaluating {model_name} predictions")
            
            # Basic metrics
            mae = mean_absolute_error(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_true, y_pred)
            
            # MAPE with protection against division by zero
            mape = np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100
            
            # Additional metrics
            median_ae = np.median(np.abs(y_true - y_pred))
            max_error = np.max(np.abs(y_true - y_pred))
            
            # Percentage of predictions within certain error bounds
            error_percentages = self._calculate_error_percentages(y_true, y_pred)
            
            # Prediction distribution analysis
            distribution_stats = self._analyze_prediction_distribution(y_true, y_pred)
            
            # Performance by prediction magnitude
            magnitude_analysis = self._analyze_by_magnitude(y_true, y_pred)
            
            results = {
                'model_name': model_name,
                'sample_count': len(y_true),
                'basic_metrics': {
                    'mae': float(mae),
                    'mse': float(mse),
                    'rmse': float(rmse),
                    'r2_score': float(r2),
                    'mape': float(mape),
                    'median_absolute_error': float(median_ae),
                    'max_error': float(max_error)
                },
                'error_percentages': error_percentages,
                'distribution_stats': distribution_stats,
                'magnitude_analysis': magnitude_analysis,
                'evaluated_at': datetime.now().isoformat()
            }
            
            logger.info(f"{model_name} evaluation completed - R²: {r2:.4f}, MAPE: {mape:.2f}%")
            
            return results
            
        except Exception as e:
            logger.error(f"Error evaluating {model_name}: {str(e)}")
            raise
    
    def compare_models(self, 
                      evaluations: List[Dict[str, Any]],
                      save_plots: bool = True) -> Dict[str, Any]:
        """
        Compare multiple model evaluations.
        
        Args:
            evaluations: List of evaluation results from evaluate_predictions
            save_plots: Whether to save comparison plots
            
        Returns:
            Model comparison results
        """
        try:
            logger.info(f"Comparing {len(evaluations)} models")
            
            if len(evaluations) < 2:
                raise ValueError("Need at least 2 models for comparison")
            
            # Extract metrics for comparison
            comparison_data = []
            for eval_result in evaluations:
                model_data = {
                    'model_name': eval_result['model_name'],
                    'sample_count': eval_result['sample_count'],
                    **eval_result['basic_metrics']
                }
                comparison_data.append(model_data)
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Rank models by different metrics
            rankings = self._rank_models(comparison_df)
            
            # Statistical significance tests
            significance_tests = self._perform_significance_tests(evaluations)
            
            # Generate comparison plots
            plots_info = {}
            if save_plots:
                plots_info = self._create_comparison_plots(comparison_df, evaluations)
            
            results = {
                'comparison_summary': comparison_df.to_dict('records'),
                'rankings': rankings,
                'significance_tests': significance_tests,
                'plots': plots_info,
                'best_model': rankings['overall']['best_model'],
                'compared_at': datetime.now().isoformat()
            }
            
            logger.info(f"Model comparison completed. Best model: {rankings['overall']['best_model']}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error comparing models: {str(e)}")
            raise
    
    def analyze_residuals(self, 
                         y_true: np.ndarray, 
                         y_pred: np.ndarray,
                         model_name: str = "Model",
                         save_plots: bool = True) -> Dict[str, Any]:
        """
        Analyze model residuals for diagnostic purposes.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            model_name: Name of the model
            save_plots: Whether to save residual plots
            
        Returns:
            Residual analysis results
        """
        try:
            logger.info(f"Analyzing residuals for {model_name}")
            
            residuals = y_true - y_pred
            
            # Basic residual statistics
            residual_stats = {
                'mean': float(np.mean(residuals)),
                'std': float(np.std(residuals)),
                'median': float(np.median(residuals)),
                'min': float(np.min(residuals)),
                'max': float(np.max(residuals)),
                'skewness': float(self._calculate_skewness(residuals)),
                'kurtosis': float(self._calculate_kurtosis(residuals))
            }
            
            # Normality tests
            normality_tests = self._test_residual_normality(residuals)
            
            # Heteroscedasticity analysis
            heteroscedasticity = self._analyze_heteroscedasticity(y_pred, residuals)
            
            # Outlier detection
            outliers = self._detect_outliers(residuals, y_true, y_pred)
            
            # Generate residual plots
            plots_info = {}
            if save_plots:
                plots_info = self._create_residual_plots(y_true, y_pred, residuals, model_name)
            
            results = {
                'model_name': model_name,
                'residual_stats': residual_stats,
                'normality_tests': normality_tests,
                'heteroscedasticity': heteroscedasticity,
                'outliers': outliers,
                'plots': plots_info,
                'analyzed_at': datetime.now().isoformat()
            }
            
            logger.info(f"Residual analysis completed for {model_name}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing residuals: {str(e)}")
            raise
    
    def evaluate_feature_importance(self, 
                                  feature_importance: Dict[str, float],
                                  feature_groups: Optional[Dict[str, List[str]]] = None,
                                  save_plots: bool = True) -> Dict[str, Any]:
        """
        Analyze and visualize feature importance.
        
        Args:
            feature_importance: Dictionary of feature names and importance scores
            feature_groups: Optional grouping of features by type
            save_plots: Whether to save importance plots
            
        Returns:
            Feature importance analysis results
        """
        try:
            logger.info("Analyzing feature importance")
            
            if not feature_importance:
                return {'error': 'No feature importance data provided'}
            
            # Sort features by importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            # Top and bottom features
            top_features = sorted_features[:20]  # Top 20
            bottom_features = sorted_features[-10:]  # Bottom 10
            
            # Group analysis if groups provided
            group_analysis = {}
            if feature_groups:
                group_analysis = self._analyze_feature_groups(feature_importance, feature_groups)
            
            # Feature importance statistics
            importance_values = list(feature_importance.values())
            importance_stats = {
                'total_features': len(feature_importance),
                'mean_importance': float(np.mean(importance_values)),
                'std_importance': float(np.std(importance_values)),
                'max_importance': float(np.max(importance_values)),
                'min_importance': float(np.min(importance_values)),
                'top_10_cumulative': float(sum([imp for _, imp in sorted_features[:10]]))
            }
            
            # Generate importance plots
            plots_info = {}
            if save_plots:
                plots_info = self._create_importance_plots(
                    feature_importance, feature_groups, top_features
                )
            
            results = {
                'importance_stats': importance_stats,
                'top_features': top_features,
                'bottom_features': bottom_features,
                'group_analysis': group_analysis,
                'plots': plots_info,
                'analyzed_at': datetime.now().isoformat()
            }
            
            logger.info(f"Feature importance analysis completed for {len(feature_importance)} features")
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing feature importance: {str(e)}")
            raise
    
    def generate_evaluation_report(self, 
                                 evaluation_results: Dict[str, Any],
                                 output_path: str = "reports/evaluation_report.html") -> bool:
        """
        Generate a comprehensive HTML evaluation report.
        
        Args:
            evaluation_results: Combined evaluation results
            output_path: Path to save the HTML report
            
        Returns:
            True if report generated successfully
        """
        try:
            logger.info("Generating evaluation report")
            
            # Create output directory
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate HTML report
            html_content = self._generate_html_report(evaluation_results)
            
            # Save report
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Evaluation report saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating evaluation report: {str(e)}")
            return False
    
    # Private helper methods
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'plots': {
                'figsize': (10, 6),
                'dpi': 300,
                'format': 'png',
                'save_dir': 'plots/evaluation'
            },
            'metrics': {
                'error_thresholds': [0.1, 0.2, 0.3, 0.5],  # For error percentage analysis
                'magnitude_bins': [0, 1000, 10000, 100000, float('inf')]  # View count bins
            }
        }
    
    def _calculate_error_percentages(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate percentage of predictions within error thresholds."""
        
        relative_errors = np.abs((y_true - y_pred) / np.maximum(y_true, 1))
        
        error_percentages = {}
        for threshold in self.config['metrics']['error_thresholds']:
            within_threshold = np.sum(relative_errors <= threshold) / len(relative_errors) * 100
            error_percentages[f'within_{int(threshold*100)}pct'] = float(within_threshold)
        
        return error_percentages
    
    def _analyze_prediction_distribution(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Analyze the distribution of predictions vs actual values."""
        
        return {
            'actual_stats': {
                'mean': float(np.mean(y_true)),
                'std': float(np.std(y_true)),
                'median': float(np.median(y_true)),
                'min': float(np.min(y_true)),
                'max': float(np.max(y_true))
            },
            'predicted_stats': {
                'mean': float(np.mean(y_pred)),
                'std': float(np.std(y_pred)),
                'median': float(np.median(y_pred)),
                'min': float(np.min(y_pred)),
                'max': float(np.max(y_pred))
            },
            'correlation': float(np.corrcoef(y_true, y_pred)[0, 1])
        }
    
    def _analyze_by_magnitude(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Analyze performance by prediction magnitude."""
        
        bins = self.config['metrics']['magnitude_bins']
        bin_labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins)-1)]
        bin_labels[-1] = f'{bins[-2]}+'
        
        magnitude_analysis = {}
        
        for i, (low, high) in enumerate(zip(bins[:-1], bins[1:])):
            if high == float('inf'):
                mask = y_true >= low
            else:
                mask = (y_true >= low) & (y_true < high)
            
            if np.sum(mask) > 0:
                y_true_bin = y_true[mask]
                y_pred_bin = y_pred[mask]
                
                mae_bin = mean_absolute_error(y_true_bin, y_pred_bin)
                mape_bin = np.mean(np.abs((y_true_bin - y_pred_bin) / np.maximum(y_true_bin, 1))) * 100
                
                magnitude_analysis[bin_labels[i]] = {
                    'count': int(np.sum(mask)),
                    'mae': float(mae_bin),
                    'mape': float(mape_bin)
                }
        
        return magnitude_analysis
    
    def _rank_models(self, comparison_df: pd.DataFrame) -> Dict[str, Any]:
        """Rank models by different metrics."""
        
        rankings = {}
        
        # Rank by individual metrics (lower is better for error metrics, higher for R²)
        error_metrics = ['mae', 'rmse', 'mape']
        performance_metrics = ['r2_score']
        
        for metric in error_metrics:
            if metric in comparison_df.columns:
                ranked = comparison_df.nsmallest(len(comparison_df), metric)
                rankings[metric] = ranked[['model_name', metric]].to_dict('records')
        
        for metric in performance_metrics:
            if metric in comparison_df.columns:
                ranked = comparison_df.nlargest(len(comparison_df), metric)
                rankings[metric] = ranked[['model_name', metric]].to_dict('records')
        
        # Overall ranking (weighted combination)
        if 'r2_score' in comparison_df.columns and 'mape' in comparison_df.columns:
            # Normalize metrics and create composite score
            comparison_df['r2_normalized'] = (comparison_df['r2_score'] - comparison_df['r2_score'].min()) / (comparison_df['r2_score'].max() - comparison_df['r2_score'].min())
            comparison_df['mape_normalized'] = 1 - ((comparison_df['mape'] - comparison_df['mape'].min()) / (comparison_df['mape'].max() - comparison_df['mape'].min()))
            
            comparison_df['composite_score'] = 0.6 * comparison_df['r2_normalized'] + 0.4 * comparison_df['mape_normalized']
            
            overall_ranked = comparison_df.nlargest(len(comparison_df), 'composite_score')
            rankings['overall'] = {
                'ranking': overall_ranked[['model_name', 'composite_score']].to_dict('records'),
                'best_model': overall_ranked.iloc[0]['model_name']
            }
        
        return rankings
    
    def _perform_significance_tests(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform statistical significance tests between models."""
        
        # This is a placeholder for more sophisticated statistical tests
        # In a full implementation, you would perform paired t-tests, Wilcoxon tests, etc.
        
        return {
            'note': 'Statistical significance testing requires prediction residuals from each model',
            'recommendation': 'Implement paired statistical tests for robust model comparison'
        }
    
    def _create_comparison_plots(self, comparison_df: pd.DataFrame, evaluations: List[Dict[str, Any]]) -> Dict[str, str]:
        """Create model comparison plots."""
        
        plots_dir = Path(self.config['plots']['save_dir'])
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        plots_info = {}
        
        try:
            # Metrics comparison bar plot
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # R² Score
            if 'r2_score' in comparison_df.columns:
                axes[0, 0].bar(comparison_df['model_name'], comparison_df['r2_score'])
                axes[0, 0].set_title('R² Score Comparison')
                axes[0, 0].set_ylabel('R² Score')
                
            # MAPE
            if 'mape' in comparison_df.columns:
                axes[0, 1].bar(comparison_df['model_name'], comparison_df['mape'])
                axes[0, 1].set_title('MAPE Comparison')
                axes[0, 1].set_ylabel('MAPE (%)')
                
            # MAE
            if 'mae' in comparison_df.columns:
                axes[1, 0].bar(comparison_df['model_name'], comparison_df['mae'])
                axes[1, 0].set_title('MAE Comparison')
                axes[1, 0].set_ylabel('MAE')
                
            # RMSE
            if 'rmse' in comparison_df.columns:
                axes[1, 1].bar(comparison_df['model_name'], comparison_df['rmse'])
                axes[1, 1].set_title('RMSE Comparison')
                axes[1, 1].set_ylabel('RMSE')
            
            plt.tight_layout()
            
            comparison_plot_path = plots_dir / 'model_comparison.png'
            plt.savefig(comparison_plot_path, dpi=self.config['plots']['dpi'], bbox_inches='tight')
            plt.close()
            
            plots_info['comparison'] = str(comparison_plot_path)
            
        except Exception as e:
            logger.error(f"Error creating comparison plots: {str(e)}")
        
        return plots_info
    
    def _create_residual_plots(self, y_true: np.ndarray, y_pred: np.ndarray, 
                              residuals: np.ndarray, model_name: str) -> Dict[str, str]:
        """Create residual analysis plots."""
        
        plots_dir = Path(self.config['plots']['save_dir'])
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        plots_info = {}
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Residuals vs Predicted
            axes[0, 0].scatter(y_pred, residuals, alpha=0.6)
            axes[0, 0].axhline(y=0, color='r', linestyle='--')
            axes[0, 0].set_xlabel('Predicted Values')
            axes[0, 0].set_ylabel('Residuals')
            axes[0, 0].set_title('Residuals vs Predicted')
            
            # Q-Q plot (approximate)
            from scipy import stats
            stats.probplot(residuals, dist="norm", plot=axes[0, 1])
            axes[0, 1].set_title('Q-Q Plot')
            
            # Histogram of residuals
            axes[1, 0].hist(residuals, bins=30, alpha=0.7, edgecolor='black')
            axes[1, 0].set_xlabel('Residuals')
            axes[1, 0].set_ylabel('Frequency')
            axes[1, 0].set_title('Distribution of Residuals')
            
            # Actual vs Predicted
            axes[1, 1].scatter(y_true, y_pred, alpha=0.6)
            min_val = min(np.min(y_true), np.min(y_pred))
            max_val = max(np.max(y_true), np.max(y_pred))
            axes[1, 1].plot([min_val, max_val], [min_val, max_val], 'r--')
            axes[1, 1].set_xlabel('Actual Values')
            axes[1, 1].set_ylabel('Predicted Values')
            axes[1, 1].set_title('Actual vs Predicted')
            
            plt.suptitle(f'Residual Analysis - {model_name}')
            plt.tight_layout()
            
            residual_plot_path = plots_dir / f'residual_analysis_{model_name.lower().replace(" ", "_")}.png'
            plt.savefig(residual_plot_path, dpi=self.config['plots']['dpi'], bbox_inches='tight')
            plt.close()
            
            plots_info['residuals'] = str(residual_plot_path)
            
        except Exception as e:
            logger.error(f"Error creating residual plots: {str(e)}")
        
        return plots_info
    
    def _create_importance_plots(self, feature_importance: Dict[str, float], 
                               feature_groups: Optional[Dict[str, List[str]]], 
                               top_features: List[Tuple[str, float]]) -> Dict[str, str]:
        """Create feature importance plots."""
        
        plots_dir = Path(self.config['plots']['save_dir'])
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        plots_info = {}
        
        try:
            # Top features plot
            fig, ax = plt.subplots(figsize=(12, 8))
            
            features, importances = zip(*top_features)
            y_pos = np.arange(len(features))
            
            ax.barh(y_pos, importances)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(features)
            ax.invert_yaxis()
            ax.set_xlabel('Feature Importance')
            ax.set_title('Top 20 Feature Importance')
            
            plt.tight_layout()
            
            importance_plot_path = plots_dir / 'feature_importance.png'
            plt.savefig(importance_plot_path, dpi=self.config['plots']['dpi'], bbox_inches='tight')
            plt.close()
            
            plots_info['importance'] = str(importance_plot_path)
            
        except Exception as e:
            logger.error(f"Error creating importance plots: {str(e)}")
        
        return plots_info
    
    def _analyze_feature_groups(self, feature_importance: Dict[str, float], 
                               feature_groups: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyze feature importance by groups."""
        
        group_analysis = {}
        
        for group_name, features in feature_groups.items():
            group_importances = [feature_importance.get(feature, 0) for feature in features if feature in feature_importance]
            
            if group_importances:
                group_analysis[group_name] = {
                    'total_importance': float(sum(group_importances)),
                    'mean_importance': float(np.mean(group_importances)),
                    'feature_count': len(group_importances),
                    'top_feature': max([(f, feature_importance[f]) for f in features if f in feature_importance], 
                                     key=lambda x: x[1], default=('None', 0))
                }
        
        return group_analysis
    
    def _calculate_skewness(self, data: np.ndarray) -> float:
        """Calculate skewness of data."""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, data: np.ndarray) -> float:
        """Calculate kurtosis of data."""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std) ** 4) - 3
    
    def _test_residual_normality(self, residuals: np.ndarray) -> Dict[str, Any]:
        """Test residuals for normality."""
        try:
            from scipy import stats
            
            # Shapiro-Wilk test (for smaller samples)
            if len(residuals) <= 5000:
                shapiro_stat, shapiro_p = stats.shapiro(residuals)
                shapiro_result = {
                    'statistic': float(shapiro_stat),
                    'p_value': float(shapiro_p),
                    'is_normal': shapiro_p > 0.05
                }
            else:
                shapiro_result = {'note': 'Sample too large for Shapiro-Wilk test'}
            
            # Kolmogorov-Smirnov test
            ks_stat, ks_p = stats.kstest(residuals, 'norm', args=(np.mean(residuals), np.std(residuals)))
            ks_result = {
                'statistic': float(ks_stat),
                'p_value': float(ks_p),
                'is_normal': ks_p > 0.05
            }
            
            return {
                'shapiro_wilk': shapiro_result,
                'kolmogorov_smirnov': ks_result
            }
            
        except ImportError:
            return {'error': 'scipy not available for normality tests'}
        except Exception as e:
            return {'error': f'Error in normality tests: {str(e)}'}
    
    def _analyze_heteroscedasticity(self, y_pred: np.ndarray, residuals: np.ndarray) -> Dict[str, Any]:
        """Analyze heteroscedasticity in residuals."""
        try:
            # Simple correlation test
            correlation = np.corrcoef(np.abs(residuals), y_pred)[0, 1]
            
            # Breusch-Pagan test (simplified)
            # Regress squared residuals on predictions
            squared_residuals = residuals ** 2
            
            # Simple linear regression
            X = np.column_stack([np.ones(len(y_pred)), y_pred])
            try:
                coeffs = np.linalg.lstsq(X, squared_residuals, rcond=None)[0]
                fitted = X @ coeffs
                
                # Calculate R-squared
                ss_res = np.sum((squared_residuals - fitted) ** 2)
                ss_tot = np.sum((squared_residuals - np.mean(squared_residuals)) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
                
                return {
                    'correlation_with_predictions': float(correlation),
                    'breusch_pagan_r_squared': float(r_squared),
                    'likely_heteroscedastic': abs(correlation) > 0.3 or r_squared > 0.1
                }
            except np.linalg.LinAlgError:
                return {
                    'correlation_with_predictions': float(correlation),
                    'likely_heteroscedastic': abs(correlation) > 0.3,
                    'note': 'Could not perform Breusch-Pagan test'
                }
                
        except Exception as e:
            return {'error': f'Error in heteroscedasticity analysis: {str(e)}'}
    
    def _detect_outliers(self, residuals: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Detect outliers in residuals."""
        
        # IQR method
        q1 = np.percentile(residuals, 25)
        q3 = np.percentile(residuals, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outlier_mask = (residuals < lower_bound) | (residuals > upper_bound)
        outlier_indices = np.where(outlier_mask)[0]
        
        # Z-score method
        z_scores = np.abs((residuals - np.mean(residuals)) / np.std(residuals))
        z_outlier_mask = z_scores > 3
        z_outlier_indices = np.where(z_outlier_mask)[0]
        
        return {
            'iqr_method': {
                'count': int(np.sum(outlier_mask)),
                'percentage': float(np.sum(outlier_mask) / len(residuals) * 100),
                'indices': outlier_indices.tolist()[:10]  # First 10 outliers
            },
            'z_score_method': {
                'count': int(np.sum(z_outlier_mask)),
                'percentage': float(np.sum(z_outlier_mask) / len(residuals) * 100),
                'indices': z_outlier_indices.tolist()[:10]  # First 10 outliers
            }
        }
    
    def _generate_html_report(self, evaluation_results: Dict[str, Any]) -> str:
        """Generate HTML evaluation report."""
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ViewTrendsSL Model Evaluation Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
                .section { margin: 20px 0; }
                .metric { background-color: #f9f9f9; padding: 10px; margin: 5px 0; border-left: 4px solid #007bff; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .plot { text-align: center; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>ViewTrendsSL Model Evaluation Report</h1>
                <p>Generated on: {timestamp}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                <p>This report provides a comprehensive evaluation of the ViewTrendsSL machine learning models.</p>
            </div>
            
            <div class="section">
                <h2>Model Performance Metrics</h2>
                {metrics_content}
            </div>
            
            <div class="section">
                <h2>Feature Importance Analysis</h2>
                {feature_content}
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                <ul>
                    <li>Monitor model performance regularly</li>
                    <li>Retrain models when performance degrades</li>
                    <li>Consider feature engineering improvements</li>
                    <li>Validate predictions on new data</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        # Generate content sections
        metrics_content = self._generate_metrics_html(evaluation_results)
        feature_content = self._generate_feature_html(evaluation_results)
        
        return html_template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            metrics_content=metrics_content,
            feature_content=feature_content
        )
    
    def _generate_metrics_html(self, evaluation_results: Dict[str, Any]) -> str:
        """Generate HTML for metrics section."""
        
        html = "<div class='metric'><h3>Model Performance Summary</h3>"
        
        if 'basic_metrics' in evaluation_results:
            metrics = evaluation_results['basic_metrics']
            html += f"""
            <p><strong>R² Score:</strong> {metrics.get('r2_score', 'N/A'):.4f}</p>
            <p><strong>MAPE:</strong> {metrics.get('mape', 'N/A'):.2f}%</p>
            <p><strong>MAE:</strong> {metrics.get('mae', 'N/A'):.2f}</p>
            <p><strong>RMSE:</strong> {metrics.get('rmse', 'N/A'):.2f}</p>
            """
        
        html += "</div>"
        return html
    
    def _generate_feature_html(self, evaluation_results: Dict[str, Any]) -> str:
        """Generate HTML for feature importance section."""
        
        html = "<div class='metric'><h3>Top Important Features</h3>"
        
        if 'top_features' in evaluation_results:
            html += "<table><tr><th>Feature</th><th>Importance</th></tr>"
            for feature, importance in evaluation_results['top_features'][:10]:
                html += f"<tr><td>{feature}</td><td>{importance:.4f}</td></tr>"
            html += "</table>"
        
        html += "</div>"
        return html
