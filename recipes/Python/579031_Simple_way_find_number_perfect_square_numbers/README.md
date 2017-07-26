###Simple way to find number of perfect square numbers in a range.

Originally published: 2015-03-05 15:59:29
Last updated: 2015-03-05 15:59:30
Author: alexander baker

The strategy here is not to iterate through the set of possible integer values and check for is_perfect_square()\n      each time but to translate the upper and lower values to either complex or real space of square numbers.\n        \n        # O(n) complexity\n        len([x for x in range(0, 100) if x!= 0 and float(math.sqrt(x)).is_integer()])\n        \n        so if a and b positive then we count the number of integer values between upper and lower sqrt() values\n        if either a or b are negative then we need to use the complex number space for the sqrt() results. In this case\n        we are still counting integer values either along the imaginary or real axis, the result is then a simple sum\n        if both a and b are negative we need to make sure that when walking down the same imaginary axis we dont count\n        the same inteters twice, in this case we can take the min(a,b) to get max distinct set of integer values.