def conditional_retry(func=None, exceptions=Exception,
    action=None, callback_args=(), timeout=2):
    '''
    This decorator is able to be called with arguments.
    :keyword exceptions: exceptions in a tuple that will be
                         tested in the try/except
    :keyword action: a callable to be called at the end of every
                     time of re-attempt
    :keyword callback_args: arguments to be passed into the callable
    :keyword timeout: times of attempt, defaults to 2
    '''

    def decorated(func):
        def wrapper(*args, **kwargs):
            result = None
            i = 1
            while i <= timeout:
                try:
                    result = func(*args, **kwargs)
                    break
                except exceptions:
                    if i == timeout:
                        raise
                    if callable(action):
                        action(*callback_args)
                i += 1
            return result
        return wrapper

    if func is None: # in this case, the decorator is called with arguments
        def decorator(func):
            return decorated(func)
        return decorator
    # or the decorator is called without arguments
    return decorated(func)
