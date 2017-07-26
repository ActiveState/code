def is_a_number(x):
    """This function determines if its argument, x, is in the
    format of a number. It can be number can be in integer, floating
    point, scientific, or engineering format. The function returns True if the
    argument is formattted like a number, and False otherwise."""
    
    import re
    num_re = re.compile(r'^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$')
    mo = num_re.match(str(x))
    if mo:
        return True
    else:
        return False
