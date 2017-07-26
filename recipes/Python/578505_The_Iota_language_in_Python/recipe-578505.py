# Iota
#
# http://semarch.linguistics.fas.nyu.edu/barker/Iota/
#
# S = λx.λy.λz.xz(yz)
# K = λx.λy.x
# i = λc.cSK
#
# i, *ii, *i*ii, **ii*ii
# 0  100  10100  1100100  Iota is the encoding.
#
##  (let iota ()
##    (if (eq? #\* (read-char)) ((iota)(iota))
##        (lambda (c) ((c (lambda (x) (lambda (y) (lambda (z) ((x z)(y z))))))
##                     (lambda (x) (lambda (y) x))))))
##


S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x
i = lambda c: c(S)(K)
I = i(i)

def _decode(path):
  bit, path = path[0], path[1:]
  if bit == '0':
    return i, path
  A, path = _decode(path)
  B, path = _decode(path)
  return A(B), path


decode = lambda path: _decode(path)[0]


# K = *i*i*ii = 1010100
#
print K is i(i(i(i))) is decode('1010100')

# S = *i*i*i*ii = 101010100
#
print S is i(i(i(i(i)))) is decode('101010100')


# All of these return i itself.
print i is i
print i is i(i)(i)

print i is i(   i     )  ( i(i)(i) )
print i is i( i(i)(i) )  (   i     )
print i is i( i(i)(i) )  ( i(i)(i) )


# Identity function
#
I is decode('100') # I.e. i(i)
