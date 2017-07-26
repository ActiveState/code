def pi(err, abs=abs):
    'Approximation of pi +/- err using the Mandlebrot set'
    n = 0
    z = c = complex(-0.75, err)
    while abs(z) < 2.0:
            n += 1
            z = z * z + c
    return n * err

if __name__ == '__main__':
    for i in range(1, 8):
        err_bound = 10 ** (-i)
        print(pi(err_bound), 'within', err_bound)
