import os
import sys

# Ensure project root is on sys.path so imports like `core.*` work under Streamlit
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from stock_analysis import render_stock_analysis_page
from personal_finance import render_personal_finance_page

def display_landing_page():
    """Display the clean and simple landing page with two main options"""
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 1.2rem; background: #f8fafc; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
        <h2 style="font-size: 2rem; margin: 0; color: #1a202c; font-weight: 600;">🚀 Finance GPT</h2>
        <p style="font-size: 1.2rem; margin: 0.3rem 0 0 0; color: #4a5568;">Your AI-Powered Financial Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Options Grid

    st.markdown("---")
    st.markdown("### 🎯 Choose Your Financial Tool")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stock Analysis Card
        with st.container():
            st.markdown("""
                <div style="border: 1px solid #ccc; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
                    <h4>📊 AI Based Stock Analysis</h4>
                    <p>Comprehensive stock analysis with real-time market data, AI-driven recommendations, and advanced financial metrics visualization.</p>
                </div>
            """, unsafe_allow_html=True)

        if st.button("📊 Start Stock Analysis", key="stock_analysis_btn", use_container_width=True):
            st.session_state.current_page = "stock_analysis"
            st.rerun()
    
    with col2:       
        # Personal Finance card
        with st.container():
            st.markdown("""
                <div style="border: 1px solid #ccc; padding: 20px; border-radius: 10px; background-color: #f9f9f9;">
                    <h4>💰 Personal Finance</h4>
                    <p>AI-powered analysis of spending patterns, investment tracking, and financial insights from your email data</p>
                </div>
            """, unsafe_allow_html=True)
        if st.button("💰 Manage Personal Finance", key="personal_finance_btn", use_container_width=True):
            st.session_state.current_page = "personal_finance"
            st.rerun()
    
    st.markdown("---")
    
    # Compact Statistics Grid at the bottom
    st.markdown("### 📊 Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; border: 1px solid #e2e8f0; margin: 0.25rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="font-size: 1.5rem; font-weight: bold; color: #3182ce;">10K+</div>
            <div style="font-size: 0.8rem; color: #718096;">Stocks Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; border: 1px solid #e2e8f0; margin: 0.25rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="font-size: 1.5rem; font-weight: bold; color: #38a169;">95%</div>
            <div style="font-size: 0.8rem; color: #718096;">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; border: 1px solid #e2e8f0; margin: 0.25rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="font-size: 1.5rem; font-weight: bold; color: #d69e2e;">24/7</div>
            <div style="font-size: 0.8rem; color: #718096;">Market Monitoring</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; border: 1px solid #e2e8f0; margin: 0.25rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="font-size: 1.5rem; font-weight: bold; color: #805ad5;">AI</div>
            <div style="font-size: 0.8rem; color: #718096;">Powered</div>
        </div>
        """, unsafe_allow_html=True)

def app():
    """Main application function with clean navigation between different pages"""
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "landing"
    
    # Navigation
    if st.session_state.current_page != "landing":
        if st.button("← Back to Home", key="back_button"):
            st.session_state.current_page = "landing"
            st.rerun()
    
    # Page routing
    if st.session_state.current_page == "landing":
        display_landing_page()
    
    elif st.session_state.current_page == "stock_analysis":
        render_stock_analysis_page()
    
    elif st.session_state.current_page == "personal_finance":
        render_personal_finance_page()

if __name__ == "__main__":
    app()
