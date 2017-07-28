def area_by_shoelace(x, y):
    "Assumes x,y points go around the polygon in one direction"
    return abs( sum(i * j for i, j in zip(x, y[1:])) + x[-1] * y[0]
               -sum(i * j for i, j in zip(x[1:], y)) - x[0] * y[-1]) / 2 
