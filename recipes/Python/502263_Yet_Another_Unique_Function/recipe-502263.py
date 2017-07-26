def unique(inlist, keepstr=True):
  typ = type(inlist)
  if not typ == list:
    inlist = list(inlist)
  i = 0
  while i < len(inlist):
    try:
      del inlist[inlist.index(inlist[i], i + 1)]
    except:
      i += 1
  if not typ in (str, unicode):
    inlist = typ(inlist)
  else:
    if keepstr:
      inlist = ''.join(inlist)
  return inlist

##
## testing...
##

assert unique( [[1], [2]] ) == [[1], [2]]
assert unique( ((1,),(2,)) ) == ((1,), (2,))
assert unique( ([1,],[2,]) ) == ([1,], [2,])
assert unique( ([1+2J],[2+1J],[1+2J]) ) == ([1+2j], [2+1j])
assert unique( ([1+2J],[1+2J]) ) == ([1+2j],)
assert unique( [0] * 1000 ) == [0]
assert unique( [1, 2, 3, 1, 2]) == [1, 2, 3]
assert unique( [3, 2, 3, 1, 2]) == [3, 2, 1]
s = "iterable dict based unique"
assert unique(s) == 'iterabl dcsunq'
assert unique(s, False) == ['i', 't', 'e', 'r', 'a', 'b', 'l', ' ', 'd', 'c', 's', 'u', 'n', 'q']
s = unicode(s)
assert unique(s, False) == [u'i', u't', u'e', u'r', u'a', u'b', u'l', u' ', u'd', u'c', u's', u'u', u'n', u'q']
assert unique(s) == u'iterabl dcsunq'

# all asserts should pass!
