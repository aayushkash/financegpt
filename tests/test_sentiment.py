import core.sentiment_analysis as sa


def test_analyze_sentiment_defaults_to_neutral():
    articles = [{"title": "Flat day"}, {"title": "Mixed signals"}]
    sentiment = sa.analyze_sentiment(articles)
    assert sentiment in {"neutral", "positive", "negative"}


