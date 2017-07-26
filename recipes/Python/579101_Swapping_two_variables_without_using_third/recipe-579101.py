First method of swapping, using arithmetic expressions, reqires the variable being swapped to be of numeric type, specifically integer:
a = 1
b = 2
# Prints original values of a and b, i.e. 1 and 2:
print a, b
# Now the swap, using some additions and subtractions.
a = a + b
b = a - b
a = a - b# Prints swapped values of a and b, i.e. 2 and 1:
print a, b

Second method is simpler, and can work for more types of Python objects, using parallel assignment:

a, b = b, a
