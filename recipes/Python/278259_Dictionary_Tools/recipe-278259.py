#========================================================================

def sumDict(d): 
    return reduce(lambda x,y:x+y, d.values())

#========================================================================

def avgDict(d): 
    return reduce(lambda x,y:x+y, d.values()) / (len(d)*1.0)

#========================================================================

def mkDict(keyList, valueList, cond=None):
    '''
    Make a new dict out of two lists. The first list provides keys,
    the 2nd provides values. The cond is a function taking 2 arguments:
    key and value. Example: lambda k,v:v%2==0
    A valid item means its cond(key, value) is true. Only valid items
    are included in the returned dict. 

    >>> a
    [0, 1, 2, 3, 4]
    
    >>> b= [chr(x) for x in range(65,70)]
    >>> b
    ['A', 'B', 'C', 'D', 'E']
    
    >>> mkDict(b,a)
    {'A': 0, 'C': 2, 'B': 1, 'E': 4, 'D': 3}
    
    >>> mkDict(b,a,lambda x,y:y%2==0)
    {'A': 0, 'C': 2, 'E': 4}

    Note:
    mkDict(a,b) (without the conditional check) is equavilant to
    dict(zip(a,b)), which is much faster. If you know there's no
    conditional check, better use dict(zip(a,b)) instead.
    '''

    if cond==None:
        return dict(zip(keyList, valueList))        
    else:
        return dict( [(k,v) for k,v in zip(keyList, valueList) if cond(k,v)] )

#========================================================================

def trimDict(aDict, cond=(lambda k,v:1)):
    ''' Return a new dict in which its items whose cond(k,v) == true
    are removed (discarded) from aDict.
    The cond is a function taking 2 arguments: key and value
    
    >>> g
    {'A': 0, 'C': 2, 'B': 1, 'E': 4, 'D': 3}
    >>> trimDict(g, lambda x,y:y%2!=0)
    {'A': 0, 'C': 2, 'E': 4}
    
    '''    
    tmp={}
    [tmp.setdefault(k,v) for k,v in aDict.items() if not cond(k,v)]
    return tmp.copy()

#========================================================================

def reDict(aDict, func, cond=(lambda k,v:1), delUnchanged=0):
    '''
    Given aDict, return a new dict with valid items (= items whose
    cond(key, value) is true) been modified by the function func.
    if delUnchanged, then those invalid items are excluded from
    the returned dict.
    
    >>> d
    {'B': 1, 'D': 3}
    >>> reDict(d, lambda x:x**2)
    {'B': 1, 'D': 9}
    >>> g
    {'A': 0, 'C': 2, 'B': 1, 'E': 4, 'D': 3}
    >>> reDict(g, lambda x:-x, lambda k,v: v%2==0)
    {'A': 0, 'C': -2, 'B': 1, 'E': -4, 'D': 3}
    >>> reDict(g, lambda x:-x, lambda k,v: v%2==0, delUnchanged=1)
    {'A': 0, 'C': -2, 'E': -4}    

    '''
    tmp={}
    if delUnchanged:
       [tmp.setdefault(k,func(v)) for k,v in aDict.items() if cond(k,v)]
    else:
       [tmp.setdefault(k,(cond(k,v) and func(v) or v)) for k,v in aDict.items()]
    return tmp.copy()

#========================================================================

def normDict(d, normalizeTo=1):
  ''' Normalize the values of d by setting the largest value in d.values
      to normalizeTo. The return dict will have it's values spreading
      between 0~normalizeTo'''
  ks = d.keys()
  vs = d.values()
  vMax = max(vs)
  vs= [ x/(vMax*1.0)*normalizeTo for x in vs]
  return dict(zip(ks, vs))

#========================================================================

def normDictSumTo(d, sumTo=1):
  ''' Normalize the values of d to sumTo. The returned dict will
      have value sum = sumTo
  '''
  ks = d.keys()
  vs = d.values()  
  sum = reduce(lambda x,y:x+y, vs)
  vs= [ x/(sum*1.0)*sumTo for x in vs]
  return dict(zip(ks, vs))

#========================================================================

def accumDict(d, normalizeTo=None):
    ''' if d.values=[1,2,3,4,5]: 
        accumDict(d).values ==>   [1, 3, 6, 10, 15]
        if d.values=[0.25, 0.25, 0.25, 0.25]
        accumDict(d).values ==>   [0.25, 0.50, 0.75, 1.00]

        Required: odict()
        Ordered Dictionary Class
        Dave Benjamin 
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/161403
    '''
    ks = d.keys()
    vs = d.values()
    if normalizeTo: vs = normListSumTo(vs, sumTo=normalizeTo)

    r = range(1, len(vs))
    newList=[vs[0]]
    for i in r:
        newList.append( newList[-1]+ vs[i] )
    
    odic = odict()
    for i in range(len(newList)):
        odic[ks[i]] =newList[i]
    return odic 

#========================================================================

def fallInDict(val, aDict, baseValue=0):
    '''
    oo:
    {
     'a':3,
     'b':5,
     'c':2
    }
    accumDict(oo):
    {
     'a':3,
     'b':8,
     'c':10
    }
    fallInDict(0, oo)=0
    fallInDict(1, oo)=0
    fallInDict(2, oo)=0
    fallInDict(3, oo)=0
    fallInDict(4, oo)=1
    fallInDict(5, oo)=1
    fallInDict(6, oo)=1
    fallInDict(7, oo)=1
    fallInDict(8, oo)=1
    fallInDict(9, oo)=2
    fallInDict(10, oo)=2

    When val out of range:
    
    fallInDict(-1, oo)= -1
    fallInDict(11, oo)= -2
    fallInDict(12, oo)= -2
    '''

    if val<baseValue: return -1
    acd = accumDict(aDict)
    if val>acd.values()[-1]: return -2

    ra = range(len(acd))

    for i in ra:
        vInDict = acd.values()[i]
        if val <= vInDict: break

    return aDict.keys()[i]  

#========================================================================

def randomPickDict(d):
    ''' given a diictionary d, with all values are numbers,
        randomly pick an item and return it's key according
        to the percentage of its values'''
    ks = d.keys()
    vs = accumList(d.values(),1)
    return ks[ findIndex( vs, random.random()) ]

#========================================================================

def sumInDict(L):
  ''' Given a list L:
     [ {'S': [s11,s12,s13], 'V':[v11,v12,v13], ...},
       {'S': [s21,s22,s23], 'V':[v21,v22,v23], ...},
       {'S': [s31,s32,s33], 'V':[v31,v32,v33], ...},
       ... ]
       
     Return a dict:
     {'S': [s1,s2,s3], 'V':[v1,v2,v3], ...}

     where s1 = s11 + s21 + s31 + ...
           s2 = s12 + s22 + s32 + ...
  '''  
  keys = L[0].keys()
  new={}
  for k in keys:
      new[k] = []   # Init 'S':[]
      for x in L:   # x = {'S': [s11,s12,s13], 'V':[v11,v12,v13], ...}
          y = x[k]  # y = [s11,s12,s13]
          new[k].append(y) 

      ''' new[k] = [ [s11,s12,s13],[s21,s22,s23],[s31,s32,s33], ...]
          Then use sumInList=> {'S': [s1,s2,s3],'V': [v1,v2,v3],... }'''
      new[k] = sumInList(new[k])
  return new   

#========================================================================

def avgInDict(L):
  ''' Given a list L:
     [ {'S': [s11,s12,s13], 'V':[v11,v12,v13], ...},
       {'S': [s21,s22,s23], 'V':[v21,v22,v23], ...},
       {'S': [s31,s32,s33], 'V':[v31,v32,v33], ...},
       ... ]
       
     Return a dict:
     {'S': [s1,s2,s3], 'V':[v1,v2,v3], ...}

     where s1 = avg of (s11 + s21 + s31 + ...)
           s2 = avg of (s12 + s22 + s32 + ...)
  '''  
  ''' First turn L into:
      {'S': [ [s11,s12,s13],[s21,s22,s23],[s31,s32,s33], ...],
       'V': [ [v11,v12,v13],[v21,v22,v23],[v31,v32,v33], ...],
       ... }  '''

  keys = L[0].keys()
  new={}
  for k in keys:
      new[k] = []   # Init 'S':[]
      for x in L:   # x = {'S': [s11,s12,s13], 'V':[v11,v12,v13], ...}
          y = x[k]  # y = [s11,s12,s13]
          new[k].append(y) 

      ''' new[k] = [ [s11,s12,s13],[s21,s22,s23],[s31,s32,s33], ...]
          Then use avgInList=> {'S': [s1,s2,s3],'V': [v1,v2,v3],... }'''
      new[k] = avgInList(new[k])
  return new    

#========================================================================

def sumInDict2(D):
  ''' Given a dict:
        {'A':{'S': [s11,s12,s13], 'V':[v11,v12,v13], ...},
         'B':{'S': [s21,s22,s23], 'V':[v21,v22,v23], ...},
         'C':{'S': [s31,s32,s33], 'V':[v31,v32,v33], ...}, ...
        } 
     Return a dict:
     {'S': [s1,s2,s3], 'V':[v1,v2,v3], ...}

     where s1 = s11 + s21 + s31 + ...
           s2 = s12 + s22 + s32 + ...
  '''
  return sumInDict(D.values())

#========================================================================

def avgInDict2(D):
  ''' Given a dict:
        {'A':{'S': [s11,s12,s13], 'V':[v11,v12,v13], ...},
         'B':{'S': [s21,s22,s23], 'V':[v21,v22,v23], ...},
         'C':{'S': [s31,s32,s33], 'V':[v31,v32,v33], ...}, ...
        } 
     Return a dict:
     {'S': [s1,s2,s3], 'V':[v1,v2,v3], ...}

     where s1 = avg of (s11 + s21 + s31 + ...)
           s2 = avg of (s12 + s22 + s32 + ...)
  '''
  return avgInDict(D.values())

#========================================================================
