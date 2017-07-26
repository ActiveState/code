# Show relative speeds of local, nonlocal, global, and built-in access.

trials = [1] * 500

def read_local(trials=trials):
    v_local = 1
    for t in trials:
        v_local;    v_local;    v_local;    v_local;    v_local
        v_local;    v_local;    v_local;    v_local;    v_local
        v_local;    v_local;    v_local;    v_local;    v_local
        v_local;    v_local;    v_local;    v_local;    v_local
        v_local;    v_local;    v_local;    v_local;    v_local

def make_nonlocal_reader():
    v_nonlocal = 1
    def inner(trials=trials):
        for t in trials:
            v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal
            v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal
            v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal
            v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal
            v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal; v_nonlocal
    inner.__name__ = 'read_nonlocal'
    return inner

read_nonlocal = make_nonlocal_reader()

v_global = 1
def read_global(trials=trials):
    for t in trials:
        v_global; v_global; v_global; v_global; v_global
        v_global; v_global; v_global; v_global; v_global
        v_global; v_global; v_global; v_global; v_global
        v_global; v_global; v_global; v_global; v_global
        v_global; v_global; v_global; v_global; v_global

def read_builtin(trials=trials):
    for t in trials:
        oct; oct; oct; oct; oct
        oct; oct; oct; oct; oct
        oct; oct; oct; oct; oct
        oct; oct; oct; oct; oct
        oct; oct; oct; oct; oct

class A(object):
    def m(self):
        pass

def read_classvar(trials=trials, A=A):
    A.x = 1
    for t in trials:
        A.x;    A.x;    A.x;    A.x;    A.x
        A.x;    A.x;    A.x;    A.x;    A.x
        A.x;    A.x;    A.x;    A.x;    A.x
        A.x;    A.x;    A.x;    A.x;    A.x
        A.x;    A.x;    A.x;    A.x;    A.x

def read_instancevar(trials=trials, a=A()):
    a.x = 1
    for t in trials:
        a.x;    a.x;    a.x;    a.x;    a.x
        a.x;    a.x;    a.x;    a.x;    a.x
        a.x;    a.x;    a.x;    a.x;    a.x
        a.x;    a.x;    a.x;    a.x;    a.x
        a.x;    a.x;    a.x;    a.x;    a.x

def read_unboundmethod(trials=trials, A=A):
    # real unbound methods are only in Py2.x
    for t in trials:
        A.m;    A.m;    A.m;    A.m;    A.m
        A.m;    A.m;    A.m;    A.m;    A.m
        A.m;    A.m;    A.m;    A.m;    A.m
        A.m;    A.m;    A.m;    A.m;    A.m
        A.m;    A.m;    A.m;    A.m;    A.m

def read_boundmethod(trials=trials, a=A()):
    for t in trials:
        a.m;    a.m;    a.m;    a.m;    a.m
        a.m;    a.m;    a.m;    a.m;    a.m
        a.m;    a.m;    a.m;    a.m;    a.m
        a.m;    a.m;    a.m;    a.m;    a.m
        a.m;    a.m;    a.m;    a.m;    a.m

def write_local(trials=trials):
    v_local = 1
    for t in trials:
        v_local = 1; v_local = 1; v_local = 1; v_local = 1; v_local = 1
        v_local = 1; v_local = 1; v_local = 1; v_local = 1; v_local = 1
        v_local = 1; v_local = 1; v_local = 1; v_local = 1; v_local = 1
        v_local = 1; v_local = 1; v_local = 1; v_local = 1; v_local = 1
        v_local = 1; v_local = 1; v_local = 1; v_local = 1; v_local = 1

def make_nonlocal_writer():
    v_nonlocal = 1
    def inner(trials=trials):
        nonlocal v_nonlocal            # this is invalid syntax in Py2.x
        for t in trials:
            v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1
            v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1
            v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1
            v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1
            v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1; v_nonlocal = 1
    inner.__name__ = 'write_nonlocal'
    return inner

write_nonlocal = make_nonlocal_writer()

def write_global(trials=trials):
    global v_global
    for t in trials:
        v_global = 1; v_global = 1; v_global = 1; v_global = 1; v_global = 1
        v_global = 1; v_global = 1; v_global = 1; v_global = 1; v_global = 1
        v_global = 1; v_global = 1; v_global = 1; v_global = 1; v_global = 1
        v_global = 1; v_global = 1; v_global = 1; v_global = 1; v_global = 1
        v_global = 1; v_global = 1; v_global = 1; v_global = 1; v_global = 1

def write_classvar(trials=trials, A=A):
    for t in trials:
        A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1
        A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1
        A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1
        A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1
        A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1;    A.x = 1

def write_instancevar(trials=trials, a=A()):
    for t in trials:
        a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1
        a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1
        a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1
        a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1
        a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1;    a.x = 1

def loop_overhead(trials=trials):
    for t in trials:
        pass


if __name__=='__main__':
    from timeit import Timer

    for f in [read_local, read_nonlocal, read_global, read_builtin,
              read_classvar, read_instancevar, read_unboundmethod, read_boundmethod,
              write_local, write_nonlocal, write_global,
              write_classvar, write_instancevar,
              loop_overhead]:
        print('{:5.3f}\t{}'.format(min(Timer(f).repeat(7, 1000)), f.__name__))
