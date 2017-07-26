def load_setting(key):
    # Just some dummy values for demo
    if key == 'key':
        return '123123'
    elif key == 'limit':
        return 123123
    elif key == 'dummylist':
        return [1, 2, 3, 4, 5]
    elif key == 'crap':
        return {'good': "boy"}

def superlazy(key, default):
    class T(type(default)):
        @staticmethod
        def __loader__():
            ret = load_setting(key)
            if ret:
                setattr(T, '__cache__', ret)
            delattr(T, '__loader__')
        
    def force(k, v):
        def _wrapper(*args, **kwargs):
            if hasattr(T, '__loader__'):
                T.__loader__()
            if hasattr(T, '__cache__'):
                c = T.__cache__
                func = getattr(c, k)
                return func(*args[1:], **kwargs)
            
            return v(*args, **kwargs)

        return _wrapper
    
    t = T(default)
    for k, v in type(default).__dict__.iteritems():
        if (k in ['__doc__']): continue
        setattr(T, k, force(k, v))
    return t

# Lazy string
a = superlazy("key", 'hahahaha')
print a, isinstance(a, str)

# Lazy int
b = superlazy("limit",9)
print 1 + b, isinstance(b, int)
print str(b)

# Lazy list
c = superlazy("dummylist", [1, 2, 3])
print c
print c[0]
print len(c)

# Lazy dict
d = superlazy("crap", {'a': 1, 'b': 2, 'c': 3})
print isinstance(d, dict)
print d
print d.get('a')

# Not existed lazy int, default value is used
e = superlazy("wer", 321)
print isinstance(e, int)
print e
