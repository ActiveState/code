# -*- coding: utf-8 -*-
"""
Created  2015
"""

from decimal import Decimal


# TTT uppercase makes it a list var

# this just demonstrates the normalize-function
# and will print some numbers in a loop
# the Spyder IDE will run it no problem.

def eng(num):
    """ some doc string right here  """
    return Decimal(num).normalize().to_eng_string()

if __name__ == '__main__':

    TTT = [-78951, -500, 1e-3, 0.005, 0.05, 0.12,
               10, 23.3456789, 50, 150, 250, 800, 1250,
               127e11, 51234562]

    for x in TTT:
        print "%s: %s " % (x, eng(x))

###   no lint errors in here
