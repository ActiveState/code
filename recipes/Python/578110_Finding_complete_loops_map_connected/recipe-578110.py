def copy(l):
    l2=[]
    for x in l:
        l2.append(x)
    return l2
def loops(d):
    l=[]
    for x in d:
        l.append(x)
    lreq=[]
    lreq2=[]
    ltemp=[]
    for x in l:
        ltemp=[]
        ltemp.append(x)
        lreq2.append(ltemp)
    t=1
    while (t<=(len(l)-1)):
        lreq3=[]
        for x in lreq2:
            ltemp=copy(l)
            for y in x:
                ltemp.remove(y)
            for y in ltemp:
                h=copy(x)
                if y in d[x[-1]]:
                    h.append(y)
                    lreq3.append(h)
        if t>=2:
            for x in lreq3:
                if x[0] in d[x[-1]]:
                    h=copy(x)
                    h.append(h[0])
                    lreq.append(h)
        lreq2=copy(lreq3)
        t+=1
    for x in lreq:
        for y in lreq[(lreq.index(x)+1):]:
            if set(x)==set(y):
                lreq.remove(y)
    return lreq
