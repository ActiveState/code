"""docfunc module"""

from deferred_binder import DeferredBinder

class DocFunc(DeferredBinder):

    TRIGGER = None

    def __init__(self, f):
        super().__init__(f.__name__, f)
        self.f = self.target

    @staticmethod
    def transform(name, context, target, obj=None):
        """The DeferredBinder transform for this subclass.

          name - the attribute name to which the function will be bound.
          context - the class/namespace to which the function will be bound.
          target - the function that will be bound.
          obj - ignored.

        The DeferredBinder descriptor class will replace itself with the
        result of this method, when the name to which the descriptor is requested
        for the first time.  This can be on the class or an instances of the
        class.

        This way the class to which the method is bound is available so that the
        inherited docstring can be identified and set.

        """

        namespace, cls = context
        doc = target.__doc__
        if doc == DocFunc.TRIGGER:
            doc = DocFunc.get_doc(cls, name, DocFunc.TRIGGER)
        target.__doc__ = doc
        return target

    @staticmethod
    def get_doc(cls, fname, default=TRIGGER, member=True):
        """Returns the function docstring the method should inherit.

          cls - the class from which to start looking for the method.
          fname - the method name on that class
          default - the docstring to return if none is found.
          member - is the target function already bound to cls?

        """

        print(cls)
        bases = cls.__mro__[:]
        if member:
            bases = bases[1:]
        for base in bases:
            print(base)
            func = getattr(base, fname, None)
            if not func:
                continue
            doc = getattr(func, '__doc__', default)
            if doc == default:
                continue
            return doc
        return default

    @staticmethod
    def inherits_docstring(f, context=None, fname=None, default=TRIGGER):
        """A decorator that returns a new DocFunc object.
          
          f - the function to decorate.
          context - the class/namespace where the function is bound, if known.
          fname - the function name in that context, if known.
          default - the docstring to return if none is found.

        """

        if context is not None:
            cls, namespace = context
            fname = fname or f.__name__
            f.__doc__ = DocFunc.get_doc(cls, fname, default, False)
            return f
        return DocFunc(f, default)
