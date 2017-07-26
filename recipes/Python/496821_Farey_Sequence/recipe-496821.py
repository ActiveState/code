def farey(n):
    def gcd(a,b):
        while b: a,b = b,a%b
        return a

    def simplify(a,b):
        g = gcd(a,b)
        return (a/g,b/g)

    fs = dict()
    for i in xrange(1,n+1):
        for i2 in xrange(1,i+1):
            if i2 < n and i != i2:
                r = simplify(i2,i)
                fs[float(i2)/i] = r

    return [fs[k] for k in sorted(fs.keys())]

# Usage:
# print farey(5)
# => [(1, 5), (1, 4), (1, 3), (2, 5), (1, 2), (3, 5), (2, 3), (3, 4), (4, 5)]
