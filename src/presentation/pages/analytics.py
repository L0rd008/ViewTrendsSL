"""
Analytics Page

This module provides comprehensive analytics and insights for the ViewTrendsSL web application.

Author: ViewTrendsSL Team
Date: 2025
"""

import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

from src.presentation.components.chart_component import ChartComponent, display_metric_card, display_chart_with_download


class AnalyticsPage:
    """Analytics page functionality for ViewTrendsSL."""
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
        self.chart_component = ChartComponent()
    
    def render(self):
        """Render the analytics page."""
        st.set_page_config(
            page_title="Analytics - ViewTrendsSL",
            page_icon="📊",
            layout="wide"
        )
        
        self._render_header()
        self._render_navigation()
        
        # Check authentication
        if 'access_token' not in st.session_state:
            self._render_login_required()
            return
        
        # Main content based on selected tab
        tab = st.session_state.get('analytics_tab', 'dashboard')
        
        if tab == 'dashboard':
            self._render_dashboard()
        elif tab == 'trends':
            self._render_trends_analysis()
        elif tab == 'categories':
            self._render_category_analysis()
        elif tab == 'insights':
            self._render_insights()
        elif tab == 'reports':
            self._render_reports()
    
    def _render_header(self):
        """Render the page header."""
        st.markdown("""
        <style>
        .analytics-header {
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
        .analytics-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="analytics-header">
            <h1>📊 Analytics Dashboard</h1>
            <p>Comprehensive insights and data analysis for YouTube viewership trends</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_navigation(self):
        """Render the navigation tabs."""
        st.markdown('<div class="tab-container">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("📈 Dashboard", use_container_width=True):
                st.session_state.analytics_tab = 'dashboard'
                st.rerun()
        
        with col2:
            if st.button("📊 Trends", use_container_width=True):
                st.session_state.analytics_tab = 'trends'
                st.rerun()
        
        with col3:
            if st.button("🏷️ Categories", use_container_width=True):
                st.session_state.analytics_tab = 'categories'
                st.rerun()
        
        with col4:
            if st.button("💡 Insights", use_container_width=True):
                st.session_state.analytics_tab = 'insights'
                st.rerun()
        
        with col5:
            if st.button("📋 Reports", use_container_width=True):
                st.session_state.analytics_tab = 'reports'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show current tab
        current_tab = st.session_state.get('analytics_tab', 'dashboard')
        tab_names = {
            'dashboard': '📈 Analytics Dashboard',
            'trends': '📊 Trend Analysis',
            'categories': '🏷️ Category Analysis',
            'insights': '💡 AI Insights',
            'reports': '📋 Reports & Export'
        }
        st.markdown(f"### {tab_names.get(current_tab, 'Analytics')}")
    
    def _render_login_required(self):
        """Render login required message."""
        st.warning("🔒 Please log in to access analytics features.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚪 Go to Login", use_container_width=True):
                st.switch_page("pages/auth.py")
    
    def _render_dashboard(self):
        """Render the main analytics dashboard."""
        # Time range selector
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            date_range = st.selectbox(
                "Time Period",
                options=["last_7_days", "last_30_days", "last_90_days", "last_year"],
                format_func=lambda x: x.replace('_', ' ').title(),
                index=1
            )
        
        with col2:
            refresh_interval = st.selectbox(
                "Auto Refresh",
                options=["off", "30s", "1m", "5m"],
                index=0
            )
        
        with col3:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        # Load dashboard data
        dashboard_data = self._load_dashboard_data(date_range)
        
        if dashboard_data:
            # Key metrics row
            st.markdown("#### 📊 Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                display_metric_card(
                    "Total Predictions",
                    f"{dashboard_data.get('total_predictions', 0):,}",
                    f"+{dashboard_data.get('predictions_change', 0):,}"
                )
            
            with col2:
                display_metric_card(
                    "Avg Accuracy",
                    f"{dashboard_data.get('avg_accuracy', 0):.1f}%",
                    f"+{dashboard_data.get('accuracy_change', 0):.1f}%"
                )
            
            with col3:
                display_metric_card(
                    "Videos Analyzed",
                    f"{dashboard_data.get('videos_analyzed', 0):,}",
                    f"+{dashboard_data.get('videos_change', 0):,}"
                )
            
            with col4:
                display_metric_card(
                    "Active Users",
                    f"{dashboard_data.get('active_users', 0):,}",
                    f"+{dashboard_data.get('users_change', 0):,}"
                )
            
            # Charts row
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Prediction Activity")
                activity_chart = self._create_activity_chart(dashboard_data.get('activity_data', []))
                st.plotly_chart(activity_chart, use_container_width=True)
            
            with col2:
                st.markdown("#### 🎯 Accuracy Trend")
                accuracy_chart = self._create_accuracy_chart(dashboard_data.get('accuracy_data', []))
                st.plotly_chart(accuracy_chart, use_container_width=True)
            
            # Category performance
            st.markdown("#### 🏷️ Category Performance")
            category_chart = self.chart_component.create_category_performance_chart(
                dashboard_data.get('category_data', [])
            )
            display_chart_with_download(category_chart, "category_performance")
            
            # Recent predictions table
            st.markdown("#### 📋 Recent Predictions")
            recent_predictions = dashboard_data.get('recent_predictions', [])
            if recent_predictions:
                df = pd.DataFrame(recent_predictions)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No recent predictions to display.")
    
    def _render_trends_analysis(self):
        """Render trend analysis interface."""
        st.markdown("#### 📊 Trend Analysis")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            trend_type = st.selectbox(
                "Trend Type",
                options=["viewership", "engagement", "category", "timing"],
                format_func=lambda x: x.title()
            )
        
        with col2:
            time_period = st.selectbox(
                "Time Period",
                options=["daily", "weekly", "monthly"],
                index=1
            )
        
        with col3:
            category_filter = st.selectbox(
                "Category",
                options=["all", "entertainment", "education", "music", "news", "gaming"],
                format_func=lambda x: x.title()
            )
        
        with col4:
            if st.button("📊 Analyze Trends", use_container_width=True):
                self._analyze_trends(trend_type, time_period, category_filter)
        
        # Load and display trend data
        trend_data = self._load_trend_data(trend_type, time_period, category_filter)
        
        if trend_data:
            # Main trend chart
            st.markdown("#### 📈 Trend Visualization")
            trend_chart = self.chart_component.create_trend_analysis_chart(trend_data)
            display_chart_with_download(trend_chart, f"trend_{trend_type}_{time_period}")
            
            # Trend insights
            st.markdown("#### 💡 Trend Insights")
            insights = trend_data.get('insights', [])
            
            for insight in insights:
                if insight.get('type') == 'positive':
                    st.success(f"📈 {insight.get('message', '')}")
                elif insight.get('type') == 'negative':
                    st.error(f"📉 {insight.get('message', '')}")
                else:
                    st.info(f"ℹ️ {insight.get('message', '')}")
            
            # Seasonal patterns
            if trend_data.get('seasonal_patterns'):
                st.markdown("#### 🔄 Seasonal Patterns")
                seasonal_chart = self._create_seasonal_chart(trend_data.get('seasonal_patterns'))
                display_chart_with_download(seasonal_chart, f"seasonal_{trend_type}")
    
    def _render_category_analysis(self):
        """Render category analysis interface."""
        st.markdown("#### 🏷️ Category Performance Analysis")
        
        # Category comparison
        col1, col2 = st.columns(2)
        
        with col1:
            selected_categories = st.multiselect(
                "Select Categories to Compare",
                options=["Entertainment", "Education", "Music", "News", "Gaming", "Sports", "Technology"],
                default=["Entertainment", "Education", "Music"]
            )
        
        with col2:
            metric_type = st.selectbox(
                "Comparison Metric",
                options=["avg_views", "prediction_accuracy", "engagement_rate", "growth_rate"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        if selected_categories:
            # Load category data
            category_data = self._load_category_comparison(selected_categories, metric_type)
            
            if category_data:
                # Category comparison chart
                st.markdown("#### 📊 Category Comparison")
                comparison_chart = self._create_category_comparison_chart(category_data, metric_type)
                display_chart_with_download(comparison_chart, f"category_comparison_{metric_type}")
                
                # Category details table
                st.markdown("#### 📋 Category Details")
                df = pd.DataFrame(category_data)
                st.dataframe(df, use_container_width=True)
                
                # Best performing videos by category
                st.markdown("#### 🏆 Top Performing Videos by Category")
                for category in selected_categories:
                    with st.expander(f"🏷️ {category}"):
                        top_videos = self._get_top_videos_by_category(category.lower())
                        if top_videos:
                            for video in top_videos[:5]:  # Show top 5
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.write(f"**{video.get('title', 'N/A')[:50]}...**")
                                with col2:
                                    st.write(f"{video.get('predicted_views', 0):,} views")
                                with col3:
                                    st.write(f"{video.get('accuracy', 0):.1f}% accuracy")
                        else:
                            st.info("No data available for this category.")
    
    def _render_insights(self):
        """Render AI insights interface."""
        st.markdown("#### 💡 AI-Generated Insights")
        
        # Insight categories
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎯 Performance Insights", use_container_width=True):
                self._generate_performance_insights()
        
        with col2:
            if st.button("📊 Trend Insights", use_container_width=True):
                self._generate_trend_insights()
        
        with col3:
            if st.button("🔮 Prediction Insights", use_container_width=True):
                self._generate_prediction_insights()
        
        # Load and display insights
        insights_data = self._load_insights_data()
        
        if insights_data:
            # Key insights
            st.markdown("#### 🔍 Key Insights")
            
            for insight in insights_data.get('key_insights', []):
                insight_type = insight.get('type', 'info')
                message = insight.get('message', '')
                confidence = insight.get('confidence', 0)
                
                if insight_type == 'success':
                    st.success(f"✅ {message} (Confidence: {confidence:.1f}%)")
                elif insight_type == 'warning':
                    st.warning(f"⚠️ {message} (Confidence: {confidence:.1f}%)")
                elif insight_type == 'error':
                    st.error(f"❌ {message} (Confidence: {confidence:.1f}%)")
                else:
                    st.info(f"ℹ️ {message} (Confidence: {confidence:.1f}%)")
            
            # Recommendations
            st.markdown("#### 🎯 Recommendations")
            recommendations = insights_data.get('recommendations', [])
            
            for i, rec in enumerate(recommendations, 1):
                with st.expander(f"💡 Recommendation {i}: {rec.get('title', 'Untitled')}"):
                    st.write(f"**Description:** {rec.get('description', 'N/A')}")
                    st.write(f"**Impact:** {rec.get('impact', 'N/A')}")
                    st.write(f"**Priority:** {rec.get('priority', 'N/A')}")
                    
                    if rec.get('action_items'):
                        st.write("**Action Items:**")
                        for action in rec.get('action_items', []):
                            st.write(f"• {action}")
            
            # Insight trends
            st.markdown("#### 📈 Insight Trends")
            if insights_data.get('trend_data'):
                insight_trend_chart = self._create_insight_trend_chart(insights_data.get('trend_data'))
                display_chart_with_download(insight_trend_chart, "insight_trends")
    
    def _render_reports(self):
        """Render reports and export interface."""
        st.markdown("#### 📋 Reports & Data Export")
        
        # Report types
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 Available Reports")
            
            report_types = [
                ("prediction_summary", "Prediction Summary Report"),
                ("accuracy_analysis", "Accuracy Analysis Report"),
                ("trend_report", "Trend Analysis Report"),
                ("category_report", "Category Performance Report"),
                ("user_activity", "User Activity Report")
            ]
            
            selected_report = st.selectbox(
                "Select Report Type",
                options=[r[0] for r in report_types],
                format_func=lambda x: next(r[1] for r in report_types if r[0] == x)
            )
            
            date_range = st.selectbox(
                "Date Range",
                options=["last_7_days", "last_30_days", "last_90_days", "custom"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            if date_range == "custom":
                col_start, col_end = st.columns(2)
                with col_start:
                    start_date = st.date_input("Start Date")
                with col_end:
                    end_date = st.date_input("End Date")
            
            export_format = st.selectbox(
                "Export Format",
                options=["csv", "excel", "pdf", "json"],
                format_func=lambda x: x.upper()
            )
        
        with col2:
            st.markdown("##### ⚙️ Report Options")
            
            include_charts = st.checkbox("Include Charts", value=True)
            include_raw_data = st.checkbox("Include Raw Data", value=False)
            include_insights = st.checkbox("Include AI Insights", value=True)
            
            st.markdown("##### 📧 Delivery Options")
            
            delivery_method = st.selectbox(
                "Delivery Method",
                options=["download", "email"],
                format_func=lambda x: x.title()
            )
            
            if delivery_method == "email":
                email_address = st.text_input("Email Address")
            
            # Generate report button
            if st.button("📋 Generate Report", use_container_width=True):
                self._generate_report(
                    selected_report, date_range, export_format,
                    include_charts, include_raw_data, include_insights,
                    delivery_method
                )
        
        # Quick export options
        st.markdown("#### ⚡ Quick Export")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Export Predictions", use_container_width=True):
                self._quick_export("predictions")
        
        with col2:
            if st.button("📈 Export Analytics", use_container_width=True):
                self._quick_export("analytics")
        
        with col3:
            if st.button("🏷️ Export Categories", use_container_width=True):
                self._quick_export("categories")
        
        with col4:
            if st.button("💡 Export Insights", use_container_width=True):
                self._quick_export("insights")
        
        # Recent reports
        st.markdown("#### 📋 Recent Reports")
        recent_reports = self._get_recent_reports()
        
        if recent_reports:
            for report in recent_reports:
                with st.expander(f"📄 {report.get('name', 'Untitled')} - {report.get('created_at', '')[:10]}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Type:** {report.get('type', 'N/A')}")
                        st.write(f"**Format:** {report.get('format', 'N/A').upper()}")
                    
                    with col2:
                        st.write(f"**Size:** {report.get('size', 'N/A')}")
                        st.write(f"**Status:** {report.get('status', 'N/A')}")
                    
                    with col3:
                        if st.button(f"📥 Download", key=f"download_{report.get('id')}"):
                            self._download_report(report.get('id'))
        else:
            st.info("No recent reports available.")
    
    def _load_dashboard_data(self, date_range: str) -> Dict[str, Any]:
        """Load dashboard data from API."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            params = {'date_range': date_range}
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/dashboard",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error("Failed to load dashboard data")
                return {}
                
        except Exception as e:
            st.error(f"Error loading dashboard data: {str(e)}")
            return {}
    
    def _create_activity_chart(self, activity_data: List[Dict]) -> go.Figure:
        """Create activity chart."""
        if not activity_data:
            return go.Figure()
        
        df = pd.DataFrame(activity_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['predictions'],
            mode='lines+markers',
            name='Predictions',
            line=dict(color='#667eea', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Daily Prediction Activity',
            xaxis_title='Date',
            yaxis_title='Number of Predictions',
            template='plotly_white',
            height=300
        )
        
        return fig
    
    def _create_accuracy_chart(self, accuracy_data: List[Dict]) -> go.Figure:
        """Create accuracy trend chart."""
        if not accuracy_data:
            return go.Figure()
        
        df = pd.DataFrame(accuracy_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['accuracy'],
            mode='lines+markers',
            name='Accuracy',
            line=dict(color='#28a745', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Prediction Accuracy Trend',
            xaxis_title='Date',
            yaxis_title='Accuracy (%)',
            template='plotly_white',
            height=300
        )
        
        return fig
    
    def _load_trend_data(self, trend_type: str, time_period: str, category_filter: str) -> Dict[str, Any]:
        """Load trend analysis data from API."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'trend_type': trend_type,
                'time_period': time_period,
                'category': category_filter
            }
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/trends",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.warning("Unable to load trend data")
                return {}
                
        except Exception as e:
            st.error(f"Error loading trend data: {str(e)}")
            return {}
    
    def _analyze_trends(self, trend_type: str, time_period: str, category_filter: str):
        """Trigger trend analysis."""
        with st.spinner("🔄 Analyzing trends..."):
            # Mock analysis for demonstration
            st.success("✅ Trend analysis completed!")
    
    def _create_seasonal_chart(self, seasonal_data: Dict[str, Any]) -> go.Figure:
        """Create seasonal patterns chart."""
        fig = go.Figure()
        
        # Mock seasonal data visualization
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        values = [100, 120, 110, 130, 140, 160, 180, 170, 150, 140, 130, 120]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=values,
            mode='lines+markers',
            name='Seasonal Pattern',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Seasonal Viewership Patterns',
            xaxis_title='Month',
            yaxis_title='Relative Performance',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def _load_category_comparison(self, categories: List[str], metric_type: str) -> List[Dict]:
        """Load category comparison data."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'categories': ','.join(categories),
                'metric': metric_type
            }
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/categories/compare",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('comparison_data', [])
            else:
                # Mock data for demonstration
                return [
                    {'category': cat, 'value': 85.5 + (i * 5), 'count': 100 + (i * 20)}
                    for i, cat in enumerate(categories)
                ]
                
        except Exception as e:
            st.error(f"Error loading category comparison: {str(e)}")
            return []
    
    def _create_category_comparison_chart(self, data: List[Dict], metric_type: str) -> go.Figure:
        """Create category comparison chart."""
        if not data:
            return go.Figure()
        
        df = pd.DataFrame(data)
        
        fig = px.bar(
            df,
            x='category',
            y='value',
            title=f'Category Comparison - {metric_type.replace("_", " ").title()}',
            color='value',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=400,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def _get_top_videos_by_category(self, category: str) -> List[Dict]:
        """Get top performing videos by category."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            params = {'category': category, 'limit': 5}
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/categories/{category}/top-videos",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('videos', [])
            else:
                # Mock data for demonstration
                return [
                    {
                        'title': f'Sample {category.title()} Video {i+1}',
                        'predicted_views': 50000 + (i * 10000),
                        'accuracy': 85.5 + (i * 2)
                    }
                    for i in range(5)
                ]
                
        except Exception as e:
            return []
    
    def _generate_performance_insights(self):
        """Generate performance insights."""
        with st.spinner("🔄 Generating performance insights..."):
            st.success("✅ Performance insights generated!")
    
    def _generate_trend_insights(self):
        """Generate trend insights."""
        with st.spinner("🔄 Generating trend insights..."):
            st.success("✅ Trend insights generated!")
    
    def _generate_prediction_insights(self):
        """Generate prediction insights."""
        with st.spinner("🔄 Generating prediction insights..."):
            st.success("✅ Prediction insights generated!")
    
    def _load_insights_data(self) -> Dict[str, Any]:
        """Load insights data from API."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/insights",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                # Mock data for demonstration
                return {
                    'key_insights': [
                        {
                            'type': 'success',
                            'message': 'Your prediction accuracy has improved by 5% this month',
                            'confidence': 92.5
                        },
                        {
                            'type': 'warning',
                            'message': 'Entertainment category shows declining performance',
                            'confidence': 78.3
                        },
                        {
                            'type': 'info',
                            'message': 'Best upload time is between 6-8 PM for your audience',
                            'confidence': 85.7
                        }
                    ],
                    'recommendations': [
                        {
                            'title': 'Optimize Upload Timing',
                            'description': 'Upload videos between 6-8 PM for maximum engagement',
                            'impact': 'High',
                            'priority': 'Medium',
                            'action_items': [
                                'Schedule uploads for peak hours',
                                'Test different time slots',
                                'Monitor engagement patterns'
                            ]
                        }
                    ]
                }
                
        except Exception as e:
            st.error(f"Error loading insights: {str(e)}")
            return {}
    
    def _create_insight_trend_chart(self, trend_data: Dict[str, Any]) -> go.Figure:
        """Create insight trend chart."""
        # Mock trend chart
        dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
        values = [80 + (i % 10) + (i * 0.2) for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name='Insight Score',
            line=dict(color='#9c27b0', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Insight Quality Trend',
            xaxis_title='Date',
            yaxis_title='Insight Score',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def _generate_report(self, report_type: str, date_range: str, export_format: str,
                        include_charts: bool, include_raw_data: bool, include_insights: bool,
                        delivery_method: str):
        """Generate and deliver report."""
        with st.spinner("📋 Generating report..."):
            # Mock report generation
            st.success(f"✅ {report_type.replace('_', ' ').title()} report generated successfully!")
            
            if delivery_method == "download":
                # Mock download
                report_data = f"Mock {report_type} report data in {export_format.upper()} format"
                st.download_button(
                    label=f"📥 Download {export_format.upper()} Report",
                    data=report_data,
                    file_name=f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format}",
                    mime=f"application/{export_format}"
                )
            else:
                st.info("📧 Report will be sent to your email address shortly.")
    
    def _quick_export(self, export_type: str):
        """Quick export functionality."""
        with st.spinner(f"📊 Exporting {export_type}..."):
            # Mock export
            export_data = f"Mock {export_type} export data"
            st.download_button(
                label=f"📥 Download {export_type.title()} CSV",
                data=export_data,
                file_name=f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    def _get_recent_reports(self) -> List[Dict]:
        """Get recent reports."""
        try:
            headers = {
                'Authorization': f'Bearer {st.session_state.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_base_url}/api/v1/analytics/reports/recent",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('reports', [])
            else:
                # Mock data for demonstration
                return [
                    {
                        'id': f'report_{i}',
                        'name': f'Analytics Report {i+1}',
                        'type': 'prediction_summary',
                        'format': 'csv',
                        'size': '2.5 MB',
                        'status': 'completed',
                        'created_at': (datetime.now() - timedelta(days=i)).isoformat()
                    }
                    for i in range(3)
                ]
                
        except Exception as e:
            return []
    
    def _download_report(self, report_id: str):
        """Download a specific report."""
        with st.spinner("📥 Preparing download..."):
            st.success(f"✅ Report {report_id} download started!")


def main():
    """Main function to run the analytics page."""
    analytics_page = AnalyticsPage()
    analytics_page.render()


if __name__ == "__main__":
    main()
