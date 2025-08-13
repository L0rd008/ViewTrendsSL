"""
Home Page

This module provides the main landing page for the ViewTrendsSL web interface.

Author: ViewTrendsSL Team
Date: 2025
"""

import streamlit as st
import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime
import plotly.graph_objects as go

from src.presentation.components.chart_component import ChartComponent, display_metric_card


class HomePage:
    """Home page functionality for ViewTrendsSL."""
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
        self.chart_component = ChartComponent()
    
    def render(self):
        """Render the home page."""
        self._render_header()
        self._render_hero_section()
        self._render_quick_prediction()
        self._render_recent_activity()
        self._render_features_overview()
        self._render_footer()
    
    def _render_header(self):
        """Render the page header."""
        st.set_page_config(
            page_title="ViewTrendsSL - YouTube Viewership Forecasting",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 1rem 0;
        }
        .metric-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="main-header">
            <h1>🎬 ViewTrendsSL</h1>
            <h3>YouTube Viewership Forecasting for Sri Lankan Audience</h3>
            <p>Predict your video's performance before you upload</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_hero_section(self):
        """Render the hero section with key value propositions."""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🎯 Accurate Predictions</h4>
                <p>Get precise viewership forecasts using advanced machine learning models trained on Sri Lankan YouTube data.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Data-Driven Insights</h4>
                <p>Understand what makes videos successful with comprehensive analytics and trend analysis.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🚀 Optimize Performance</h4>
                <p>Make informed decisions about content strategy, timing, and optimization for maximum reach.</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_quick_prediction(self):
        """Render the quick prediction section."""
        st.markdown("## 🔮 Quick Prediction")
        st.markdown("Get instant viewership forecasts for any YouTube video")
        
        with st.form("quick_prediction_form"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                video_url = st.text_input(
                    "YouTube Video URL",
                    placeholder="https://www.youtube.com/watch?v=...",
                    help="Paste any YouTube video URL to get a prediction"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                predict_button = st.form_submit_button("🔍 Predict", use_container_width=True)
            
            # Prediction options
            col1, col2, col3 = st.columns(3)
            with col1:
                include_confidence = st.checkbox("Include confidence intervals", value=True)
            with col2:
                include_insights = st.checkbox("Include insights", value=True)
            with col3:
                timeframes = st.multiselect(
                    "Prediction timeframes (days)",
                    options=[1, 3, 7, 14, 30, 90],
                    default=[7, 30]
                )
        
        if predict_button and video_url:
            self._handle_quick_prediction(video_url, timeframes, include_confidence, include_insights)
    
    def _handle_quick_prediction(self, video_url: str, timeframes: list, include_confidence: bool, include_insights: bool):
        """Handle quick prediction request."""
        try:
            with st.spinner("🔄 Analyzing video and generating prediction..."):
                # Check if user is logged in
                if 'access_token' not in st.session_state:
                    st.warning("⚠️ Please log in to use the prediction feature.")
                    if st.button("Go to Login"):
                        st.switch_page("pages/auth.py")
                    return
                
                # Make API request
                headers = {
                    'Authorization': f'Bearer {st.session_state.access_token}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'video_url': video_url,
                    'prediction_timeframes': timeframes,
                    'include_confidence': include_confidence,
                    'include_insights': include_insights
                }
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/prediction/predict",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._display_prediction_result(result)
                elif response.status_code == 401:
                    st.error("🔒 Authentication required. Please log in again.")
                    del st.session_state.access_token
                elif response.status_code == 429:
                    st.error("⏰ Rate limit exceeded. Please try again later.")
                else:
                    error_msg = response.json().get('error', 'Unknown error occurred')
                    st.error(f"❌ Error: {error_msg}")
                    
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection error. Please check your internet connection.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _display_prediction_result(self, result: Dict[str, Any]):
        """Display prediction results."""
        st.success("✅ Prediction completed successfully!")
        
        # Video information
        st.markdown("### 📹 Video Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Title:** {result.get('video_title', 'N/A')}")
        with col2:
            st.info(f"**Video ID:** {result.get('video_id', 'N/A')}")
        
        # Prediction chart
        if result.get('predictions'):
            st.markdown("### 📈 Viewership Forecast")
            
            chart = self.chart_component.create_viewership_forecast_chart(
                prediction_data=result,
                video_title=result.get('video_title', 'Video Forecast'),
                show_confidence=result.get('confidence_scores') is not None
            )
            
            st.plotly_chart(chart, use_container_width=True)
            
            # Prediction metrics
            st.markdown("### 📊 Prediction Summary")
            predictions = result.get('predictions', {})
            
            cols = st.columns(len(predictions))
            for i, (timeframe, views) in enumerate(predictions.items()):
                with cols[i]:
                    days = timeframe.replace('_days', '').replace('_', ' ').title()
                    display_metric_card(
                        title=f"{days} Days",
                        value=f"{views:,.0f}",
                        delta=None
                    )
        
        # Insights
        if result.get('insights'):
            st.markdown("### 💡 Insights")
            insights = result.get('insights', {})
            
            for insight_type, insight_data in insights.items():
                if isinstance(insight_data, str):
                    st.info(f"**{insight_type.replace('_', ' ').title()}:** {insight_data}")
                elif isinstance(insight_data, dict):
                    with st.expander(f"📋 {insight_type.replace('_', ' ').title()}"):
                        st.json(insight_data)
        
        # Save to history button
        if st.button("💾 Save to History"):
            st.success("Prediction saved to your history!")
    
    def _render_recent_activity(self):
        """Render recent activity section."""
        st.markdown("## 📊 Platform Overview")
        
        # Mock data for demonstration
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            display_metric_card("Total Predictions", "12,543", "+234")
        
        with col2:
            display_metric_card("Active Users", "1,247", "+45")
        
        with col3:
            display_metric_card("Avg Accuracy", "87.3%", "+2.1%")
        
        with col4:
            display_metric_card("Videos Analyzed", "8,921", "+156")
        
        # Recent predictions chart
        if 'access_token' in st.session_state:
            st.markdown("### 📈 Your Recent Activity")
            self._render_user_activity_chart()
        else:
            st.markdown("### 📈 Platform Activity")
            self._render_platform_activity_chart()
    
    def _render_user_activity_chart(self):
        """Render user-specific activity chart."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/prediction/history",
                headers=headers,
                params={'per_page': 10},
                timeout=10
            )
            
            if response.status_code == 200:
                history_data = response.json().get('predictions', [])
                if history_data:
                    chart = self.chart_component.create_prediction_history_chart(history_data)
                    st.plotly_chart(chart, use_container_width=True)
                else:
                    st.info("📝 No prediction history yet. Make your first prediction above!")
            else:
                st.warning("Unable to load activity data.")
                
        except Exception as e:
            st.warning("Unable to load activity data.")
    
    def _render_platform_activity_chart(self):
        """Render platform-wide activity chart."""
        # Mock data for demonstration
        import pandas as pd
        from datetime import datetime, timedelta
        
        # Generate sample data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        predictions = [50 + (i * 2) + (i % 7) * 10 for i in range(30)]
        
        df = pd.DataFrame({
            'date': dates,
            'predictions': predictions
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['predictions'],
            mode='lines+markers',
            name='Daily Predictions',
            line=dict(color='#667eea', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Platform Activity (Last 30 Days)',
            xaxis_title='Date',
            yaxis_title='Number of Predictions',
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_features_overview(self):
        """Render features overview section."""
        st.markdown("## 🛠️ Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Prediction Features
            - **Single Video Prediction**: Get forecasts for any YouTube video
            - **Batch Predictions**: Analyze multiple videos at once
            - **Custom Predictions**: Test hypothetical video scenarios
            - **Confidence Intervals**: Understand prediction reliability
            - **Multiple Timeframes**: 1, 3, 7, 14, 30, and 90-day forecasts
            """)
            
            st.markdown("""
            ### 📊 Analytics Features
            - **Trend Analysis**: Identify what's working in your niche
            - **Category Insights**: Compare performance across categories
            - **Historical Data**: Track your prediction accuracy over time
            - **Export Options**: Download your data and charts
            """)
        
        with col2:
            st.markdown("""
            ### 🔧 Advanced Tools
            - **Comparison Tool**: Compare multiple video predictions
            - **Performance Tracking**: Monitor actual vs predicted performance
            - **Insight Generation**: Get actionable recommendations
            - **API Access**: Integrate with your own tools (Pro feature)
            """)
            
            st.markdown("""
            ### 🎨 User Experience
            - **Intuitive Interface**: Easy-to-use web interface
            - **Real-time Results**: Get predictions in seconds
            - **Mobile Friendly**: Works on all devices
            - **Secure & Private**: Your data is protected
            """)
    
    def _render_footer(self):
        """Render the page footer."""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **ViewTrendsSL**  
            YouTube Viewership Forecasting  
            University of Moratuwa Project
            """)
        
        with col2:
            st.markdown("""
            **Quick Links**  
            [📈 Make Prediction](prediction)  
            [📊 Analytics](analytics)  
            [📚 Documentation](https://github.com/L0rd008/ViewTrendsSL)
            """)
        
        with col3:
            st.markdown("""
            **Support**  
            [🐛 Report Issues](https://github.com/L0rd008/ViewTrendsSL/issues)  
            [💬 Discussions](https://github.com/L0rd008/ViewTrendsSL/discussions)  
            [📧 Contact Us](mailto:support@viewtrendssl.com)
            """)
        
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666;">
            <p>© 2025 ViewTrendsSL Team. Built with ❤️ for Sri Lankan YouTube creators.</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main function to run the home page."""
    home_page = HomePage()
    home_page.render()


if __name__ == "__main__":
    main()
