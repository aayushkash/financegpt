import sys
import os
import google.generativeai as genai
from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Fix imports for package structure
from services.data_fetcher import fetch_stock_data, fetch_financial_data, fetch_stock_news
from core.sentiment_analysis import analyze_sentiment

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_recommendation(ticker):
    stock_history, stock_info = fetch_stock_data(ticker)
    if stock_info is None:
        return "Error: No stock info available", "Could not fetch data for the given ticker."
    if 'currentPrice' in stock_info:
        price = stock_info['currentPrice']
    else:
        return "Error: Missing 'currentPrice'", f"The stock data for {ticker} does not contain the 'currentPrice'."
    
    pe_ratio = stock_info.get('trailingPE', 'N/A')
    market_cap = stock_info.get('marketCap', 'N/A')

    financial_data = fetch_financial_data(ticker)
    if financial_data is None:
        financial_data = "No financial data available."
    
    news_data = fetch_stock_news(ticker)
    # Fix typo: 'contect' -> 'content'
    combined_news_data = "\n".join(
        news_data[i]['title'] + " " + news_data[i].get('content', '') 
        for i in range(len(news_data))
    ) if isinstance(news_data, list) and news_data else "No news data available."
    combined_stock_history = stock_history.astype(str).to_string()
    
    # Optionally, extract sentiment from news
    # sentiment = analyze_sentiment(news_data) if isinstance(news_data, list) and news_data else "No Sentiment Data"

    prompt = f"""
    You are a stock recommendation expert. Use the following data to provide a recommendation on whether the stock should be a "Buy", "Sell", or "Hold":
    Provide Explanation for your recommendation based on Stock data, Financial data and Stock News. Also do sentiment analysis on the Stock News data provided. 

    Stock Data: 
    - Price: ${price}
    - P/E Ratio: {pe_ratio}
    - Market Cap: {market_cap}
    - Stock History: {combined_stock_history}

    Financial Data: {financial_data}
    
    Stock News : {combined_news_data}

    Instructions for your output:
    - Start with a clear heading  Recommendation:  "Buy", "Sell", or "Hold"
    - Provide short Explanation for your recommendation.
    """
    
    #print("Prompt to model:", prompt)
    model = genai.GenerativeModel("gemini-2.0-flash")
    recommendation = model.generate_content(prompt).text.strip()
    #print("Prompt recommendation:", recommendation)
    return recommendation

if __name__ == "__main__":
    ticker = "INFY"
    recommendation = generate_recommendation(ticker)
    print(f"Recommendation: {recommendation}")
