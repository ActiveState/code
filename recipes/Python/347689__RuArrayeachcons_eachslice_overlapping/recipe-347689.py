def each_cons_iter(listin,n): 
"""(overlapp'g)moving window,return n items at a time from listin thru iterator"""
    i=0
    while (i<len(listin)-n+1 ):
        yield listin[i:i+n]
        i+=1
        
def each_slice_iter(listin,n):    
"""non-overlapp'g slices n elements at a time from listin,returned thru iterator"""
    i=0;        len_listin=len(listin)
    while (i<len_listin ):
        yield listin[i:min(len_listin,i+n)]
        i+=n
        
def each_cons_lol(listin,n):    
"""moving window, return (list of lists) of n items at a time"""
    return [listin[i:i+n] for i in range(len(listin)-n+1)]

def each_slice_lol(listin,n):        
"""non-overlapp'g slices, return (list of lists) """
    len_listin=len(listin)
    return [listin[i:min(len_listin, i+n)] for i in range(0,len_listin,n)]
