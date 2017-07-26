def require_methods(*method_args):
    """Class decorator to require methods on a subclass.
    
    Example usage
    ------------
    @require_methods('m1', 'm2')
    class C(object):
        'This class cannot be instantiated unless the subclass defines m1() and m2().'
        def __init__(self):
            pass
    """
    def fn(cls):
        orig_init = cls.__init__
        def init_wrapper(self, *args, **kwargs):
            for method in method_args:
                if (not (method in dir(self))) or \
                   (not callable(getattr(self, method))):
                    raise Exception("Required method %s not implemented" % method)
            orig_init(self, *args, **kwargs)
        cls.__init__ = init_wrapper
        return cls
    return fn
