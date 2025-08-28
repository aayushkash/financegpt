import types

import services.data_fetcher as df


def test_fetch_stock_data_returns_tuple(monkeypatch):
    class DummyTicker:
        def __init__(self, *_a, **_k):
            self.info = {"currentPrice": 123}
        def history(self, period="1mo"):
            import pandas as pd
            return pd.DataFrame({"Close": [1, 2, 3]})

    monkeypatch.setattr(df.yf, 'Ticker', DummyTicker)
    hist, info = df.fetch_stock_data('INFY')
    assert 'currentPrice' in info
    assert hasattr(hist, 'tail')


def test_fetch_stock_news_handles_missing_articles(monkeypatch):
    class DummyResponse:
        def json(self):
            return {}
    monkeypatch.setattr(df.requests, 'get', lambda url: DummyResponse())
    news = df.fetch_stock_news('INFY')
    assert news == []


def test_fetch_financial_data_handles_exception(monkeypatch):
    class BoomFD:
        def __init__(self, *_a, **_k):
            pass
        def get_company_overview(self, *_a, **_k):
            raise RuntimeError('boom')
    fd_mod = types.SimpleNamespace(FundamentalData=BoomFD)
    monkeypatch.setattr(df, 'FundamentalData', fd_mod.FundamentalData)
    assert df.fetch_financial_data('INFY') is None


