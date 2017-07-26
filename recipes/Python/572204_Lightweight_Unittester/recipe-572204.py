import sys
from types import GeneratorType
from time import clock as sysTime

def timedeco(fct):
    def wrapper(*a, **k):
        start=sysTime()
        retval=fct(*a, **k)
        elapsed=sysTime()-start
        return (retval, elapsed)
    return wrapper

@timedeco
def run_test_functions(source=None):
    # source can be module, class, None, or a dictionary
    if source is None:
        ns = globals()
    elif isinstance(source, dict):
        ns = dict(source)
    else:
        ns = vars(source)

    tests = [(name, func) for name, func in ns.items() if name.startswith('test_')]
    tests = sorted(tests, reverse=True)

    failures = 0
    while tests:
        name, func = tests.pop()
        try:
            rv, et = timedeco(func)()
        except Exception, E:
            failures += 1
            print 'Err %s : %r ' % (name, E)
        else:
            if isinstance(rv, GeneratorType):
                pairs = []
                for func, arg in rv:
                    gname = '%s(%r)' % (func.__name__, arg)
                    gfunc = lambda func=func, arg=arg: func(arg)
                    pairs.append((gname, gfunc))
                tests.extend(reversed(pairs))
            else:
                print 'Ok %s : %.2G s' % (name, et)
    return failures

if __name__=='__main__':
    def test_sum():
        assert sum(range(5)) == 10
    def test_badsum():
        assert sum(range(5)) == 12, 'Bad Sum'
    def test_excpt():
        raise IndexError(3)
    def test_generative():
        x=1
        while x<10000000:
            x*=10
            yield sum_range, x
    def sum_range(arg):
        s=sum(range(arg))
    def td_setup():
        global g
        g = 1
    def td_teardown():
        global g
        del g
    def test_setup_and_teardown():
        td_setup()
        assert g == 1
        td_teardown()
    def test_att():
        a=b

    print '\n %i Err, %.2G s' % run_test_functions()
