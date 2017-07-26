def pascal(n):
    """Prints n first lines of Pascal`s triangle

    author: DR#m <dnpsite.narod.ru>
    last rev 20.03.05"""
    l=[1]
    p=[]
    for i in xrange(n):
        l2=[1]
        for j in xrange(len(l)-1):
            l2.append(l[j]+l[j+1])
        l2.append(1)
        print l
        l=l2
if __name__=="__main__":
    pascal(20)
