import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv 
import os
from core.gmail_agent import build_gmail_search_query,summarize_financial_data, get_gmail_data
import re
from datetime import datetime

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def format_financial_summary(summary_text):
    """Format the financial summary in a structured, readable way"""
    
    # Split the summary into lines and process each section
    lines = summary_text.split('\n')
    formatted_html = ""
    
    # Track if we're inside a section
    in_bse_trades = False
    in_investments = False
    in_spends = False
    
    # Track if sections have been created to prevent duplicates
    bse_section_created = False
    investments_section_created = False
    spends_section_created = False
    
    # Collect all transactions for better categorization
    bse_transactions = []
    investment_transactions = []
    spend_transactions = []
    
    # Track total spends for calculation
    total_spends = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for section headers and start sections
        if 'BSE Trades' in line or '📊 BSE Trades' in line or 'bse trade' in line.lower():
            if not bse_section_created:
                formatted_html += '<div style="margin: 1.5rem 0;"><h4 style="color: #3182ce; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">📊 BSE Trades</h4>'
                bse_section_created = True
            in_bse_trades = True
            in_investments = False
            in_spends = False
        elif 'Investments' in line or '🏦 Investments' in line or 'investment' in line.lower():
            if not investments_section_created:
                formatted_html += '<div style="margin: 1.5rem 0;"><h4 style="color: #38a169; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">🏦 Investments</h4>'
                investments_section_created = True
            in_bse_trades = False
            in_investments = True
            in_spends = False
        elif 'Spends' in line or '💳 Spends' in line or 'Spending' in line or 'spend' in line.lower():
            if not spends_section_created:
                formatted_html += '<div style="margin: 1.5rem 0;"><h4 style="color: #d69e2e; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">💳 Spends</h4>'
                spends_section_created = True
            in_bse_trades = False
            in_investments = False
            in_spends = True
        elif 'Total Spends' in line or '💰 Total Spends' in line or 'total spend' in line.lower():
            # Extract the amount from the total spends line
            amount_match = re.search(r'₹?([\d,]+\.?\d*)', line)
            if amount_match:
                total_amount = amount_match.group(1).replace(',', '')
                try:
                    total_spends = float(total_amount)
                except:
                    pass
            
            in_bse_trades = False
            in_investments = False
            in_spends = False
        elif line.startswith('•') or line.startswith('-') or 'Date:' in line or 'date:' in line:
            # Format transaction lines with standardized date format
            formatted_line = standardize_date_format(line)
            formatted_html += f'<div style="margin: 0.5rem 0; color: #374151; font-size: 0.95rem;">{formatted_line}</div>'
        elif 'No' in line and 'found' in line:
            # Format "No [Category] found" messages
            formatted_html += f'<div style="padding: 0.75rem; margin: 0.5rem 0; background: #fef5e7; border-radius: 6px; border-left: 3px solid #f59e0b; color: #92400e; font-style: italic;">{line}</div>'
        elif any(keyword in line.lower() for keyword in ['swiggy', 'flipkart', 'payment', 'debit', 'order', 'bill', 'purchase', 'taxi', 'meal', 'food', 'electricity', 'google pay', 'zomato', 'uber', 'ola', 'amazon', 'myntra', 'hotel', 'restaurant']):
            # This looks like a spend transaction - add it to spends section if not already in one
            if not spends_section_created:
                formatted_html += '<div style="margin: 1.5rem 0;"><h4 style="color: #d69e2e; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">💳 Spends</h4>'
                spends_section_created = True
                in_spends = True
            
            # Extract amount for total calculation
            amount_match = re.search(r'₹?([\d,]+\.?\d*)', line)
            if amount_match:
                try:
                    amount = float(amount_match.group(1).replace(',', ''))
                    total_spends += amount
                    spend_transactions.append((line, amount))
                except:
                    pass
            
            formatted_line = standardize_date_format(line)
            formatted_html += f'<div style="margin: 0.5rem 0; color: #374151; font-size: 0.95rem;">{formatted_line}</div>'
        elif '₹' in line and any(keyword in line.lower() for keyword in ['swiggy', 'flipkart', 'payment', 'debit', 'order', 'bill', 'purchase', 'taxi', 'meal', 'food', 'electricity', 'google pay', 'zomato', 'uber', 'ola', 'amazon', 'myntra', 'hotel', 'restaurant']):
            # Additional check for spend transactions with rupee symbol
            if not spends_section_created:
                formatted_html += '<div style="margin: 1.5rem 0;"><h4 style="color: #d69e2e; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">💳 Spends</h4>'
                spends_section_created = True
                in_spends = True
            
            # Extract amount for total calculation
            amount_match = re.search(r'₹?([\d,]+\.?\d*)', line)
            if amount_match:
                try:
                    amount = float(amount_match.group(1).replace(',', ''))
                    total_spends += amount
                    spend_transactions.append((line, amount))
                except:
                    pass
            
            formatted_line = standardize_date_format(line)
            formatted_html += f'<div style="margin: 0.5rem 0; color: #374151; font-size: 0.95rem;">{formatted_line}</div>'
        else:
            # Regular text lines
            formatted_html += f'<div style="margin: 0.5rem 0; color: #4a5568; font-size: 0.9rem;">{line}</div>'
    
    return formatted_html

def standardize_date_format(line):
    """Standardize date format in transaction lines to 'May 28, 2025' format"""
    
    # Look for various date patterns and standardize them to "Month DD, YYYY" format
    
    # Pattern 1: YYYY-MM-DD (e.g., 2025-05-28)
    def convert_iso_date(match):
        try:
            date_obj = datetime.strptime(match.group(0), '%Y-%m-%d')
            return date_obj.strftime('%B %d, %Y')
        except:
            return match.group(0)
    
    line = re.sub(r'\d{4}-\d{2}-\d{2}', convert_iso_date, line)
    
    # Pattern 2: DD/MM/YYYY (e.g., 28/05/2025)
    def convert_slash_date(match):
        try:
            day, month, year = match.groups()
            date_obj = datetime(int(year), int(month), int(day))
            return date_obj.strftime('%B %d, %Y')
        except:
            return match.group(0)
    
    line = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', convert_slash_date, line)
    
    # Pattern 3: DD-MM-YYYY (e.g., 28-05-2025)
    def convert_dash_date(match):
        try:
            day, month, year = match.groups()
            date_obj = datetime(int(year), int(month), int(day))
            return date_obj.strftime('%B %d, %Y')
        except:
            return match.group(0)
    
    line = re.sub(r'(\d{1,2})-(\d{1,2})-(\d{4})', convert_dash_date, line)
    
    # Pattern 4: DD Month YYYY (e.g., 28 May 2025) - already in correct format, just add comma
    line = re.sub(r'(\d{1,2})\s+(\w+)\s+(\d{4})', r'\2 \1, \3', line)
    
    # Pattern 5: Month DD YYYY (e.g., May 28 2025) - add comma
    line = re.sub(r'(\w+)\s+(\d{1,2})\s+(\d{4})', r'\1 \2, \3', line)
    
    return line

def render_personal_finance_page():
    """Display the personal finance management interface with simple styling"""
    
    # Compact header
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 1.2rem; background: #f8fafc; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
        <h2 style="color: #1a202c; margin: 0; font-size: 1.8rem; font-weight: 600;">💰 AI-Powered Personal Finance Management</h1>
        <p style="color: #4a5568; margin: 0.3rem 0 0 0; font-size: 1.2rem;">Transform your financial emails into actionable insights</p>
    </div>
    """, unsafe_allow_html=True)

    
    # Compact feature highlights
    col1, col2, col3 = st.columns(3)
    
    # Define a common card style template
    card_html = """
    <div style="height: 170px; display: flex; flex-direction: column; justify-content: center; align-items: center;
                padding: 1rem; background: white; border-radius: 10px; border: 1px solid #e2e8f0;
                margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h4 style="color: #2d3748; margin: 0; font-size: 1.2rem;">{title}</h4>
        <p style="color: #718096; font-size: 0.8rem; margin: 0.50rem 0 0 0; text-align: center;">{description}</p>
    </div>
    """

    # Render each card using the shared template
    with col1:
        st.markdown(card_html.format(
            icon="📈",
            title="BSE Trades",
            description="Track stock transactions and portfolio performance"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(card_html.format(
            icon="🏦",
            title="Investments",
            description="Monitor mutual funds and SIP activities"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(card_html.format(
            icon="💳",
            title="Spending",
            description="Analyze expenses and payment patterns"
        ), unsafe_allow_html=True)


    st.markdown("---")
    
    # Compact analysis section
    st.markdown("""
    <div style='text-align: left;'>
        <span style='font-size: 1.5rem; font-weight: bold;'>🔍 Financial Email Analysis</span>
        <span style='font-size: 0.9rem; color: #718096;'>(Ask questions about your financial data and get AI-powered insights)</span>
    </div> """, unsafe_allow_html=True)
    
    # Sample email snippets for demonstration
    sample_email_snippets = get_gmail_data()
    
    user_query = st.text_area(
        "What would you like to analyze?",
        value="financial data for BSE Trades, Investments and spends for this month",
        height=80,
        placeholder="e.g., Show me all my expenses this month, Analyze my investment portfolio, etc."
    )
    
    if st.button("🔍 Analyze Financial Data", key="analyze_finance", use_container_width=True):
        if user_query.strip():
            with st.spinner("🤖 AI is analyzing your financial data..."):
                # Generate Gmail search query
                gmail_search_query = build_gmail_search_query(user_query)
                
                # Analyze financial data
                financial_summary = summarize_financial_data(user_query, sample_email_snippets)
                
                # Display results with compact styling
                st.markdown("""
                <div style="background: #f0f9ff; border-radius: 15px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #bae6fd;">
                    <h3 style="color: #0c4a6e; margin: 0 0 1rem 0; text-align: center;">📊 Financial Analysis Results</h3>
                    <div style="background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <p style="margin: 0; color: #0c4a6e;"><strong>Gmail Search Query:</strong></p>
                        <code style="background: #f1f5f9; padding: 0.5rem; border-radius: 5px; display: block; margin: 0.5rem 0; color: #1e293b;">{query}</code>
                    </div>
                </div>
                """.format(query=gmail_search_query), unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: #f8fafc; border-radius: 15px; padding: 2rem; margin: 1rem 0; border: 2px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <h3 style="color: #1a202c; margin: 0 0 1.5rem 0; text-align: center; font-size: 1.6rem; font-weight: 600; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">💰 Financial Summary</h3>
                    <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        {formatted_summary}
                    </div>
                </div>
                """.format(formatted_summary=format_financial_summary(financial_summary)), unsafe_allow_html=True)
        else:
            st.error("Please enter a query to analyze.")
