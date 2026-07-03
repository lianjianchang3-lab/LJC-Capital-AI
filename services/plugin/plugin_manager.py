class PluginManager:
    def __init__(self, logger=None):
        self.logger = logger
        self._plugins = {}

    def register(self, plugin):
        self._plugins[plugin.name] = plugin
        if self.logger:
            self.logger.info(f"Plugin registered: {plugin.name}")

    def get(self, name):
        return self._plugins.get(name)

    def list_plugins(self):
        return list(self._plugins.keys())

    def quality_report(self):
        return {name: plugin.quality() for name, plugin in self._plugins.items()}
