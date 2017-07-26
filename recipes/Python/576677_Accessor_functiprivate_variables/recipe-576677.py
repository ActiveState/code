# Accessor function for private variables in Py3.x

def get_private_attr(inst, attr):
    'Access private variables without resorting to name mangling'
    s = ('class %(cls)s: \n' +
         ' def _show(self):  return self.%(attr)s \n' +
         'private = %(cls)s._show(inst) \n')
    s %= dict(cls=inst.__class__.__name__, attr=attr)
    d = dict(inst=inst)
    exec(s, d, d)
    return d['private']


if __name__ == '__main__':

    class MyClass:
        def __init__(self, x):
            self.__hidden = x

    m = MyClass(10)
    print(get_private_attr(m, '__hidden'))
