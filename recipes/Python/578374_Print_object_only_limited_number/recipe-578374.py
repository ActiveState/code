# From psome.py

import inspect

"""
The psome function detects the position into the source files where the
function itself is called. It prints the object according a counter variable.
Therefore, whenever the psome function is called inside a loop the object will
be printed only a limited number of times. This can useful for debugging
code in particular when the data structure we want to scan is quite big and we
want to print only the first elements of it.
"""

__author__ = "Filippo Squillace"
__version__ = "0.1.0"


# The dictionary stores for each call of psome the position
# (<namefile>:<numline>) as key and the counter as value
d = {}

def psome(obj, count):
    """
    The obj will printed only a number of count times.
    """
    global d
    key = inspect.stack()[1][1]+':'+str(inspect.stack()[1][2])
    d[key] = d.get(key,count) -1

    if d[key]>=0:
        print(obj)







# From test.py

from psome import psome

def test_psome():
    ls = "This is a list of elements, but not all of them will be printed".split()
    for e in ls:
        # .... let's do many stuff

        # Prints only six elements
        psome(e, 6)


if __name__ == '__main__':
    test_psome()
