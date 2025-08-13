"""
Prediction Page

This module provides the main prediction interface for the ViewTrendsSL web application.

Author: ViewTrendsSL Team
Date: 2025
"""

import streamlit as st
import requests
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import plotly.graph_objects as go
from urllib.parse import urlparse, parse_qs

from src.presentation.components.chart_component import ChartComponent, display_metric_card, display_chart_with_download


class PredictionPage:
    """Prediction page functionality for ViewTrendsSL."""
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
        self.chart_component = ChartComponent()
    
    def render(self):
        """Render the prediction page."""
        st.set_page_config(
            page_title="Predictions - ViewTrendsSL",
            page_icon="🔮",
            layout="wide"
        )
        
        self._render_header()
        self._render_navigation()
        
        # Check authentication
        if 'access_token' not in st.session_state:
            self._render_login_required()
            return
        
        # Main content based on selected tab
        tab = st.session_state.get('prediction_tab', 'single')
        
        if tab == 'single':
            self._render_single_prediction()
        elif tab == 'batch':
            self._render_batch_prediction()
        elif tab == 'custom':
            self._render_custom_prediction()
        elif tab == 'history':
            self._render_prediction_history()
        elif tab == 'compare':
            self._render_comparison_tool()
    
    def _render_header(self):
        """Render the page header."""
        st.markdown("""
        <style>
        .prediction-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .tab-container {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }
        .prediction-form {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .result-container {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            margin-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="prediction-header">
            <h1>🔮 Video Predictions</h1>
            <p>Get accurate viewership forecasts for YouTube videos</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_navigation(self):
        """Render the navigation tabs."""
        st.markdown('<div class="tab-container">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🎯 Single Video", use_container_width=True):
                st.session_state.prediction_tab = 'single'
                st.rerun()
        
        with col2:
            if st.button("📊 Batch Prediction", use_container_width=True):
                st.session_state.prediction_tab = 'batch'
                st.rerun()
        
        with col3:
            if st.button("⚙️ Custom Prediction", use_container_width=True):
                st.session_state.prediction_tab = 'custom'
                st.rerun()
        
        with col4:
            if st.button("📈 History", use_container_width=True):
                st.session_state.prediction_tab = 'history'
                st.rerun()
        
        with col5:
            if st.button("🔄 Compare", use_container_width=True):
                st.session_state.prediction_tab = 'compare'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show current tab
        current_tab = st.session_state.get('prediction_tab', 'single')
        tab_names = {
            'single': '🎯 Single Video Prediction',
            'batch': '📊 Batch Prediction',
            'custom': '⚙️ Custom Prediction',
            'history': '📈 Prediction History',
            'compare': '🔄 Compare Predictions'
        }
        st.markdown(f"### {tab_names.get(current_tab, 'Prediction')}")
    
    def _render_login_required(self):
        """Render login required message."""
        st.warning("🔒 Please log in to access prediction features.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚪 Go to Login", use_container_width=True):
                st.switch_page("pages/auth.py")
    
    def _render_single_prediction(self):
        """Render single video prediction interface."""
        st.markdown('<div class="prediction-form">', unsafe_allow_html=True)
        
        with st.form("single_prediction_form"):
            st.markdown("#### 📹 Video Information")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                video_url = st.text_input(
                    "YouTube Video URL",
                    placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    help="Enter the full YouTube video URL"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("🔍 Analyze Video", use_container_width=True):
                    if video_url:
                        self._extract_video_info(video_url)
            
            st.markdown("#### ⚙️ Prediction Settings")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                timeframes = st.multiselect(
                    "Prediction Timeframes (days)",
                    options=[1, 3, 7, 14, 30, 90],
                    default=[7, 30],
                    help="Select the time periods for prediction"
                )
            
            with col2:
                include_confidence = st.checkbox(
                    "Include Confidence Intervals",
                    value=True,
                    help="Show prediction confidence ranges"
                )
            
            with col3:
                include_insights = st.checkbox(
                    "Include AI Insights",
                    value=True,
                    help="Get AI-generated insights and recommendations"
                )
            
            # Advanced options
            with st.expander("🔧 Advanced Options"):
                col1, col2 = st.columns(2)
                
                with col1:
                    model_type = st.selectbox(
                        "Model Type",
                        options=["auto", "shorts", "longform"],
                        index=0,
                        help="Choose model type (auto-detect recommended)"
                    )
                
                with col2:
                    save_to_history = st.checkbox(
                        "Save to History",
                        value=True,
                        help="Save this prediction to your history"
                    )
            
            predict_button = st.form_submit_button("🚀 Generate Prediction", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if predict_button and video_url:
            self._handle_single_prediction(
                video_url, timeframes, include_confidence, 
                include_insights, model_type, save_to_history
            )
    
    def _render_batch_prediction(self):
        """Render batch prediction interface."""
        st.markdown('<div class="prediction-form">', unsafe_allow_html=True)
        
        st.markdown("#### 📊 Batch Video Analysis")
        st.info("Analyze multiple videos at once (up to 10 videos per batch)")
        
        with st.form("batch_prediction_form"):
            # Video URLs input
            video_urls_text = st.text_area(
                "YouTube Video URLs (one per line)",
                height=200,
                placeholder="https://www.youtube.com/watch?v=video1\nhttps://www.youtube.com/watch?v=video2\n...",
                help="Enter up to 10 YouTube video URLs, one per line"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                timeframes = st.multiselect(
                    "Prediction Timeframes (days)",
                    options=[1, 3, 7, 14, 30, 90],
                    default=[7, 30]
                )
            
            with col2:
                include_confidence = st.checkbox(
                    "Include Confidence Intervals",
                    value=True
                )
            
            # File upload option
            st.markdown("#### 📁 Or Upload CSV File")
            uploaded_file = st.file_uploader(
                "Upload CSV with video URLs",
                type=['csv'],
                help="CSV should have a 'video_url' column"
            )
            
            batch_predict_button = st.form_submit_button("🚀 Analyze Batch", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if batch_predict_button:
            video_urls = []
            
            # Process text input
            if video_urls_text:
                video_urls.extend([url.strip() for url in video_urls_text.split('\n') if url.strip()])
            
            # Process uploaded file
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)
                    if 'video_url' in df.columns:
                        video_urls.extend(df['video_url'].dropna().tolist())
                    else:
                        st.error("CSV file must contain a 'video_url' column")
                        return
                except Exception as e:
                    st.error(f"Error reading CSV file: {str(e)}")
                    return
            
            if video_urls:
                self._handle_batch_prediction(video_urls, timeframes, include_confidence)
            else:
                st.warning("Please provide video URLs either in the text area or upload a CSV file")
    
    def _render_custom_prediction(self):
        """Render custom prediction interface."""
        st.markdown('<div class="prediction-form">', unsafe_allow_html=True)
        
        st.markdown("#### ⚙️ Custom Video Prediction")
        st.info("Create predictions for hypothetical videos by specifying metadata manually")
        
        with st.form("custom_prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input(
                    "Video Title",
                    placeholder="Amazing Sri Lankan Food Recipe!",
                    help="Enter the video title"
                )
                
                description = st.text_area(
                    "Video Description",
                    height=100,
                    placeholder="In this video, we'll show you how to make...",
                    help="Enter the video description"
                )
                
                duration_minutes = st.number_input(
                    "Duration (minutes)",
                    min_value=0.1,
                    max_value=600.0,
                    value=10.0,
                    step=0.5,
                    help="Video duration in minutes"
                )
                
                category_id = st.selectbox(
                    "Category",
                    options=[
                        (22, "People & Blogs"),
                        (23, "Comedy"),
                        (24, "Entertainment"),
                        (25, "News & Politics"),
                        (26, "Howto & Style"),
                        (27, "Education"),
                        (28, "Science & Technology"),
                        (10, "Music"),
                        (15, "Pets & Animals"),
                        (17, "Sports"),
                        (19, "Travel & Events"),
                        (20, "Gaming"),
                        (1, "Film & Animation"),
                        (2, "Autos & Vehicles")
                    ],
                    format_func=lambda x: x[1],
                    help="Select video category"
                )
            
            with col2:
                tags = st.text_input(
                    "Tags (comma-separated)",
                    placeholder="cooking, sri lanka, recipe, food",
                    help="Enter video tags separated by commas"
                )
                
                publish_time = st.datetime_input(
                    "Publish Time",
                    value=datetime.now(),
                    help="When will the video be published?"
                )
                
                channel_subscriber_count = st.number_input(
                    "Channel Subscriber Count",
                    min_value=0,
                    value=1000,
                    step=100,
                    help="Number of subscribers on the channel"
                )
                
                is_short = st.checkbox(
                    "YouTube Short",
                    value=duration_minutes <= 1,
                    help="Is this a YouTube Short?"
                )
                
                timeframes = st.multiselect(
                    "Prediction Timeframes (days)",
                    options=[1, 3, 7, 14, 30, 90],
                    default=[7, 30]
                )
            
            custom_predict_button = st.form_submit_button("🚀 Generate Custom Prediction", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if custom_predict_button and title:
            self._handle_custom_prediction(
                title, description, duration_minutes * 60, category_id[0],
                tags, publish_time, channel_subscriber_count, is_short, timeframes
            )
    
    def _render_prediction_history(self):
        """Render prediction history interface."""
        st.markdown("#### 📈 Your Prediction History")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            date_range = st.selectbox(
                "Time Period",
                options=["last_week", "last_month", "last_3_months", "all_time"],
                format_func=lambda x: x.replace('_', ' ').title(),
                index=1
            )
        
        with col2:
            per_page = st.selectbox(
                "Results per page",
                options=[10, 20, 50, 100],
                index=1
            )
        
        with col3:
            sort_by = st.selectbox(
                "Sort by",
                options=["created_at", "video_title", "prediction_accuracy"],
                format_func=lambda x: x.replace('_', ' ').title(),
                index=0
            )
        
        with col4:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        # Load and display history
        self._load_prediction_history(date_range, per_page, sort_by)
    
    def _render_comparison_tool(self):
        """Render prediction comparison interface."""
        st.markdown("#### 🔄 Compare Predictions")
        st.info("Select multiple predictions from your history to compare their forecasts")
        
        # Load user's predictions for selection
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/prediction/history",
                headers=headers,
                params={'per_page': 50},
                timeout=10
            )
            
            if response.status_code == 200:
                history_data = response.json().get('predictions', [])
                
                if history_data:
                    # Create selection interface
                    prediction_options = {}
                    for pred in history_data:
                        key = f"{pred.get('video_title', 'Unknown')} ({pred.get('created_at', '')[:10]})"
                        prediction_options[key] = pred.get('prediction_id')
                    
                    selected_predictions = st.multiselect(
                        "Select predictions to compare (2-5 predictions)",
                        options=list(prediction_options.keys()),
                        help="Choose predictions you want to compare"
                    )
                    
                    if len(selected_predictions) >= 2:
                        if st.button("🔄 Compare Selected Predictions", use_container_width=True):
                            prediction_ids = [prediction_options[key] for key in selected_predictions]
                            self._handle_comparison(prediction_ids)
                    elif len(selected_predictions) == 1:
                        st.warning("Please select at least 2 predictions to compare")
                else:
                    st.info("📝 No predictions found. Make some predictions first to use the comparison tool.")
            else:
                st.error("Unable to load prediction history for comparison")
                
        except Exception as e:
            st.error(f"Error loading predictions: {str(e)}")
    
    def _extract_video_info(self, video_url: str):
        """Extract and display video information."""
        try:
            # Extract video ID from URL
            video_id = self._extract_video_id(video_url)
            if not video_id:
                st.error("❌ Invalid YouTube URL")
                return
            
            with st.spinner("🔄 Fetching video information..."):
                # Mock video info for demonstration
                st.success("✅ Video information extracted successfully!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info("**Title:** Sample Video Title")
                    st.info("**Duration:** 5:30")
                    st.info("**Category:** Entertainment")
                
                with col2:
                    st.info("**Channel:** Sample Channel")
                    st.info("**Published:** 2025-01-01")
                    st.info("**Current Views:** 1,234")
                
        except Exception as e:
            st.error(f"❌ Error extracting video info: {str(e)}")
    
    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        try:
            parsed_url = urlparse(url)
            
            if 'youtube.com' in parsed_url.netloc:
                if 'watch' in parsed_url.path:
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                elif 'embed' in parsed_url.path:
                    return parsed_url.path.split('/')[-1]
            elif 'youtu.be' in parsed_url.netloc:
                return parsed_url.path[1:]
            
            return None
        except:
            return None
    
    def _handle_single_prediction(self, video_url: str, timeframes: list, 
                                include_confidence: bool, include_insights: bool,
                                model_type: str, save_to_history: bool):
        """Handle single video prediction request."""
        try:
            with st.spinner("🔄 Generating prediction..."):
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
                    self._display_single_prediction_result(result)
                else:
                    error_msg = response.json().get('error', 'Unknown error occurred')
                    st.error(f"❌ Error: {error_msg}")
                    
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _handle_batch_prediction(self, video_urls: list, timeframes: list, include_confidence: bool):
        """Handle batch prediction request."""
        if len(video_urls) > 10:
            st.warning("⚠️ Maximum 10 videos allowed per batch. Using first 10 URLs.")
            video_urls = video_urls[:10]
        
        try:
            with st.spinner(f"🔄 Analyzing {len(video_urls)} videos..."):
                headers = {
                    'Authorization': f'Bearer {st.session_state.access_token}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'video_urls': video_urls,
                    'prediction_timeframes': timeframes,
                    'include_confidence': include_confidence
                }
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/prediction/predict/batch",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._display_batch_prediction_result(result)
                else:
                    error_msg = response.json().get('error', 'Unknown error occurred')
                    st.error(f"❌ Error: {error_msg}")
                    
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _handle_custom_prediction(self, title: str, description: str, duration_seconds: int,
                                category_id: int, tags: str, publish_time: datetime,
                                channel_subscriber_count: int, is_short: bool, timeframes: list):
        """Handle custom prediction request."""
        try:
            with st.spinner("🔄 Generating custom prediction..."):
                headers = {
                    'Authorization': f'Bearer {st.session_state.access_token}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'title': title,
                    'description': description,
                    'duration_seconds': duration_seconds,
                    'category_id': category_id,
                    'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
                    'publish_time': publish_time.isoformat(),
                    'channel_subscriber_count': channel_subscriber_count,
                    'is_short': is_short,
                    'prediction_timeframes': timeframes
                }
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/prediction/predict/custom",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._display_custom_prediction_result(result)
                else:
                    error_msg = response.json().get('error', 'Unknown error occurred')
                    st.error(f"❌ Error: {error_msg}")
                    
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _handle_comparison(self, prediction_ids: list):
        """Handle prediction comparison request."""
        try:
            with st.spinner("🔄 Comparing predictions..."):
                headers = {
                    'Authorization': f'Bearer {st.session_state.access_token}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'prediction_ids': prediction_ids
                }
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/prediction/compare",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._display_comparison_result(result)
                else:
                    error_msg = response.json().get('error', 'Unknown error occurred')
                    st.error(f"❌ Error: {error_msg}")
                    
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _display_single_prediction_result(self, result: Dict[str, Any]):
        """Display single prediction results."""
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        
        st.success("✅ Prediction completed successfully!")
        
        # Video information
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Title:** {result.get('video_title', 'N/A')}")
        with col2:
            st.info(f"**Video ID:** {result.get('video_id', 'N/A')}")
        
        # Prediction chart
        if result.get('predictions'):
            chart = self.chart_component.create_viewership_forecast_chart(
                prediction_data=result,
                video_title=result.get('video_title', 'Video Forecast'),
                show_confidence=result.get('confidence_scores') is not None
            )
            
            display_chart_with_download(chart, f"prediction_{result.get('video_id', 'video')}")
            
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
            st.markdown("### 💡 AI Insights")
            insights = result.get('insights', {})
            
            for insight_type, insight_data in insights.items():
                if isinstance(insight_data, str):
                    st.info(f"**{insight_type.replace('_', ' ').title()}:** {insight_data}")
                elif isinstance(insight_data, dict):
                    with st.expander(f"📋 {insight_type.replace('_', ' ').title()}"):
                        st.json(insight_data)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _display_batch_prediction_result(self, result: Dict[str, Any]):
        """Display batch prediction results."""
        st.success(f"✅ Batch prediction completed! {result.get('successful_predictions', 0)} successful, {result.get('failed_predictions', 0)} failed")
        
        successful_predictions = result.get('successful_predictions', [])
        failed_predictions = result.get('failed_predictions', [])
        
        if successful_predictions:
            st.markdown("### 📊 Successful Predictions")
            
            # Create comparison chart
            chart = self.chart_component.create_comparison_chart(successful_predictions)
            display_chart_with_download(chart, f"batch_prediction_{result.get('batch_id', 'batch')}")
            
            # Results table
            st.markdown("### 📋 Results Summary")
            
            results_data = []
            for pred in successful_predictions:
                predictions = pred.get('predictions', {})
                row = {
                    'Video Title': pred.get('video_title', 'N/A')[:50] + '...' if len(pred.get('video_title', '')) > 50 else pred.get('video_title', 'N/A'),
                    'Video ID': pred.get('video_id', 'N/A')
                }
                
                for timeframe, views in predictions.items():
                    days = timeframe.replace('_days', '').replace('_', ' ').title()
                    row[f'{days} Days'] = f"{views:,.0f}"
                
                results_data.append(row)
            
            if results_data:
                df = pd.DataFrame(results_data)
                st.dataframe(df, use_container_width=True)
                
                # Download CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results CSV",
                    data=csv,
                    file_name=f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        if failed_predictions:
            st.markdown("### ❌ Failed Predictions")
            for error in failed_predictions:
                st.error(f"**{error.get('video_url', 'Unknown URL')}:** {error.get('error', 'Unknown error')}")
    
    def _display_custom_prediction_result(self, result: Dict[str, Any]):
        """Display custom prediction results."""
        st.success("✅ Custom prediction completed successfully!")
        
        # Prediction chart
        if result.get('predictions'):
            chart = self.chart_component.create_viewership_forecast_chart(
                prediction_data=result,
                video_title="Custom Video Prediction",
                show_confidence=result.get('confidence_scores') is not None
            )
            
            display_chart_with_download(chart, "custom_prediction")
            
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
    
    def _display_comparison_result(self, result: Dict[str, Any]):
        """Display comparison results."""
        st.success("✅ Comparison completed successfully!")
        
        comparison_data = result.get('comparison', {})
        predictions = comparison_data.get('predictions', [])
        
        if predictions:
            # Create comparison chart
            chart = self.chart_component.create_comparison_chart(predictions)
            display_chart_with_download(chart, "prediction_comparison")
            
            # Comparison summary
            st.markdown("### 📊 Comparison Summary")
            
            summary_data = []
            for pred in predictions:
                predictions_dict = pred.get('predictions', {})
                row = {
                    'Video': pred.get('video_title', 'N/A')[:30] + '...' if len(pred.get('video_title', '')) > 30 else pred.get('video_title', 'N/A')
                }
                
                for timeframe, views in predictions_dict.items():
                    days = timeframe.replace('_days', '').replace('_', ' ').title()
                    row[f'{days} Days'] = f"{views:,.0f}"
                
                summary_data.append(row)
            
            if summary_data:
                df = pd.DataFrame(summary_data)
                st.dataframe(df, use_container_width=True)
                
                # Download comparison CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Comparison CSV",
                    data=csv,
                    file_name=f"prediction_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    def _load_prediction_history(self, date_range: str, per_page: int, sort_by: str):
        """Load and display prediction history."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Calculate date filter
            params = {'per_page': per_page}
            
            if date_range != 'all_time':
                end_date = datetime.now()
                if date_range == 'last_week':
                    start_date = end_date - timedelta(weeks=1)
                elif date_range == 'last_month':
                    start_date = end_date - timedelta(days=30)
                elif date_range == 'last_3_months':
                    start_date = end_date - timedelta(days=90)
                
                params['start_date'] = start_date.isoformat()
                params['end_date'] = end_date.isoformat()
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/prediction/history",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                predictions = data.get('predictions', [])
                pagination = data.get('pagination', {})
                
                if predictions:
                    # Display predictions
                    for pred in predictions:
                        with st.expander(f"📹 {pred.get('video_title', 'Unknown Video')} - {pred.get('created_at', '')[:10]}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Video ID:** {pred.get('video_id', 'N/A')}")
                                st.write(f"**Created:** {pred.get('created_at', 'N/A')}")
                                st.write(f"**Prediction ID:** {pred.get('prediction_id', 'N/A')}")
                            
                            with col2:
                                predictions_dict = pred.get('predictions', {})
                                for timeframe, views in predictions_dict.items():
                                    days = timeframe.replace('_days', '').replace('_', ' ').title()
                                    st.write(f"**{days} Days:** {views:,.0f} views")
                            
                            # View details button
                            if st.button(f"View Details", key=f"details_{pred.get('prediction_id')}"):
                                st.session_state.selected_prediction = pred.get('prediction_id')
                    
                    # Pagination
                    if pagination.get('pages', 1) > 1:
                        st.markdown("### 📄 Pagination")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if pagination.get('has_prev') and st.button("⬅️ Previous"):
                                st.session_state.history_page = pagination.get('page', 1) - 1
                                st.rerun()
                        
                        with col2:
                            st.write(f"Page {pagination.get('page', 1)} of {pagination.get('pages', 1)}")
                        
                        with col3:
                            if pagination.get('has_next') and st.button("➡️ Next"):
                                st.session_state.history_page = pagination.get('page', 1) + 1
                                st.rerun()
                else:
                    st.info("📝 No predictions found for the selected time period.")
            else:
                st.error("Unable to load prediction history.")
                
        except Exception as e:
            st.error(f"Error loading prediction history: {str(e)}")


def main():
    """Main function to run the prediction page."""
    prediction_page = PredictionPage()
    prediction_page.render()


if __name__ == "__main__":
    main()
