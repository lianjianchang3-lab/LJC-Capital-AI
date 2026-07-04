from abc import ABC, abstractmethod

class BaseProvider(ABC):
    name = "base"
    mode = "unknown"

    @abstractmethod
    def get_quotes(self): pass

    @abstractmethod
    def get_capital(self): pass

    @abstractmethod
    def get_portfolio(self): pass

    def health(self):
        return {"provider": self.name, "mode": self.mode, "ready": True, "latency_ms": None, "message": "OK"}
