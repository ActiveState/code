from functools import wraps


class default_kwargs(object):
    """
    Metadecorator for ensuring specified keys are present in kwargs before calling function

    Will only use default value if the key is not already present in kwargs.
    """
    def __init__(self, **kwargs):
        self.defaults = kwargs
    def __call__(self, wrapped):
        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            new_kwargs = self.defaults.copy()
            new_kwargs.update(kwargs)
            return wrapped(*args, **new_kwargs)
        return wrapper


## Usage example:

@default_kwargs(echo=True)
def f(*args, **kwargs):
  if kwargs["echo"]:
    print args, kwargs
