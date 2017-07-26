import sys
import types
import warnings

class EncapsulationWarning(RuntimeWarning): pass

class ModuleWrapper(types.ModuleType):
    def __init__(self, context):
        self.context = context
        super(ModuleWrapper, self).__init__(
                context.__name__,
                context.__doc__)

    def __getattribute__(self, key):
        context = object.__getattribute__(self, 'context')
        if key not in context.__all__:
            warnings.warn('%s not in %s.__all__' % (key, context.__name__),
                          EncapsulationWarning,
                          2)
        return context.__getattribute__(key)

import example
sys.modules['example'] = ModuleWrapper(example)
