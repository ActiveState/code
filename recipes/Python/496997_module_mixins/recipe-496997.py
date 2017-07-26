def mixin(mod):
    return type("mixin(%s)" % (mod.__name__,), (object,), mod.__dict__)
