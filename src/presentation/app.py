"""
Main Streamlit Application

This is the main entry point for the ViewTrendsSL Streamlit web application.

Author: ViewTrendsSL Team
Date: 2025
"""

import streamlit as st
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.presentation.pages.home import HomePage
from src.presentation.pages.prediction import PredictionPage
from src.presentation.pages.analytics import AnalyticsPage
from src.presentation.pages.auth import AuthPage


def main():
    """Main application entry point."""
    
    # Configure the main page
    st.set_page_config(
        page_title="ViewTrendsSL - YouTube Viewership Forecasting",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/L0rd008/ViewTrendsSL/discussions',
            'Report a bug': 'https://github.com/L0rd008/ViewTrendsSL/issues',
            'About': """
            # ViewTrendsSL
            
            YouTube Viewership Forecasting for Sri Lankan Audience
            
            **Version:** 1.0.0  
            **Team:** University of Moratuwa - CS3501 Project  
            **GitHub:** https://github.com/L0rd008/ViewTrendsSL
            
            This application uses advanced machine learning models to predict 
            YouTube video viewership specifically for the Sri Lankan audience.
            """
        }
    )
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("# 🎬 ViewTrendsSL")
        st.markdown("---")
        
        # Check if user is logged in
        is_logged_in = 'access_token' in st.session_state
        user_info = st.session_state.get('user_info', {})
        
        if is_logged_in:
            st.success(f"👋 Welcome, {user_info.get('name', 'User')}!")
            st.markdown(f"**Email:** {user_info.get('email', 'N/A')}")
            st.markdown(f"**Account:** {user_info.get('account_type', 'Free').title()}")
            st.markdown("---")
        
        # Navigation menu
        st.markdown("## 📋 Navigation")
        
        # Home
        if st.button("🏠 Home", use_container_width=True, 
                    type="primary" if st.session_state.current_page == 'home' else "secondary"):
            st.session_state.current_page = 'home'
            st.rerun()
        
        # Authentication
        if not is_logged_in:
            if st.button("🔐 Login", use_container_width=True,
                        type="primary" if st.session_state.current_page == 'auth' else "secondary"):
                st.session_state.current_page = 'auth'
                st.rerun()
        
        # Main features (require login)
        if is_logged_in:
            if st.button("🔮 Predictions", use_container_width=True,
                        type="primary" if st.session_state.current_page == 'prediction' else "secondary"):
                st.session_state.current_page = 'prediction'
                st.rerun()
            
            if st.button("📊 Analytics", use_container_width=True,
                        type="primary" if st.session_state.current_page == 'analytics' else "secondary"):
                st.session_state.current_page = 'analytics'
                st.rerun()
        else:
            # Show disabled buttons for non-logged in users
            st.button("🔮 Predictions", use_container_width=True, disabled=True, 
                     help="Please log in to access predictions")
            st.button("📊 Analytics", use_container_width=True, disabled=True,
                     help="Please log in to access analytics")
        
        st.markdown("---")
        
        # User actions
        if is_logged_in:
            st.markdown("## ⚙️ Account")
            
            if st.button("👤 Profile", use_container_width=True):
                st.info("Profile management coming soon!")
            
            if st.button("🚪 Logout", use_container_width=True):
                # Clear session state
                for key in ['access_token', 'refresh_token', 'user_info']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.current_page = 'home'
                st.success("✅ Logged out successfully!")
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("### 🔗 Quick Links")
        st.markdown("""
        - [📚 Documentation](https://github.com/L0rd008/ViewTrendsSL)
        - [🐛 Report Issues](https://github.com/L0rd008/ViewTrendsSL/issues)
        - [💬 Discussions](https://github.com/L0rd008/ViewTrendsSL/discussions)
        - [📧 Contact](mailto:support@viewtrendssl.com)
        """)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.8em; color: #666;">
            <p>© 2025 ViewTrendsSL Team<br>
            University of Moratuwa<br>
            CS3501 Project</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    current_page = st.session_state.current_page
    
    try:
        if current_page == 'home':
            home_page = HomePage()
            home_page.render()
        
        elif current_page == 'auth':
            auth_page = AuthPage()
            auth_page.render()
        
        elif current_page == 'prediction':
            if is_logged_in:
                prediction_page = PredictionPage()
                prediction_page.render()
            else:
                st.warning("🔒 Please log in to access predictions.")
                if st.button("🚪 Go to Login"):
                    st.session_state.current_page = 'auth'
                    st.rerun()
        
        elif current_page == 'analytics':
            if is_logged_in:
                analytics_page = AnalyticsPage()
                analytics_page.render()
            else:
                st.warning("🔒 Please log in to access analytics.")
                if st.button("🚪 Go to Login"):
                    st.session_state.current_page = 'auth'
                    st.rerun()
        
        else:
            st.error("❌ Page not found!")
            st.session_state.current_page = 'home'
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")
        
        # Show error details in development
        if os.getenv('ENVIRONMENT', 'development') == 'development':
            with st.expander("🔍 Error Details (Development Mode)"):
                st.exception(e)


if __name__ == "__main__":
    main()
