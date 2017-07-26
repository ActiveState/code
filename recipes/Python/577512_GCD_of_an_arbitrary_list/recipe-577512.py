#!/usr/bin/python

def gcd(*args):
    if len(args) == 1:
        return args[0]

    L = list(args)

    while len(L) > 1:
        a = L[len(L) - 2]
        b = L[len(L) - 1]
        L = L[:len(L) - 2]
        
        while a:
            a, b = b%a, a

        L.append(b)
        
    return abs(b)

#if __name__ == "__main__":

print gcd(68, 14, 9, 36, 126)
