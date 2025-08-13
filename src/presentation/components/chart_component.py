"""
Chart Components

This module provides reusable chart components for data visualization
in the ViewTrendsSL web interface.

Author: ViewTrendsSL Team
Date: 2025
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class ChartComponent:
    """Reusable chart components for ViewTrendsSL."""
    
    @staticmethod
    def create_viewership_forecast_chart(
        prediction_data: Dict[str, Any],
        video_title: str = "Video Forecast",
        show_confidence: bool = True
    ) -> go.Figure:
        """
        Create a viewership forecast line chart.
        
        Args:
            prediction_data: Dictionary containing prediction results
            video_title: Title of the video being predicted
            show_confidence: Whether to show confidence intervals
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Extract prediction data
        predictions = prediction_data.get('predictions', {})
        confidence_scores = prediction_data.get('confidence_scores', {})
        
        # Create time points for the forecast
        time_points = []
        view_counts = []
        confidence_upper = []
        confidence_lower = []
        
        for timeframe, views in predictions.items():
            if timeframe.endswith('_days'):
                days = int(timeframe.split('_')[0])
                time_points.append(days)
                view_counts.append(views)
                
                # Add confidence intervals if available
                if show_confidence and confidence_scores:
                    confidence = confidence_scores.get(timeframe, 0.8)
                    margin = views * (1 - confidence) * 0.5
                    confidence_upper.append(views + margin)
                    confidence_lower.append(max(0, views - margin))
        
        # Sort by time points
        sorted_data = sorted(zip(time_points, view_counts, confidence_upper, confidence_lower))
        if sorted_data:
            time_points, view_counts, confidence_upper, confidence_lower = zip(*sorted_data)
        
        # Add confidence interval
        if show_confidence and confidence_upper:
            fig.add_trace(go.Scatter(
                x=list(time_points) + list(reversed(time_points)),
                y=list(confidence_upper) + list(reversed(confidence_lower)),
                fill='toself',
                fillcolor='rgba(0,100,80,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=False,
                name='Confidence Interval'
            ))
        
        # Add main forecast line
        fig.add_trace(go.Scatter(
            x=time_points,
            y=view_counts,
            mode='lines+markers',
            name='Predicted Views',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color='#1f77b4'),
            hovertemplate='<b>Day %{x}</b><br>Views: %{y:,.0f}<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Viewership Forecast: {video_title[:50]}...' if len(video_title) > 50 else f'Viewership Forecast: {video_title}',
            xaxis_title='Days After Upload',
            yaxis_title='Predicted Views',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Format y-axis to show numbers in K, M format
        fig.update_yaxis(tickformat='.2s')
        
        return fig
    
    @staticmethod
    def create_category_performance_chart(category_data: List[Dict]) -> go.Figure:
        """
        Create a bar chart showing performance by category.
        
        Args:
            category_data: List of dictionaries with category performance data
            
        Returns:
            Plotly figure object
        """
        if not category_data:
            return go.Figure()
        
        df = pd.DataFrame(category_data)
        
        fig = px.bar(
            df,
            x='category_name',
            y='avg_views',
            color='avg_views',
            color_continuous_scale='viridis',
            title='Average Views by Category',
            labels={
                'category_name': 'Category',
                'avg_views': 'Average Views'
            }
        )
        
        fig.update_layout(
            template='plotly_white',
            height=400,
            xaxis_tickangle=-45
        )
        
        fig.update_yaxis(tickformat='.2s')
        
        return fig
    
    @staticmethod
    def create_trend_analysis_chart(trend_data: Dict[str, Any]) -> go.Figure:
        """
        Create a multi-line chart showing trends over time.
        
        Args:
            trend_data: Dictionary containing trend data
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        trends = trend_data.get('trends', {})
        
        for trend_name, data_points in trends.items():
            if isinstance(data_points, list) and data_points:
                dates = [point.get('date') for point in data_points]
                values = [point.get('value', 0) for point in data_points]
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    name=trend_name.replace('_', ' ').title(),
                    line=dict(width=2),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title='Trend Analysis Over Time',
            xaxis_title='Date',
            yaxis_title='Value',
            template='plotly_white',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_comparison_chart(comparison_data: List[Dict]) -> go.Figure:
        """
        Create a comparison chart for multiple videos.
        
        Args:
            comparison_data: List of video comparison data
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        for i, video_data in enumerate(comparison_data):
            video_title = video_data.get('video_title', f'Video {i+1}')
            predictions = video_data.get('predictions', {})
            
            time_points = []
            view_counts = []
            
            for timeframe, views in predictions.items():
                if timeframe.endswith('_days'):
                    days = int(timeframe.split('_')[0])
                    time_points.append(days)
                    view_counts.append(views)
            
            # Sort by time points
            sorted_data = sorted(zip(time_points, view_counts))
            if sorted_data:
                time_points, view_counts = zip(*sorted_data)
                
                fig.add_trace(go.Scatter(
                    x=time_points,
                    y=view_counts,
                    mode='lines+markers',
                    name=video_title[:30] + '...' if len(video_title) > 30 else video_title,
                    line=dict(width=2),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title='Video Performance Comparison',
            xaxis_title='Days After Upload',
            yaxis_title='Predicted Views',
            template='plotly_white',
            height=500,
            hovermode='x unified'
        )
        
        fig.update_yaxis(tickformat='.2s')
        
        return fig
    
    @staticmethod
    def create_dashboard_metrics_chart(metrics_data: Dict[str, Any]) -> go.Figure:
        """
        Create a dashboard with key metrics.
        
        Args:
            metrics_data: Dictionary containing dashboard metrics
            
        Returns:
            Plotly figure object
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Predictions', 'Accuracy Trend', 'Popular Categories', 'User Activity'),
            specs=[[{"type": "indicator"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Total predictions indicator
        total_predictions = metrics_data.get('total_predictions', 0)
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=total_predictions,
                title={"text": "Total Predictions"},
                number={'font': {'size': 40}}
            ),
            row=1, col=1
        )
        
        # Accuracy trend
        accuracy_data = metrics_data.get('accuracy_trend', [])
        if accuracy_data:
            dates = [point.get('date') for point in accuracy_data]
            accuracy = [point.get('accuracy', 0) for point in accuracy_data]
            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=accuracy,
                    mode='lines+markers',
                    name='Accuracy',
                    line=dict(color='green', width=2)
                ),
                row=1, col=2
            )
        
        # Popular categories
        category_data = metrics_data.get('popular_categories', [])
        if category_data:
            categories = [cat.get('name') for cat in category_data]
            counts = [cat.get('count', 0) for cat in category_data]
            
            fig.add_trace(
                go.Bar(
                    x=categories,
                    y=counts,
                    name='Categories',
                    marker_color='lightblue'
                ),
                row=2, col=1
            )
        
        # User activity
        activity_data = metrics_data.get('user_activity', [])
        if activity_data:
            dates = [point.get('date') for point in activity_data]
            users = [point.get('active_users', 0) for point in activity_data]
            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=users,
                    mode='lines+markers',
                    name='Active Users',
                    line=dict(color='orange', width=2)
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            template='plotly_white',
            title_text="Dashboard Overview"
        )
        
        return fig
    
    @staticmethod
    def create_prediction_history_chart(history_data: List[Dict]) -> go.Figure:
        """
        Create a chart showing prediction history over time.
        
        Args:
            history_data: List of prediction history records
            
        Returns:
            Plotly figure object
        """
        if not history_data:
            return go.Figure()
        
        df = pd.DataFrame(history_data)
        
        # Convert created_at to datetime
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Group by date and count predictions
        daily_counts = df.groupby(df['created_at'].dt.date).size().reset_index()
        daily_counts.columns = ['date', 'count']
        
        fig = px.line(
            daily_counts,
            x='date',
            y='count',
            title='Prediction Activity Over Time',
            labels={
                'date': 'Date',
                'count': 'Number of Predictions'
            }
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8)
        )
        
        fig.update_layout(
            template='plotly_white',
            height=400
        )
        
        return fig


def display_metric_card(title: str, value: str, delta: Optional[str] = None, delta_color: str = "normal"):
    """
    Display a metric card using Streamlit.
    
    Args:
        title: Metric title
        value: Metric value
        delta: Change indicator
        delta_color: Color of delta (normal, inverse, off)
    """
    st.metric(
        label=title,
        value=value,
        delta=delta,
        delta_color=delta_color
    )


def display_chart_with_download(fig: go.Figure, filename: str = "chart"):
    """
    Display a chart with download option.
    
    Args:
        fig: Plotly figure object
        filename: Filename for download
    """
    st.plotly_chart(fig, use_container_width=True)
    
    # Add download button
    img_bytes = fig.to_image(format="png", width=1200, height=600)
    st.download_button(
        label="📥 Download Chart",
        data=img_bytes,
        file_name=f"{filename}.png",
        mime="image/png"
    )
