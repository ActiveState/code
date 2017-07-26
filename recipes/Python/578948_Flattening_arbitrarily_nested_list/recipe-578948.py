# Program to flatten an arbitrarily nested list.

def nested_item(depth, value):
    if depth <= 1:
        return [value]
    else:
        return [nested_item(depth - 1, value)]

def nested_list(n):
    """Generate a nested list where the i'th item is at depth i."""
    lis = []
    for i in range(n):
        if i == 0:
            lis.append(i)
        else:
            lis.append(nested_item(i, i))
    return lis

def flatten(lis):
    """Given a list, possibly nested to any level, return it flattened."""
    new_lis = []
    for item in lis:
        if type(item) == type([]):
            new_lis.extend(flatten(item))
        else:
            new_lis.append(item)
    return new_lis

for n in range(7):
    print n,
    lis = nested_list(n)
    print "original:", lis
    new_lis = flatten(lis)
    print "flattened:", new_lis
    print

for i in range(6):
    lis = range(i)
    print "orig:", lis
    flat_lis = flatten(lis)
    print "flat:", flat_lis
