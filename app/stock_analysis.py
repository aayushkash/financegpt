import streamlit as st
from core.utils import extract_recommendation
from core.agent_handler import generate_recommendation
from services.data_fetcher import fetch_stock_data

def display_stock_data(ticker):
    """Display stock data in the Streamlit app for a given ticker."""
    stock_history, stock_info = fetch_stock_data(ticker)

    # Simple header
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 15px; margin: 1rem 0; border: 1px solid #e2e8f0;">
        <h1 style="font-size: 2.5rem; margin: 0; color: #1a202c; font-weight: 600;">📊 {stock_info.get('shortName', '')}</h1>
        <p style="font-size: 1.3rem; margin: 0.5rem 0 0 0; color: #4a5568;">({ticker}) - AI-Powered Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple company info card
    st.markdown("""
    <div style='
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    '>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="text-align: center; padding: 0.75rem; background: #f7fafc; border-radius: 8px; border: 1px solid #e2e8f0;">🏢 <strong>Sector:</strong> {sector}</div>
            <div style="text-align: center; padding: 0.75rem; background: #f7fafc; border-radius: 8px; border: 1px solid #e2e8f0;">🏭 <strong>Industry:</strong> {industry}</div>
            <div style="text-align: center; padding: 0.75rem; background: #f7fafc; border-radius: 8px; border: 1px solid #e2e8f0;">🌍 <strong>Country:</strong> {country}</div>
            <div style="text-align: center; padding: 0.75rem; background: #f7fafc; border-radius: 8px; border: 1px solid #e2e8f0;">🌐 <strong>Website:</strong> <a href="{website}" target="_blank" style="color: #3182ce;">{website}</a></div>
        </div>
    </div>
    """.format(
        sector=stock_info.get('sectorDisp', 'N/A'),
        industry=stock_info.get('industryDisp', 'N/A'),
        country=stock_info.get('country', 'N/A'),
        website=stock_info.get('website', '#')
    ), unsafe_allow_html=True)

    # Simple tabs
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
            st.markdown("""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                <h4 style="color: #2d3748; margin: 0 0 1rem 0;">📈 Price Information</h4>
                <p style="margin: 0.5rem 0;"><strong>Current Price:</strong> <span style="color: #3182ce; font-weight: bold;">{current_price}</span></p>
                <p style="margin: 0.5rem 0;"><strong>Open:</strong> {open_price}</p>
                <p style="margin: 0.5rem 0;"><strong>Day High:</strong> {day_high}</p>
                <p style="margin: 0.5rem 0;"><strong>Day Low:</strong> {day_low}</p>
            </div>
            """.format(
                current_price=stock_info.get('currentPrice', 'N/A'),
                open_price=stock_info.get('regularMarketOpen', 'N/A'),
                day_high=stock_info.get('dayHigh', 'N/A'),
                day_low=stock_info.get('dayLow', 'N/A')
            ), unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                <h4 style="color: #2d3748; margin: 0 0 1rem 0;">📊 Market Stats</h4>
                <p style="margin: 0.5rem 0;"><strong>Previous Close:</strong> {prev_close}</p>
                <p style="margin: 0.5rem 0;"><strong>Change (%):</strong> <span style="color: #3182ce; font-weight: bold;">{change_pct}%</span></p>
                <p style="margin: 0.5rem 0;"><strong>Volume:</strong> {volume}</p>
            </div>
            """.format(
                prev_close=stock_info.get('previousClose', 'N/A'),
                change_pct=stock_info.get('regularMarketChangePercent', 'N/A'),
                volume=stock_info.get('regularMarketVolume', 'N/A')
            ), unsafe_allow_html=True)

    # 📈 Valuation Metrics
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                <h4 style="color: #2d3748; margin: 0 0 1rem 0;">📊 P/E Ratios</h4>
                <p style="margin: 0.5rem 0;"><strong>Trailing P/E:</strong> {trailing_pe}</p>
                <p style="margin: 0.5rem 0;"><strong>Forward P/E:</strong> {forward_pe}</p>
                <p style="margin: 0.5rem 0;"><strong>PEG Ratio:</strong> {peg_ratio}</p>
            </div>
            """.format(
                trailing_pe=stock_info.get('trailingPE', 'N/A'),
                forward_pe=stock_info.get('forwardPE', 'N/A'),
                peg_ratio=stock_info.get('pegRatio', 'N/A')
            ), unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                <h4 style="color: #2d3748; margin: 0 0 1rem 0;">📈 Other Metrics</h4>
                <p style="margin: 0.5rem 0;"><strong>Price to Book:</strong> {ptb}</p>
                <p style="margin: 0.5rem 0;"><strong>Beta:</strong> {beta}</p>
            </div>
            """.format(
                ptb=stock_info.get('priceToBook', 'N/A'),
                beta=stock_info.get('beta', 'N/A')
            ), unsafe_allow_html=True)

    # 📅 52-Week Stats
    with tab3:
        st.markdown("""
        <div style="background: #f7fafc; padding: 2rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
            <h3 style="color: #2d3748; margin: 0 0 1.5rem 0; text-align: center;">📅 52-Week Performance</h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">High</div>
                    <div style="font-size: 1.2rem;">{high}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Low</div>
                    <div style="font-size: 1.2rem;">{low}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Range</div>
                    <div style="font-size: 1.2rem;">{range_val}</div>
                </div>
            </div>
        </div>
        """.format(
            high=stock_info.get('fiftyTwoWeekHigh', 'N/A'),
            low=stock_info.get('fiftyTwoWeekLow', 'N/A'),
            range_val=stock_info.get('fiftyTwoWeekRange', 'N/A')
        ), unsafe_allow_html=True)

    # 💰 Dividend Info
    with tab4:
        st.markdown("""
        <div style="background: #f7fafc; padding: 2rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
            <h3 style="color: #2d3748; margin: 0 0 1.5rem 0; text-align: center;">💰 Dividend Information</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Dividend Rate</div>
                    <div style="font-size: 1.2rem;">{div_rate}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Yield</div>
                    <div style="font-size: 1.2rem;">{div_yield}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Ex-Dividend Date</div>
                    <div style="font-size: 1.2rem;">{ex_div_date}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Payout Ratio</div>
                    <div style="font-size: 1.2rem;">{payout_ratio}</div>
                </div>
            </div>
        </div>
        """.format(
            div_rate=stock_info.get('dividendRate', 'N/A'),
            div_yield=stock_info.get('dividendYield', 'N/A'),
            ex_div_date=stock_info.get('exDividendDate', 'N/A'),
            payout_ratio=stock_info.get('payoutRatio', 'N/A')
        ), unsafe_allow_html=True)

    # 🧾 Financials
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                <h4 style="color: #2d3748; margin: 0 0 1rem 0;">💵 Cash & Debt</h4>
                <p style="margin: 0.5rem 0;"><strong>Total Cash:</strong> {total_cash}</p>
                <p style="margin: 0.5rem 0;"><strong>Total Debt:</strong> {total_debt}</p>
                <p style="margin: 0.5rem 0;"><strong>Free Cash Flow:</strong> {fcf}</p>
            </div>
            """.format(
                total_cash=stock_info.get('totalCash', 'N/A'),
                total_debt=stock_info.get('totalDebt', 'N/A'),
                fcf=stock_info.get('freeCashflow', 'N/A')
            ), unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                <h4 style="color: #2d3748; margin: 0 0 1rem 0;">📊 Returns</h4>
                <p style="margin: 0.5rem 0;"><strong>ROA:</strong> {roa}</p>
                <p style="margin: 0.5rem 0;"><strong>ROE:</strong> {roe}</p>
            </div>
            """.format(
                roa=stock_info.get('returnOnAssets', 'N/A'),
                roe=stock_info.get('returnOnEquity', 'N/A')
            ), unsafe_allow_html=True)

    # 📅 Earnings & Growth
    with tab6:
        st.markdown("""
        <div style="background: #f7fafc; padding: 2rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
            <h3 style="color: #2d3748; margin: 0 0 1.5rem 0; text-align: center;">📈 Growth Metrics</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Earnings Date</div>
                    <div>{earnings_date}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Quarterly Growth</div>
                    <div>{qtr_growth}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Revenue Growth</div>
                    <div>{revenue_growth}</div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-weight: bold; color: #3182ce;">Gross Margins</div>
                    <div>{gross_margins}</div>
                </div>
            </div>
        </div>
        """.format(
            earnings_date=stock_info.get('earningsTimestamp', 'N/A'),
            qtr_growth=stock_info.get('earningsQuarterlyGrowth', 'N/A'),
            revenue_growth=stock_info.get('revenueGrowth', 'N/A'),
            gross_margins=stock_info.get('grossMargins', 'N/A')
        ), unsafe_allow_html=True)

    # Simple historical stock data section
    st.markdown("""
    <div style="background: #f7fafc; padding: 2rem; border-radius: 15px; margin: 2rem 0; border: 1px solid #e2e8f0;">
        <h3 style="color: #2d3748; margin: 0 0 1.5rem 0; text-align: center;">📊 Recent Stock History</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📈 Click to view the last 15 days of stock data", expanded=False):
        st.markdown("Here's a quick look at how the stock has moved over the last 15 trading days:")

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
    """Display AI recommendation with simple styling"""
    
    # Show loading message while AI is analyzing
    with st.spinner("🤖 AI is analyzing your stock data..."):
        raw_recommendation = generate_recommendation(ticker)
        tag_recommendation, recommendation = extract_recommendation(raw_recommendation)

    with st.expander("🧠 AI Recommendation: " + str(tag_recommendation), expanded=False):
        st.markdown("""
        <div style="
            background: #f0f9ff;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #bae6fd;
            color: #0c4a6e;
        ">
            <h4 style="margin: 0 0 1rem 0; text-align: center;">🤖 AI Analysis Result</h4>
            <p style="font-size: 1.1rem; line-height: 1.6; margin: 0; text-align: center;">
                <strong>📌 Recommendation:</strong> {recommendation}
            </p>
        </div>
        """.format(
            ticker=ticker,
            recommendation=recommendation
        ), unsafe_allow_html=True)

def render_stock_analysis_page():
    """Render the complete stock analysis page"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 15px; margin: 1rem 0; border: 1px solid #e2e8f0;">
        <h1 style="font-size: 2.5rem; margin: 0; color: #1a202c; font-weight: 600;">📊 AI-Powered Stock Analysis</h1>
        <p style="font-size: 1.2rem; margin: 1rem 0 0 0; color: #4a5568;">Get comprehensive insights into any stock with AI-driven recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock analysis interface
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f7fafc; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #e2e8f0;">
        <h3 style="margin: 0; color: #2d3748;">🔍 Stock Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("**Enter Stock Ticker:**")
    st.sidebar.markdown("*(e.g. GOOG, INFY, HDB, WIT, AAPL, YTRA ...)*")
    
    ticker = st.sidebar.text_input(
        "Stock Ticker", 
        label_visibility="collapsed",
        placeholder="Enter ticker symbol..."
    )

    if ticker:
        display_stock_data(ticker)
        display_recommendation(ticker)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8fafc; border-radius: 15px; margin: 2rem 0; border: 1px solid #e2e8f0;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h2 style="color: #2d3748; margin: 1rem 0;">Ready to Analyze Stocks?</h2>
            <p style="color: #4a5568; margin: 1rem 0; font-size: 1.1rem;">
                Enter a stock ticker symbol in the sidebar to get started with comprehensive AI-powered analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
