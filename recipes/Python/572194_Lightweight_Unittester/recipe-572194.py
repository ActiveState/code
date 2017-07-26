def run_test_functions(source=None):
    from sys import stderr
    from types import GeneratorType

    # source can be module, class, None, or a dictionary    
    if source is None:
        ns = globals()
    elif isinstance(source, dict):
        ns = dict(source)
    else:
        ns = vars(source)

    tests = [(name, func) for name, func in ns.items() if name.startswith('test_')]
    tests = sorted(tests, reverse=True)

    successes = failures = 0
    while tests:
        name, func = tests.pop()
        try:
            rv = func()
        except Exception, E:
            failures += 1
            print name, '...', repr(E)
        else:
            if isinstance(rv, GeneratorType):
                pairs = []
                for func, arg in rv:
                    gname = 'gen:%s(%r)' % (name, arg)
                    gfunc = lambda func=func, arg=arg: func(arg)
                    pairs.append((gname, gfunc))
                tests.extend(reversed(pairs))
            else:
                successes += 1
                print name, '... Success'

    result = (successes+failures, failures)
    print 'Ran %d tests with %d failures' % result
    return result


#################################
## Example of the tester in action

def test_sum():
    assert sum(range(5)) == 10

def test_badsum():
    assert sum(range(5)) == 12

def test_excpt():
    raise IndexError(3)

def test_generative():
    for x in (42,17,49):
        yield check, x

def check(arg):
    assert arg % 7 == 0

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

print run_test_functions()
