from services.config.config_service import ConfigService
from services.logger.log_service import LogService
from services.version.version_service import VersionService
from services.plugin.plugin_manager import PluginManager


class LJCAppCore:
    def __init__(self):
        self.config = ConfigService()
        self.logger = LogService()
        self.version = VersionService()
        self.plugins = PluginManager(self.logger)

    def boot(self):
        self.logger.info("LJC V8 Core boot")
        return {
            "app": self.config.get("app", {}),
            "version": self.version.current(),
            "plugins": self.plugins.list_plugins(),
        }
