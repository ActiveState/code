'Nested contexts trees for implementing nested scopes (static or dynamic)'

from collections import MutableMapping
from itertools import chain, imap

class Context(MutableMapping):
    ''' Nested contexts -- a chain of mapping objects.

    c = Context()           Create root context
    d = c.new_child()       Create nested child context. Inherit enable_nonlocal
    e = c.new_child()       Child of c, independent from d
    e.root                  Root context -- like Python's globals()
    e.map                   Current context dictionary -- like Python's locals()
    e.parent                Enclosing context chain -- like Python's nonlocals

    d['x']                  Get first key in the chain of contexts
    d['x'] = 1              Set value in current context
    del['x']                Delete from current context
    list(d)                 All nested values
    k in d                  Check all nested values
    len(d)                  Number of nested values
    d.items()               All nested items

    Mutations (such as sets and deletes) are restricted to the current context
    when "enable_nonlocal" is set to False (the default).  So c[k]=v will always
    write to self.map, the current context.

    But with "enable_nonlocal" set to True, variable in the enclosing contexts
    can be mutated.  For example, to implement writeable scopes for nonlocals:

        nonlocals = c.parent.new_child(enable_nonlocal=True)
        nonlocals['y'] = 10     # overwrite existing entry in a nested scope

    To emulate Python's globals(), read and write from the the root context:

        globals = c.root        # look-up the outermost enclosing context
        globals['x'] = 10       # assign directly to that context

    To implement dynamic scoping (where functions can read their caller's
    namespace), pass child contexts as an argument in a function call:

        def f(ctx):
            ctx.update(x=3, y=5)
            g(ctx.new_child())

        def g(ctx):
            ctx['z'] = 8                    # write to local context
            print ctx['x'] * 10 + ctx['y']  # read from the caller's context

    '''
    def __init__(self, enable_nonlocal=False, parent=None):
        'Create a new root context'
        self.parent = parent
        self.enable_nonlocal = enable_nonlocal
        self.map = {}
        self.maps = [self.map]
        if parent is not None:
            self.maps += parent.maps

    def new_child(self, enable_nonlocal=None):
        'Make a child context, inheriting enable_nonlocal unless specified'
        enable_nonlocal = self.enable_nonlocal if enable_nonlocal is None else enable_nonlocal
        return self.__class__(enable_nonlocal=enable_nonlocal, parent=self)

    @property
    def root(self):
        'Return root context (highest level ancestor)'
        return self if self.parent is None else self.parent.root

    def __getitem__(self, key):
        for m in self.maps:
            if key in m:
                break
        return m[key]

    def __setitem__(self, key, value):
        if self.enable_nonlocal:
            for m in self.maps:
                if key in m:
                    m[key] = value
                    return
        self.map[key] = value

    def __delitem__(self, key):
        if self.enable_nonlocal:
            for m in self.maps:
                if key in m:
                    del m[key]
                    return
        del self.map[key]

    def __len__(self, len=len, sum=sum, imap=imap):
        return sum(imap(len, self.maps))

    def __iter__(self, chain_from_iterable=chain.from_iterable):
        return chain_from_iterable(self.maps)

    def __contains__(self, key, any=any):
        return any(key in m for m in self.maps)

    def __repr__(self, repr=repr):
        return ' -> '.join(imap(repr, self.maps))


if __name__ == '__main__':
    c = Context()
    c['a'] = 1
    c['b'] = 2
    d = c.new_child()
    d['c'] = 3
    print 'd:  ', d
    assert repr(d) == "{'c': 3} -> {'a': 1, 'b': 2}"

    e = d.new_child()
    e['d'] = 4
    e['b'] = 5
    print 'e:  ', e
    assert repr(e) == "{'b': 5, 'd': 4} -> {'c': 3} -> {'a': 1, 'b': 2}"

    f = d.new_child(enable_nonlocal=True)
    f['d'] = 4
    f['b'] = 5
    print 'f:  ', f
    assert repr(f) == "{'d': 4} -> {'c': 3} -> {'a': 1, 'b': 5}"

    print len(f)
    assert len(f) == 4
    assert len(list(f)) == 4
    assert all(k in f for k in f)
    assert f.root == c

    # dynanmic scoping example
    def f(ctx):
        print ctx['a'], 'f:  reading "a" from the global context'
        print 'f: setting "a" in the global context'
        ctx['a'] *= 999
        print 'f: reading "b" from globals and setting "c" in locals'
        ctx['c'] = ctx['b'] * 50
        print 'f: ', ctx
        g(ctx.new_child())
        print 'f: ', ctx


    def g(ctx):
        print 'g: setting "d" in the local context'
        ctx['d'] = 44
        print '''g: setting "c" in f's context'''
        ctx['c'] = -1
        print 'g: ', ctx
    global_context = Context(enable_nonlocal=True)
    global_context.update(a=10, b=20)
    f(global_context.new_child())
