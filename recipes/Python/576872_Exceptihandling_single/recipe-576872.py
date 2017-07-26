def safecall(f, default=None, exception=Exception):
    '''Returns modified f. When the modified f is called and throws an
    exception, the default value is returned'''
    def _safecall(*args,**argv):
        try:
            return f(*args,**argv)
        except exception:
            return default
    return _safecall

[safecall(int)(i) for i in '1 2 x'.split()]   # returns [1, 2, None]

[safecall(int, -1, ValueError)(i) for i in '1 2 x'.split()]    # returns [1, 2, -1]
