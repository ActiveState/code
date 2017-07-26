# Halley's method for solving f(x)=0
# http://en.wikipedia.org/wiki/Halley%27s_method
# FB - 201011265
global h
h = 0.00000001
eps = 0.000001

# f(x) to solve
def f(x):
    return x * x - 2.0

def fp(x):
    global h
    return (f(x + h) - f(x)) / h

def fpp(x):
    global h
    return (fp(x + h) - fp(x)) / h

# main
x = 2.0 # initial value

while True:
    fx = f(x)
    fpx = fp(x)
    xnew = x - (2.0 * fx * fpx) / (2.0 * fpx * fpx - fx * fpp(x))
    print xnew
    if abs(xnew - x) <= eps: break
    x = xnew
