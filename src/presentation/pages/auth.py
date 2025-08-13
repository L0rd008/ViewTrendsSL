"""
Authentication Page

This module provides user authentication functionality for the ViewTrendsSL web application.

Author: ViewTrendsSL Team
Date: 2025
"""

import streamlit as st
import requests
import json
from typing import Dict, Any, Optional
import re


class AuthPage:
    """Authentication page functionality for ViewTrendsSL."""
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
    
    def render(self):
        """Render the authentication page."""
        st.set_page_config(
            page_title="Login - ViewTrendsSL",
            page_icon="🔐",
            layout="centered"
        )
        
        self._render_header()
        
        # Check if user is already logged in
        if 'access_token' in st.session_state:
            self._render_already_logged_in()
            return
        
        # Main authentication interface
        auth_mode = st.session_state.get('auth_mode', 'login')
        
        if auth_mode == 'login':
            self._render_login_form()
        elif auth_mode == 'register':
            self._render_register_form()
        elif auth_mode == 'forgot_password':
            self._render_forgot_password_form()
    
    def _render_header(self):
        """Render the page header."""
        st.markdown("""
        <style>
        .auth-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .auth-form {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            max-width: 400px;
            margin: 0 auto;
        }
        .auth-switch {
            text-align: center;
            margin-top: 1rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="auth-header">
            <h1>🔐 ViewTrendsSL</h1>
            <p>Sign in to access YouTube viewership forecasting</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_already_logged_in(self):
        """Render already logged in interface."""
        st.success("✅ You are already logged in!")
        
        # User info
        user_info = st.session_state.get('user_info', {})
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info(f"**Welcome back, {user_info.get('name', 'User')}!**")
            st.write(f"Email: {user_info.get('email', 'N/A')}")
            st.write(f"Account Type: {user_info.get('account_type', 'Free').title()}")
            
            # Navigation buttons
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🏠 Go to Home", use_container_width=True):
                    st.switch_page("pages/home.py")
            
            with col_b:
                if st.button("🔮 Make Prediction", use_container_width=True):
                    st.switch_page("pages/prediction.py")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                self._handle_logout()
    
    def _render_login_form(self):
        """Render login form."""
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        
        st.markdown("### 🔑 Sign In")
        
        with st.form("login_form"):
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                help="Enter your registered email address"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                help="Enter your account password"
            )
            
            remember_me = st.checkbox("Remember me", value=True)
            
            login_button = st.form_submit_button("🔑 Sign In", use_container_width=True)
        
        if login_button:
            if email and password:
                self._handle_login(email, password, remember_me)
            else:
                st.error("❌ Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auth mode switches
        self._render_auth_switches()
    
    def _render_register_form(self):
        """Render registration form."""
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        
        st.markdown("### 📝 Create Account")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input(
                    "First Name",
                    placeholder="John",
                    help="Enter your first name"
                )
            
            with col2:
                last_name = st.text_input(
                    "Last Name",
                    placeholder="Doe",
                    help="Enter your last name"
                )
            
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                help="Enter a valid email address"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a strong password",
                help="Password must be at least 8 characters long"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password",
                help="Re-enter your password"
            )
            
            # Terms and conditions
            agree_terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy",
                help="You must agree to continue"
            )
            
            # Newsletter subscription
            subscribe_newsletter = st.checkbox(
                "Subscribe to newsletter for updates and insights",
                value=True
            )
            
            register_button = st.form_submit_button("📝 Create Account", use_container_width=True)
        
        if register_button:
            if self._validate_registration_form(
                first_name, last_name, email, password, confirm_password, agree_terms
            ):
                self._handle_registration(
                    first_name, last_name, email, password, subscribe_newsletter
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auth mode switches
        self._render_auth_switches()
    
    def _render_forgot_password_form(self):
        """Render forgot password form."""
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        
        st.markdown("### 🔄 Reset Password")
        st.info("Enter your email address and we'll send you a link to reset your password.")
        
        with st.form("forgot_password_form"):
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                help="Enter your registered email address"
            )
            
            reset_button = st.form_submit_button("📧 Send Reset Link", use_container_width=True)
        
        if reset_button:
            if email and self._validate_email(email):
                self._handle_forgot_password(email)
            else:
                st.error("❌ Please enter a valid email address")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auth mode switches
        self._render_auth_switches()
    
    def _render_auth_switches(self):
        """Render authentication mode switches."""
        st.markdown('<div class="auth-switch">', unsafe_allow_html=True)
        
        current_mode = st.session_state.get('auth_mode', 'login')
        
        if current_mode == 'login':
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📝 Create Account", use_container_width=True):
                    st.session_state.auth_mode = 'register'
                    st.rerun()
            
            with col2:
                if st.button("🔄 Forgot Password?", use_container_width=True):
                    st.session_state.auth_mode = 'forgot_password'
                    st.rerun()
        
        elif current_mode == 'register':
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔑 Sign In", use_container_width=True):
                    st.session_state.auth_mode = 'login'
                    st.rerun()
            
            with col2:
                if st.button("🔄 Forgot Password?", use_container_width=True):
                    st.session_state.auth_mode = 'forgot_password'
                    st.rerun()
        
        elif current_mode == 'forgot_password':
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔑 Sign In", use_container_width=True):
                    st.session_state.auth_mode = 'login'
                    st.rerun()
            
            with col2:
                if st.button("📝 Create Account", use_container_width=True):
                    st.session_state.auth_mode = 'register'
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        if len(password) < 8:
            return False
        
        # Check for at least one uppercase, lowercase, digit, and special character
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return has_upper and has_lower and has_digit and has_special
    
    def _validate_registration_form(self, first_name: str, last_name: str, email: str,
                                  password: str, confirm_password: str, agree_terms: bool) -> bool:
        """Validate registration form data."""
        if not all([first_name, last_name, email, password, confirm_password]):
            st.error("❌ Please fill in all required fields")
            return False
        
        if not self._validate_email(email):
            st.error("❌ Please enter a valid email address")
            return False
        
        if not self._validate_password(password):
            st.error("❌ Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character")
            return False
        
        if password != confirm_password:
            st.error("❌ Passwords do not match")
            return False
        
        if not agree_terms:
            st.error("❌ You must agree to the Terms of Service and Privacy Policy")
            return False
        
        return True
    
    def _handle_login(self, email: str, password: str, remember_me: bool):
        """Handle login request."""
        try:
            with st.spinner("🔄 Signing in..."):
                payload = {
                    'email': email,
                    'password': password,
                    'remember_me': remember_me
                }
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/auth/login",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Store authentication data
                    st.session_state.access_token = data.get('access_token')
                    st.session_state.refresh_token = data.get('refresh_token')
                    st.session_state.user_info = data.get('user')
                    
                    st.success("✅ Login successful!")
                    st.balloons()
                    
                    # Redirect to home page
                    st.switch_page("pages/home.py")
                
                elif response.status_code == 401:
                    st.error("❌ Invalid email or password")
                elif response.status_code == 429:
                    st.error("⏰ Too many login attempts. Please try again later.")
                else:
                    error_msg = response.json().get('error', 'Login failed')
                    st.error(f"❌ {error_msg}")
                    
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection error. Please check your internet connection.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _handle_registration(self, first_name: str, last_name: str, email: str,
                           password: str, subscribe_newsletter: bool):
        """Handle registration request."""
        try:
            with st.spinner("📝 Creating account..."):
                payload = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': password,
                    'subscribe_newsletter': subscribe_newsletter
                }
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/auth/register",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 201:
                    st.success("✅ Account created successfully!")
                    st.info("📧 Please check your email to verify your account.")
                    
                    # Switch to login mode
                    st.session_state.auth_mode = 'login'
                    st.rerun()
                
                elif response.status_code == 409:
                    st.error("❌ An account with this email already exists")
                else:
                    error_msg = response.json().get('error', 'Registration failed')
                    st.error(f"❌ {error_msg}")
                    
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection error. Please check your internet connection.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _handle_forgot_password(self, email: str):
        """Handle forgot password request."""
        try:
            with st.spinner("📧 Sending reset link..."):
                payload = {'email': email}
                
                response = requests.post(
                    f"{self.api_base_url}/api/v1/auth/forgot-password",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.success("✅ Password reset link sent!")
                    st.info("📧 Please check your email for the reset link.")
                elif response.status_code == 404:
                    st.error("❌ No account found with this email address")
                else:
                    error_msg = response.json().get('error', 'Failed to send reset link')
                    st.error(f"❌ {error_msg}")
                    
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection error. Please check your internet connection.")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    def _handle_logout(self):
        """Handle logout request."""
        try:
            # Clear session state
            if 'access_token' in st.session_state:
                del st.session_state.access_token
            if 'refresh_token' in st.session_state:
                del st.session_state.refresh_token
            if 'user_info' in st.session_state:
                del st.session_state.user_info
            
            # Reset auth mode
            st.session_state.auth_mode = 'login'
            
            st.success("✅ Logged out successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error during logout: {str(e)}")


def main():
    """Main function to run the authentication page."""
    auth_page = AuthPage()
    auth_page.render()


if __name__ == "__main__":
    main()
