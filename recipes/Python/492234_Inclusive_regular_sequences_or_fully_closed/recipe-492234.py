def seq(*args, **kwargs):
    """
        seq(n1, n2, base=, by=, length=, ztol=)    

    Minimum number is 1 and maximum number of args is 2.
    Any misspecification will result in an empty list. 
    Current version has no extensive error checking!
    """
    
    # Undefined key?
    unknownKeys = [key for key in kwargs.keys() if key not in ["base","length","by","ztol"]]
    if unknownKeys:
        return []
    
    # Tolerance for floating point computations.
    if kwargs.has_key("ztol"):
        ztol = kwargs["ztol"]
    else:
        ztol = 1.0e-14
    
    # Normally, base is 0 since Python indexing is 0-based.
    if kwargs.has_key("base"):
        base = kwargs["base"]
    else:
        base = 0
    
    nargs, nkwargs = len(args), len(kwargs)
    if nargs == 1:  
        n1 = float(args[0])
        if kwargs.has_key("length"):
            L = kwargs["length"]
            if kwargs.has_key("by"):
                d = kwargs["by"]
            else:
                d = 1.0
            return [n1 + i * d for i in range(L)]
        
        elif kwargs.has_key("by"):
            d = kwargs["by"]
            if abs(d) < ztol: # too small by.
                return []
            if (n1 > base and d > 0) or (n1 < base and d < 0):
                return [] # wrong sign for value of by
            L = int((float(base-n1) / float(d)) + 1 + ztol)
            return [n1 + i * d for i in range(L) ]

        else:
            L = int((abs(n1 - base)) + 1 + ztol)
            if n1 > base:
                return [base + i  for i in range(L) ]
            else:
                return [base - i  for i in range(L) ]
            
    elif nargs == 2:  
        n1 = args[0]
        n2   = args[1]

        nparms = 0
        if kwargs.has_key("by") and kwargs.has_key("length"):
            return []  # Too many parameters
        if kwargs.has_key("by"):
            d = kwargs["by"]
            if n2 > n1 and d < 0:
                return []  # Wrong sign for by value.
            L = int((float(n2 - n1) / d) + 1 + ztol)
        elif kwargs.has_key("length"):
            L = kwargs["length"]
            if L <= 0:
                return []
            d = float((n2 - n1)) /  float(L)
        else:
            if n2 < n1:
                d = -1
            elif n2 > n1:
                d = 1
            else:
                d = 0
            L = int(abs(n2 - n1) + 1 + ztol)                
        return [n1 + i*d for i in range(L) ]
    return []
        

if __name__ == "__main__":
    print "seq(2)",                      seq(2)
    print "seq(2, base=1)",              seq(2, base=1)
    print "seq(2.6)",                    seq(2.6)
    print "seq(2.6, length=4)",          seq(2.6, length=4)
    print "seq(2.6, length=4, by=0.1)",  seq(2.6, length=4, by=0.1)
    print "seq(2.6, length=4, by=-0.1)", seq(2.6, length=4, by=-0.1)
    print "seq(2.6, length=4, by= 0)",   seq(2.6, length=4, by=0)

    print "seq(2,   by=0.1)",            seq(2.6,  by= 0.1)
    print "seq(2.6, by=-0.1)",           seq(2.6, by=-0.1)
    print "seq(2.6, by=-0.1, base = 1)", seq(2.6, by=-0.1, base=1)
    
    print "seq(-2)",                     seq(-2)
    print "seq(-2, base=1)",             seq(-2, base=1)
    print "seq(-2.6)",                   seq(-2.6)
    print "seq(-2.6, by=0.1, base = 1)", seq(-2.6, by=0.1, base=1)
    print "seq(-2.6, by=-0.1)",          seq(-2.6, by=-0.1)
    print "seq(2.6,  by= 0)",            seq(2.6, by=0)
    
    print "seq(-2.6, 5)",                seq(-2.6, 5)
    print "seq(5, -2.6)",                seq(5, -2.6)
    print "seq(-2.6, 5.1, by=0.1)",      seq(-2.6, 5.1, by=0.1)
    print "seq(-2.6, 5, by=-0.1)",       seq(-2.6, 5, by=-0.1)
    print "seq(-2.6, 5, by=-0.1, length=10)",seq(-2.6, 5, by=-0.1, length=10)
