## example
unique = lambda x: reduce(lambda y,z: (not (z in y) and y.append(z) ) or y, x, [])
unique([3, 4, 5, 6, 5, 3, 7])
