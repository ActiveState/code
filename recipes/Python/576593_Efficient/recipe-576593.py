def build(n,m=0):
    " returns a generator that will successively return permutions on n integers m at a timt (nPr)" 
    if (m==0):
        m = n
    source = """def perm(n,m):"""
    source  = source + """\n r=set(range(1,n+1))""" # 1 indent already!
    source  = source + """\n s0=r"""
    indent=1
    for z in range(0,m):  # main source build loop
        source= source + """\n""" + " ".ljust(indent)+ "for "  + "i" + str(z) + " in s" + str(z) + ":"
        indent = indent+1
        # build diff string
        diff="(["
        for k in range(0,z+1):
            diff=diff+ "i" + str(k)+","
        diff=diff[:-1]+ "])"
        #print "diff = " + diff
        source=source + """\n"""+" ".ljust(indent)+"s"+str(k+1)+"=r.difference"+diff
    
    diff = diff[2:-2]
    
    #source = source + """\n""" + " ".ljust(indent) + "print " + diff
    source = source + """\n""" + " ".ljust(indent) + "yield " + diff+","
    #print source
    obj=compile(source,'<in line source>',"exec")
    exec(obj)
    return perm(n,m)
