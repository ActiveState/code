def is_a_number(x):
    """This function determines if its argument, x, is in the format of a
    number. It can be number can be in integer, floating point, scientific, or
    engineering format. The function returns '1' if the argument is formattted
    like a number, and '0' otherwise."""
    import re 
    num_re = re.compile(r'^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$')
    return str(re.match(num_re, x))) != 'None'
