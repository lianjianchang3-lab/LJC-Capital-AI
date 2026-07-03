from abc import ABC, abstractmethod


class DataPlugin(ABC):
    name = "base"

    def connect(self):
        return True

    @abstractmethod
    def fetch_quotes(self, symbols):
        raise NotImplementedError

    def fetch_capital(self, symbols):
        return []

    def quality(self):
        return {
            "source": self.name,
            "score": 50,
            "status": "unknown",
        }

    def disconnect(self):
        return True
