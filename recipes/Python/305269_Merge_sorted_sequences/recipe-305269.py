def merge(s1, s2, *args, **kwds):
    "Merge two sorted sequences."
    s3 = list(s1) + list(s2)
    s3.sort(*args, **kwds)
    return s3

if __name__ == "__main__":
    assert merge(xrange(0,10,2), xrange(1,10,2)) == range(10)
