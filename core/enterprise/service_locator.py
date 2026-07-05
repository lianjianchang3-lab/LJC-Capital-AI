class ServiceLocator:
    """轻量级服务定位器。"""

    def __init__(self):
        self._services = {}

    def set(self, name, service):
        self._services[name] = service
        return service

    def get(self, name, factory=None):
        if name in self._services:
            return self._services[name]
        if factory is None:
            return None
        service = factory()
        self._services[name] = service
        return service

    def names(self):
        return sorted(self._services.keys())
