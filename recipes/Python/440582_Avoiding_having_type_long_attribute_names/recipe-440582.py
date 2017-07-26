class Sample(object):
    """Show how to add support for abbreviated long names to an object.


    >>> sample = Sample()
    >>> sample.__dict__
    {'x': 1, 'xylophone': 2, 'verylongname': 20}
    >>> sample.x
    1
    >>> sample.xylophone
    2
    >>> sample.xy
    2
    >>> sample.v
    20
    >>> sample.z
    Traceback (most recent call last):
    AttributeError
    """
    def __init__(self):
        self.x = 1
        self.xylophone = 2
        self.verylongname = 20
        
    def __getattr__(self,attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            choices = [a for a in self.__dict__ if a.startswith(attr)]
            if len(choices)==1:
                return self.__dict__[choices[0]]
            else:
                raise AttributeError

if __name__=="__main__":
    import doctest,recipe
    doctest.testmod(recipe)
