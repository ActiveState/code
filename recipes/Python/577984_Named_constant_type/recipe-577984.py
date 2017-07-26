class constant(int):
    """A constant type which overrides base int to provide a useful name on str().
    Example:

    >>> STATUS_RUNNING = constant(0, 'running')
    >>> STATUS_RUNNING  
    0
    >>> str(STATUS_RUNNING)
    'running'
    >>>
    """

    def __new__(cls, value, name, doc=None):
        inst = super(constant, cls).__new__(cls, value)
        inst._name = name
        if doc is not None:
            inst.__doc__ = doc
        return inst

    def __str__(self):
        return self._name

    def __eq__(self, other):
        if isinstance(other, int):
            return int(self) == other
        if isinstance(other, str):
            return self._name == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
