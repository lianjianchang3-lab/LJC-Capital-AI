import pandas as pd
from core.provider.base_provider import BaseProvider

class RealtimeProvider(BaseProvider):
    name = "Realtime Provider"
    mode = "REALTIME"

    def __init__(self, enabled=False):
        self.enabled = enabled

    def get_quotes(self): return pd.DataFrame()
    def get_capital(self): return pd.DataFrame()
    def get_portfolio(self): return pd.DataFrame()

    def health(self):
        return {"provider": self.name, "mode": self.mode, "ready": False, "latency_ms": None, "message": "Not configured. Waiting for commercial data source."}
