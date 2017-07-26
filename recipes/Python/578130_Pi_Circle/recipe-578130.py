def pi(places=10):
    "Computes pi to given number of decimal places"
    # 3 + 3*(1/24) + 3*(1/24)*(9/80) + 3*(1/24)*(9/80)*(25/168)
    # The numerators 1, 9, 25, ... are given by  (2x + 1) ^ 2
    # The denominators 24, 80, 168 are given by (16x^2 -24x + 8)
    extra = 8
    one = 10 ** (places+extra)
    t, c, n, na, d, da = 3*one, 3*one, 1, 0, 0, 24
    while t > 1:
        n, na, d, da  = n+na, na+8, d+da, da+32
        t = t * n // d
        c += t
    return c // (10 ** extra)

def picirc(radius, aspect_ratio=5):
    "Display the digit of pi in a circle of given radius"
    display_width = int(radius * aspect_ratio + 10)
    pi_str = repr(pi(int(2 * radius ** 2 * aspect_ratio)))
    pos = 0
    for i in range(2 * radius):
        cols = int(0.5 + aspect_ratio * (radius**2 - (radius-(i+0.5))**2) ** 0.5)
        print(pi_str[pos:pos+cols].center(display_width))
        pos += cols

if __name__ == '__main__':
    picirc(16)
