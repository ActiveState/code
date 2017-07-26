def sublist(lst, n):
    sub=[] ; result=[]
    for i in lst:
        sub+=[i]
        if len(sub)==n: result+=[sub] ; sub=[]
    if sub: result+=[sub]
    return result
