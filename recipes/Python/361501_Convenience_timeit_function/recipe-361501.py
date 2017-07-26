import sys
import timeit

def timefunc(func, n=3, mod=''):
    """Run func in timeit.main, n times, import from mod,
    mod defaults to name of the func."""
    parpos=func.find('(')
    if parpos == -1:
        print "You need to specify arguments or at least parentheses after the name of the function"
        return -1
    funcname=func[0:parpos]
    if mod=='':
        mod=funcname
    timeit.main(['-s', 'from ' + mod + ' import ' + funcname, '-n', n, func])
