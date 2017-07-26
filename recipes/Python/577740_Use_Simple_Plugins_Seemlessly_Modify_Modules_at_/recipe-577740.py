"""modulehacker module"""

import sys
import importlib

_hackers = []
def register(obj):
    _hackers.append(obj)

class Hacker:
    def hack(self, module):
        return module

class Loader:
    def __init__(self):
        self.module = None
    
    def find_module(self, name, path):
        sys.meta_path.remove(self)
        self.module = importlib.import_module(name)
        sys.meta_path.insert(0, self)
        return self
    
    def load_module(self, name):
        if not self.module:
            raise ImportError("Unable to load module.")
        module = self.module
        for hacker in _hackers:
            module = hacker.hack(module)
        sys.modules[name] = module
        return module

sys.meta_path.insert(0, Loader())
