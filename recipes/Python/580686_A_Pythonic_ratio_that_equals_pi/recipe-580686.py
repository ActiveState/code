from __future__ import print_function
import math

ratio = math.pi.as_integer_ratio()

# It can be verified with:

print(ratio[0] / ratio[1]) # for Python 3.x

# or

print(1.0 * ratio[0] / ratio[1]) # for Python 2.7x

# It gives:
# 3.141592653589793
# which is the value of pi to some decimal places.
