# Archimedes Method for PI
# FB - 200912082

# x: circumference of the circumscribed (outside) regular polygon
# y: circumference of the inscribed (inside) regular polygon

import math

# max error allowed
eps = 1e-10

# initialize w/ square
x = 4
y = 2*math.sqrt(2)

ctr = 0
while x-y > eps:
    xnew = 2*x*y/(x+y)
    y    = math.sqrt(xnew*y)
    x    = xnew
    ctr += 1

print("PI = " + str((x+y)/2))
print("# of iterations = " + str(ctr))
