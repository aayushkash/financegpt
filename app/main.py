import os
import sys

# Ensure project root is on sys.path so imports like `core.*` work under Streamlit
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.utils import extract_recommendation , get_recommendation
import streamlit as st # type: ignore
from core.agent_handler import generate_recommendation
from services.data_fetcher import fetch_stock_data

def display_stock_data(ticker):
    """
    Display stock data in the Streamlit app for a given ticker.
    """
    stock_history, stock_info = fetch_stock_data(ticker)

    st.subheader( f"Stock Data : {stock_info.get('shortName', '')} ({ticker}) ")
    
    st.markdown("""
    <div style='
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        font-size: 16px;
        display: flex;
        gap: 30px;
        flex-wrap: wrap;
    '>
        <div>🏢 {sector}</div>
        <div>🏭 {industry}</div>
        <div>🌍 {country}</div>
        <div>🌐 <a href="{website}" target="_blank" style='text-decoration:none;'>{website}</a></div>
    </div>
    """.format(
        sector=stock_info.get('sectorDisp', 'N/A'),
        industry=stock_info.get('industryDisp', 'N/A'),
        country=stock_info.get('country', 'N/A'),
        website=stock_info.get('website', '#')
    ), unsafe_allow_html=True)


    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Market Data", 
        "📈 Valuation Metrics", 
        "📅 52-Week Stats", 
        "💰 Dividend Info", 
        "🧾 Financials", 
        "📅 Earnings & Growth"
    ])

    # 📊 Market Data
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Current Price:** {stock_info.get('currentPrice', 'N/A')}")
            st.markdown(f"**Open:** {stock_info.get('regularMarketOpen', 'N/A')}")
            st.markdown(f"**Day High:** {stock_info.get('dayHigh', 'N/A')}")
            st.markdown(f"**Day Low:** {stock_info.get('dayLow', 'N/A')}")
        with col2:
            st.markdown(f"**Previous Close:** {stock_info.get('previousClose', 'N/A')}")
            st.markdown(f"**Change (%):** {stock_info.get('regularMarketChangePercent', 'N/A')}%")
            st.markdown(f"**Volume:** {stock_info.get('regularMarketVolume', 'N/A')}")

    # 📈 Valuation Metrics
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Trailing P/E:** {stock_info.get('trailingPE', 'N/A')}")
            st.markdown(f"**Forward P/E:** {stock_info.get('forwardPE', 'N/A')}")
            st.markdown(f"**PEG Ratio:** {stock_info.get('pegRatio', 'N/A')}")
        with col2:
            st.markdown(f"**Price to Book:** {stock_info.get('priceToBook', 'N/A')}")
            st.markdown(f"**Beta:** {stock_info.get('beta', 'N/A')}")

    # 📅 52-Week Stats
    with tab3:
        st.markdown(f"**High:** {stock_info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.markdown(f"**Low:** {stock_info.get('fiftyTwoWeekLow', 'N/A')}")
        st.markdown(f"**Range:** {stock_info.get('fiftyTwoWeekRange', 'N/A')}")

    # 💰 Dividend Info
    with tab4:
        st.markdown(f"**Dividend Rate:** {stock_info.get('dividendRate', 'N/A')}")
        st.markdown(f"**Yield:** {stock_info.get('dividendYield', 'N/A')}")
        st.markdown(f"**Ex-Dividend Date:** {stock_info.get('exDividendDate', 'N/A')}")
        st.markdown(f"**Payout Ratio:** {stock_info.get('payoutRatio', 'N/A')}")

    # 🧾 Financials
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Total Cash:** {stock_info.get('totalCash', 'N/A')}")
            st.markdown(f"**Total Debt:** {stock_info.get('totalDebt', 'N/A')}")
            st.markdown(f"**Free Cash Flow:** {stock_info.get('freeCashflow', 'N/A')}")
        with col2:
            st.markdown(f"**ROA:** {stock_info.get('returnOnAssets', 'N/A')}")
            st.markdown(f"**ROE:** {stock_info.get('returnOnEquity', 'N/A')}")

    # 📅 Earnings & Growth
    with tab6:
        st.markdown(f"**Earnings Date:** {stock_info.get('earningsTimestamp', 'N/A')}")
        st.markdown(f"**Quarterly Earnings Growth:** {stock_info.get('earningsQuarterlyGrowth', 'N/A')}")
        st.markdown(f"**Revenue Growth:** {stock_info.get('revenueGrowth', 'N/A')}")
        st.markdown(f"**Gross Margins:** {stock_info.get('grossMargins', 'N/A')}")
        st.markdown(f"**Operating Margins:** {stock_info.get('operatingMargins', 'N/A')}")
        st.markdown(f"**Profit Margins:** {stock_info.get('profitMargins', 'N/A')}")


    # Show historical stock data (e.g., last 15 days)
    st.subheader("📊 Recent Stock History")

    with st.expander("Click to view the last 15 days of stock data"):
        st.markdown("Here’s a quick look at how the stock has moved over the last 15 trading days:")

        # Line chart for closing prices
        st.line_chart(stock_history.tail(15)[["Close"]])

        # Styled DataFrame with highlights
        st.dataframe(
            stock_history.tail(15).style
                .highlight_max(axis=0, color='lightgreen')
                .highlight_min(axis=0, color='salmon')
                .set_properties(**{'text-align': 'center'})
        )

def display_recommendation(ticker):
    raw_recommendation = generate_recommendation(ticker)
    tag_recommendation, recommendation = extract_recommendation(raw_recommendation)

    # # Display the recommendation and explanation
    with st.expander("🧠 AI Recommendation: " + str(tag_recommendation), expanded=False):
        st.markdown("""
        <div style='
            background-color: #f0f4fc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            font-size: 18px;
        '>
            <p><strong>📌 Recommendation:</strong> {recommendation}</p>
        </div>
        """.format(
            ticker=ticker,
            recommendation=recommendation
        ), unsafe_allow_html=True)

def app():
    st.header("AI-Powered Stock Recommendation")
    st.sidebar.header("Stock Ticker Input")
    st.sidebar.markdown("Enter Stock Ticker:")
    st.sidebar.markdown("*(e.g. GOOG, INFY, HDB, WIT, AAPL, YTRA ...)*")
    ticker = st.sidebar.text_input(
        "Stock Ticker", 
        label_visibility="collapsed"
    )

    if ticker:
        display_stock_data(ticker)
        display_recommendation(ticker)
    else:
        st.write("Please enter a valid stock ticker in the sidebar.")

if __name__ == "__main__":
    app()
