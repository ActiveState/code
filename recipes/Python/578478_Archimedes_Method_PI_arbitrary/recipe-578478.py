# Archimedes Method for PI
# FB - 200912082
# Revised by Bjorn.madsen AT operationsresearchgroup.com for Python3.3
# BHM - 20130302

import decimal

def ArchPi(precision=99):
    # x: circumference of the circumscribed (outside) regular polygon
    # y: circumference of the inscribed (inside) regular polygon

    decimal.getcontext().prec = precision+1
    D=decimal.Decimal
    
    # max error allowed
    eps = D(1)/D(10**precision)
    
    # initialize w/ square
    x = D(4)
    y = D(2)*D(2).sqrt()

    ctr = D(0)
    while x-y > eps:
        xnew = 2*x*y/(x+y)
        y = D(xnew*y).sqrt()
        x = xnew
        ctr += 1
        

    return str((x+y)/D(2))

if __name__ == '__main__':
    print(ArchPi(99))
