from datetime import date, time, timedelta

def make_immutable(value):
    if isinstance(value, (int, long, date, time, timedelta, basestring, buffer)): return value
    if isinstance(value, (list, tuple)): return tuple([make_immutable(x) for x in value])
    if isinstance(value, dict):
        class DictTuple(tuple): pass
        return DictTuple([(make_immutable(k), make_immutable(v)) for k, v in value.iteritems()])
    raise NotImplemented()

class CacheCaller(object):
    def __init__(self, acallable):
        self.acallable = acallable
        self.cache = {}
    def __call__(self, *args, **kwargs):
        key = (make_immutable(args), make_immutable(kwargs))
        if key in self.cache:
            result = self.cache[key]
        else:
            result = self.acallable(*args, **kwargs)
            self.cache[key] = result
        return result

def example():
    
    # slow operation
    def get_value(param1, param2, param3, param4):
        from time import sleep
        sleep(1)
        return '%s %s %s %s' % (param1, param2, param3, param4)

    # not a good idea to do it repeatly
    print get_value(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print get_value(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print get_value(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print get_value(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print get_value(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})

    # make it faster with cache
    caller = CacheCaller(get_value)
    print caller(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print caller(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print caller(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print caller(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
    print caller(1, 'string', [1,2,3], {'one': 1, 'two': 2, 'three': 3})
