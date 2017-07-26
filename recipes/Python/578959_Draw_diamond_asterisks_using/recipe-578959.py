def triangles(n):
    if not n & 1:
        raise ValueError('n must be odd')
    print_diamond(0, n, n >> 1)

def print_diamond(start, stop, midpoint):
    if start < stop:
        if start <= midpoint:
            print('  ' * (midpoint - start) + '* ' * ((start << 1) + 1))
        else:
            print('  ' * (start - midpoint) + '* ' * ((stop - start << 1) - 1))
        print_diamond(start + 1, stop, midpoint)
