def samefile(f1, f2):
    '''
    A simple replacement of the os.path.samefile() function not existing 
    on the Windows platform. 
    MAC/Unix supported in standard way :).

    Author: Denis Barmenkov <denis.barmenkov@gmail.com>

    Source: code.activestate.com/recipes/576886/

    Copyright: this code is free, but if you want to use it, please
               keep this multiline comment along with function source. 
               Thank you.

    2009-08-19 20:13 
    '''
    try:
        return os.path.samefile(f1, f2)
    except AttributeError:
        f1 = os.path.abspath(f1).lower()
        f2 = os.path.abspath(f2).lower()
        return f1 == f2
