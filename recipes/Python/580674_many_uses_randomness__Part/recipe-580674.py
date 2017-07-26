from __future__ import print_function

# fn_random.py
# A program showing various uses of the "random" function 
# from the "random" module of Python's standard library.
# Author: Vasudev Ram - https://vasudevram.github.io
# Copyright 2016 Vasudev Ram

from random import random
from random import getstate, setstate

print("Ex. 1. Plain calls to random():")
print("Gives 10 random float values in the interval [0, 1).")
for i in range(10):
    print(random())

print()

print("Ex. 2. Calls to random() scaled by 10:")
print("Gives 10 random float values in the interval [0, 10).")
for i in range(10):
    print(10.0 * random())

print()

print("Ex. 3. Calls to random() scaled by 10 and offset by -5:")
print("Gives 10 random float values in the interval [-5, 5).")
for i in range(10):
    print(10.0 * random() - 5.0)

print()

print("Ex. 4. Calls to random() scaled by 20 and offset by 40:")
print("Gives 10 random float values in the interval [40, 60).")
for i in range(10):
    print(20.0 * random() + 40.0)
