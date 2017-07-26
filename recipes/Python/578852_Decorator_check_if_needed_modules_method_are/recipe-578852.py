import sys

def require_module(names,exception=None):
    """
    Check if needed modules imported before run method

    Example::

        @require_module(['time'],exception=Exception)
        def get_time():
            return time.time()
    """
    def check_module(f):
        def new_f(*args, **kwds):
            for module_name in names:
                if module_name not in sys.modules.keys():
                    if exception:
                        raise exception('Module %s is required for %s' % (module_name,f.func_name))
                    else:
                        return None
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_module


@require_module(['time'],exception=Exception)
def aaa():
    print time.time()


aaa()
