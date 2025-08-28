import os
import sys
import types


def _ensure_module(name: str):
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)
    return sys.modules[name]


def pytest_sessionstart(session):
    # Ensure project root is on sys.path for absolute imports like `core.*`
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(tests_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Provide lightweight stubs to avoid ImportError during imports
    _ensure_module('streamlit')

    # dotenv.load_dotenv can be a no-op
    dotenv = _ensure_module('dotenv')
    def load_dotenv(*args, **kwargs):
        return None
    dotenv.load_dotenv = load_dotenv

    # google.generativeai stub
    genai = _ensure_module('google.generativeai')
    class _DummyResult:
        def __init__(self, text):
            self.text = text
    class _DummyModel:
        def __init__(self, *_args, **_kwargs):
            pass
        def generate_content(self, prompt):
            return _DummyResult("## Recommendation\nHold")
    def configure(**_kwargs):
        return None
    genai.GenerativeModel = _DummyModel
    genai.configure = configure

    # yfinance stub
    yfinance = _ensure_module('yfinance')
    class _DummyTicker:
        def __init__(self, *_args, **_kwargs):
            self.info = {}
        def history(self, period="1mo"):
            import pandas as pd
            return pd.DataFrame({"Close": [1, 2, 3]})
    yfinance.Ticker = _DummyTicker

    # alpha_vantage.fundamentaldata stub
    alpha_vantage = _ensure_module('alpha_vantage')
    fd_pkg = types.ModuleType('alpha_vantage.fundamentaldata')
    class _DummyFD:
        def __init__(self, *_args, **_kwargs):
            pass
        def get_company_overview(self, *_args, **_kwargs):
            return ({"Name": "Dummy"}, None)
    fd_pkg.FundamentalData = _DummyFD
    sys.modules['alpha_vantage.fundamentaldata'] = fd_pkg

    # transformers.pipeline stub
    transformers = _ensure_module('transformers')
    def pipeline(_task, **_kwargs):
        def _analyze(text):
            return [{"label": "neutral", "score": 0.5}]
        return lambda x: _analyze(x)
    transformers.pipeline = pipeline


