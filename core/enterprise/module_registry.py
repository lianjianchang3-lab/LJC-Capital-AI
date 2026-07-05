class ModuleRegistry:
    """统一模块注册中心。"""

    def __init__(self):
        self._modules = {}

    def register(self, name, module):
        self._modules[name] = module
        return module

    def get(self, name, default=None):
        return self._modules.get(name, default)

    def has(self, name):
        return name in self._modules

    def names(self):
        return sorted(self._modules.keys())

    def run(self, name, method="run", *args, **kwargs):
        module = self.get(name)
        if module is None:
            raise KeyError(f"module not registered: {name}")
        fn = getattr(module, method, None)
        if fn is None:
            raise AttributeError(f"module {name} has no method {method}")
        return fn(*args, **kwargs)
