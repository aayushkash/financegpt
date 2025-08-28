import yfinance as yf 
from alpha_vantage.fundamentaldata import FundamentalData 
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker):
    # Fetch historical data for 1 month
    stock = yf.Ticker(ticker)
    stock_history = stock.history(period="1mo")  
    stock_info = stock.info

    # Check if necessary data is available
    if 'currentPrice' not in stock_info:
        print(f"Warning: Missing 'currentPrice' for {ticker}.")
    
    return stock_history, stock_info

def fetch_stock_news(ticker):
    # Replace with your actual NewsAPI key
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
   
    # Check if the 'articles' key exists
    if 'articles' in news_data:
        return news_data['articles']
    else:
        print(f"No stock news articles avaliable for : {url}")
        return []  


# Fetch financial data from Alpha Vantage
def fetch_financial_data(ticker):
    api_key = 'API_KEY'
    fd = FundamentalData(api_key)
    try:
        company_overview, _ = fd.get_company_overview(ticker)
        return company_overview
    except Exception as e:
        print(f"Error fetching financial data: {e}")
        return None
