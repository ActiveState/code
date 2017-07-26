from decimal import *
import math

pi = Decimal("3.14159265358979323846264338327950288419716939937510")

def gen_den():
    d = 1
    f = 1
    while(1):
        yield f
        d = d + 1
        f = f * d
    return

def gen_num(x):
    n = x
    while(1):
        yield n
        n *= x
    return

def gen_sign():
    while(1):
        yield 1
        yield -1
        yield -1
        yield 1
    return

def sincos(x):
    x = divmod(x, 2 * pi)[1]
    den = gen_den()
    num = gen_num(x)
    sign = gen_sign()

    s = 0
    c = 1
    i = 1
    done_s = False; done_c = False

    while(not done_s and not done_c):
        new_s = s + sign.next() * num.next() / den.next()
        new_c = c + sign.next() * num.next() / den.next()
        if (new_c - c == 0): done_c = True
        if (new_s - s == 0): done_s = True
        c = new_c
        s = new_s
        i = i + 2
    return (s, c)

def dec_sin(x):
    (s, c) = sincos(x)
    return s

def dec_cos(x):
    (s, c) = sincos(x)
    return c

def dec_tan(x):
    (s, c) = sincos(x)
    return s/c

print dec_sin(Decimal(1234))
print math.sin(1234)
