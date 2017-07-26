class NamedAndCachedAttributeType(type):
    '''
    In cases, where getting an attribute will
    expose to the client code the detail of
    the very attribute name, which could be changeable
    over time.
    This NamedAndCachedAttributeType is intended to
    hide this detail by mapping the real attribute name
    to another name that is maintained by the class itself.
    By doing so, the content provider(this class) and the client
    code(the caller) establish a deal that the changes of names
    are taken care of by the provider itself.
    Second, the value is set as a class variable once it is
    first retreived, as being cached.
    '''

    def _raise(cls, name):
        '''
        Override this provide a more specific exception
        '''
        raise AttributeError('No name "%s" is found' % name)

    def _cache(cls, name, value):
        '''
        The value will be cached by setting
        it as the class variable
        '''
        setattr(cls, name, value)

    def _get_value(cls, name):
        '''
        Override this method to do the
        actual work of getting the value
        '''
        raise RuntimeError('_get_value() must be overidden')

    def __getattr__(cls, name):
        if cls.__dict__.has_key(name):
            return cls.__dict__[name]
        value = cls._get_value(name)
        cls._cache(name, value)
        return value
