from core.provider.provider_manager import ProviderManager

class ProviderHealth:
    def __init__(self, manager=None):
        self.manager = manager or ProviderManager()

    def run(self):
        return self.manager.health()
