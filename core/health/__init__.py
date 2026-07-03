from core.gateway import DataGateway

class HealthCheck:
    def run(self):
        return DataGateway().health()
