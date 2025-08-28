import types

import core.agent_handler as ah


def test_generate_recommendation_happy_path(monkeypatch):
    # Stub data fetchers
    def fake_fetch_stock_data(_ticker):
        import pandas as pd
        hist = pd.DataFrame({"Close": [1, 2, 3]})
        info = {"currentPrice": 123, "trailingPE": 10, "marketCap": 1_000_000}
        return hist, info

    monkeypatch.setattr(ah, 'fetch_stock_data', fake_fetch_stock_data)
    monkeypatch.setattr(ah, 'fetch_financial_data', lambda t: {"Name": "Dummy"})
    monkeypatch.setattr(ah, 'fetch_stock_news', lambda t: [{"title": "Up"}])

    rec = ah.generate_recommendation('INFY')
    assert isinstance(rec, str)
    assert 'Recommendation' not in rec  # parse_recommendation removes header


def test_generate_recommendation_missing_price(monkeypatch):
    def fake_fetch_stock_data(_ticker):
        import pandas as pd
        hist = pd.DataFrame({"Close": [1, 2, 3]})
        info = {}
        return hist, info

    monkeypatch.setattr(ah, 'fetch_stock_data', fake_fetch_stock_data)
    res = ah.generate_recommendation('INFY')
    assert isinstance(res, tuple)
    assert 'Missing' in res[0]


