"""Sentiment analysis utilities."""
from transformers import pipeline
from services.data_fetcher import fetch_stock_news

# Initialize sentiment analysis pipeline (use HuggingFace model or any other sentiment analysis model)
def analyze_sentiment(news_articles):
    sentiment_analyzer = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")
    sentiments = []
    
    # Analyzing the sentiment of the article title
    for article in news_articles:
        sentiment = sentiment_analyzer(article['title'])[0]  
        sentiments.append(sentiment['label'])
    
    # Return the most common sentiment from the articles
    if sentiments:
        return max(set(sentiments), key=sentiments.count)
    return "neutral"  # Default to neutral if no sentiment can be determined


# Example of usage (for testing purposes)
if __name__ == "__main__":
    # Fetching the stock news data
    news_data_list = fetch_stock_news('INFY')
    sentiment = analyze_sentiment(news_data_list)
    print(f"Overall Sentiment: {sentiment}")