"""decorations module"""

import types
import modulehacker

_modules = {}
_decorators = []
def register(decorator, modules=None):
    """Register a decorator for a list of module names."""
    if not decorator:
        return
    if not modules and decorator in _decorators:
        return
    if not modules:
        _decorators.append(decorator)
        return

    if isinstance(modules, str):
        modules = (modules,)
    for module in modules:
        if module not in _modules:
            _modules[module] = []
        _modules[module].append(decorator)

class Hacker(modulehacker.Hacker):
    def hack(self, module):
        for decorator in _modules.get(module.__name__, ()):
            self.decorate(module, decorator)
        for decorator in _decorators:
            self.decorate(module, decorator)
        return module
    def decorate(self, module, decorator):
        for attr in module.__dict__:
            obj = getattr(module, attr)
            if isinstance(obj, types.FunctionType):
                setattr(module, attr, decorator(obj))

modulehacker.register(Hacker())
