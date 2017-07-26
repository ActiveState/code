def blocks(size, box=(1,1)):
    """
    Iterate over a 2D range in 2D increments.
    Returns a 4 element tuple of top left and bottom right coordinates.
    """
    box = list(box)
    pos = [0,0]
    yield tuple(pos + box)
    while True:
        if pos[0] >= size[0]-box[0]:
            pos[0] = 0
            pos[1] += box[1]
            if pos[1] >= size[1]:
                raise StopIteration
        else:
            pos[0] += box[0]
        topleft = pos
        bottomright = [min(x[1]+x[0],x[2]) for x in zip(pos,box,size)]
        yield tuple(topleft + bottomright)

if __name__ == "__main__":
    for c in blocks((100,100),(99,10)):
        print c
    for c in blocks((10,10)):
        print c
