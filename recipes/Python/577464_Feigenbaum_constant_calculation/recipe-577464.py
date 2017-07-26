# Feigenbaum constant calculation
# FB - 201011151
# http://en.wikipedia.org/wiki/Feigenbaum_constant
# Source:
# http://keithbriggs.info/documents/how-to-calc.pdf
import math

def b(a, k):
    if k == 0:
        return 0
    else:
        return a - math.pow(b(a, k - 1), 2)

def b_prime(a, k):
    if k == 0:
        return 0
    else:
        return 1 - 2 * b_prime(a, k - 1) * b(a, k - 1)

# main
print 'Feigenbaum constant calculation:'
maxIt = 10
maxItJ = 10
ai_1 = 1
ai_2 = 0
di_1 = 3.2
print 'i', 'di'
for i in range(2, maxIt):
    ai = ai_1 + (ai_1 - ai_2) / di_1
    for j in range(maxItJ):
        ai = ai - b(ai, math.pow(2, i)) / b_prime(ai, math.pow(2, i))
    #
    di = (ai_1 - ai_2) / (ai - ai_1)
    print i, di
    # prepare for the next iteration
    di_1 = di
    ai_2 = ai_1
    ai_1 = ai
