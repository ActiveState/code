import sys

def variant(expr):
    expr = int(expr)
    f = sys._getframe(1)
    name = "variant$%d"%f.f_lasti
    caller = f.f_locals
    try:
        result = (0<=expr<caller[name])
    except KeyError:
        result = True
    caller[name] = expr
    return result

#
#  sample
#

def test():
    assert variant(1) # Not an error: only executed once per function call
    assert variant(1) # Not an error: this is another statement
    for x in range(100):
        assert variant(100-x)  #Not an error: (100-x) decrease between loops
        #assert variant(1) #An error: 1 is constant

for i in range(10):
    test()
