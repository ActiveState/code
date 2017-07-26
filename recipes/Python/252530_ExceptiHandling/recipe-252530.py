def throws(f, *a, **k):
    "Return True if f(*a,**k) raises an exception."
    try:
        f(*a,**k)
    except:
        return True
    else:
        return False


# Example - get numbers from a file, ignoring ill-formatted ones.
data = [float(line) for line in open(some_file) if not throws(float, line)]
