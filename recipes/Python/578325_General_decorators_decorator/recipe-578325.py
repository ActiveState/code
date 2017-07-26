def decorator(decorating_func):
  """ takes a decorator and fixes it a bit. """
  def new_decorator(func):
    decorated_func = decorating_func(func)
    decorated_func.__name__ = func.__name__
    decorated_func.__doc__ = func.__doc__
    decorated_func.__dict__.update(func.__dict__)
    return decorated_func
  new_decorator.__name__ = decorating_func.__name__
  new_decorator.__doc__ = decorating_func.__doc__
  new_decorator.__dict__.update(decorating_func.__dict__)
  return new_decorator
