from UserDict import DictMixin
import   re

class InternalLogicError(RuntimeError):
   def   __init__(self, msg):
   self.value  =  msg

   def   __str__(self):
      return   repr(self.value)


class Node:
   def   __init__(self, key, value):
   self.prior  =  None
   self.next   =  None
   self.key =  key
   self.value  =  value

   def   elide(self):
   "Remove a node from the doubly linked list.  (It remains in the dict.)"
   if self.prior == None:
      if self.next   == None: return
      if self.next.prior ==   self:
      self.next.prior   =  None
      self.next      =  None
      return
      raise InternalLogicError("self.next.prior != self and != None")
   if self.next   == None:
      if self.prior.next == self:
      self.prior.next   =  None
      self.prior     =  None
      return
      raise InternalLogicError("self.prior.next != self and != None")
   self.prior.next   =  self.next
   self.next.prior   =  self.prior
   self.next   =  None
   self.prior  =  None

   def   addHead(self, first):
   "  add this node to the head of the list (i.e., before first, and with prior == None   "
   if first is None:
      #  empty list
      self.next   =  None
      self.prior  =  None
      return
   self.next   =  first
   first.prior =  self
   self.prior  =  None

   def   delTail(self):
   "  delete this node from the tail of the list   "
   if self.next   is not   None:
      raise InternalLogicError   \
         ("self.next != None, but it must be at the tail of the list")
   self.prior.next   =  None

   def   __str__(self):
   return   "Node(%s, %s)" % (str(self.key), str(self.value))
   
   def   portOut(self):
   "  Node position on list will be forgotten   "
   return   "<Node(%s, %s)>" % (repr(self.key), repr(self.value))


class LRUCache(DictMixin):
   """
   A class for maintaining a cache of limited size, with the most recently used versions
   being kept.  This class is designed to operate in nearly constant time as the size
   of the cache varies.
   Warning:  This has not been tested much beyond the test sample included at the end.
   """
   def   __init__(self, maxSize = 255, chunk = 1, nodeDict = None):
   if chunk >= maxSize:
      raise ValueError ("invalid parameters.  chunk must be smaller than maxSize")
   self._maxSize  =  maxSize  #  how large is the cache allowed to grow
   self._chunk =  chunk    #  how many should be freed from cache in one cycle
   self._basket   =  {}
   self._first =  None  #  head of the access sequence list
   self._last  =  None  #  tail of the access sequence list

   if nodeDict is not None:
      for   key   in nodeDict.keys():
      node  =  Node(key, nodeDict[key])
      if self._first is None:
         self._first =  node
         self._last  =  node
      else:
         node.addHead(self._first)
         self._first =  node
      self._basket[key] =  node

   def   __getitem__(self, key):
   if key in self._basket:
      node  =  self._basket[key]
      if (len(node) < 2):
      raise InternalLogicError("Invalid basket item length")
      try:
      ndx   =  self._list.index(node)
      del   self._list[ndx]
      except   KeyError, e:
      raise InternalLogicError(e)
      self._list[:0]= [node]
      return   node[1]
   return   None

   def   __setitem__(self, key, value):
   if key is None:   return
   if self._first is None:
      self._first =  Node(key, value)
      self._last  =  self._first
      self._basket[key] =  self._first
      return

   if len(self._basket) > self._maxSize:
      while (len(self._basket) >= self._maxSize - self._chunk):
      l  =  self._last
      self._last  =  self._last.prior
      l.delTail()
      del   self._basket[l.key]

   if key in self._basket:
      node  =  self._basket[key]
      if node is self._first: return   #  already at head
      node.elide()            #  remove node from within the list
      node.addHead(self._first)     #  and move it to the head
      self._first =  node
      return
   else: #  new item
      node  =  Node (key, value)
      node.addHead(self._first)
      self._first =  node
      self._basket[key] = node
      return

   def   __delitem__(self, key):
   if key not in  self._basket:  return
   node  =  self._basket[key]
   node.elide()
   del   self._basket[key]


   def   __contains__(self, key):
   return   key in self._basket

   def   __iter__(self):
   return   self._basket.iterkeys()

   def   __repr__(self):
   ret   =  "LRUCache(%s, %s" % (self._maxSize, self._chunk)
   if len(self._basket) < 1:
      return   ret + ")"
   else:
      r  =  []
      for   key   in self._basket.keys():
      node  =  self._basket[key]
      r.append("%s : %s" % (repr(node.key), repr(node.value)))
      return   ret + ", {" + ", ".join(r) + "})"

   def   iteritems(self):
   "  Warning:  This is not counted as an access by the cache  "
   for   key   in self._basket.keys():
      if key is None:   continue
      node  =  self._basket[key]
      yield node.key, node.value

   def   keys(self):
   return   self._basket.keys()

   def   portOut(self):
   ret   =  "<LRUCache(%s, %s) :: " % (self._maxSize, self._chunk)
   f  =  True
   r  =  []
   for   key   in self._basket.keys():
      node  =  self._basket[key]
      r.append ("%s : %s" % (repr(node.key), repr(node.value)))
   return   (ret + (", ".join(r)) + " >")


   @classmethod
   def   portIn(cls, defStr):
   """   defStr should have been produced by portOut.
      Warning:  You *must* be able to trust the source of this string!!
      Warning:  On porting in the order of most recent access will randomized.
   """
   if not ((defStr[0] == "<") and (defStr[-1] == ">")):
      raise ValueError ("invalid parameter.  Malformed class description.")
   ds =  defStr[1:-2].strip()
   i  =  ds.find("::")
   if (i < 0):
      itm   =  eval(ds)
      return   itm
   else:
      ds0   =  ds[0:i]
      itm   =  eval(ds0)
      ds =  ds[i + 2:].strip()
      vals  =  eval("{" + ds + "}")
      for   key   in vals.keys():
      node  =  Node(key, vals[key])
      node.addHead(itm._first)
      itm._basket[key]  =  node
      return   itm

if __name__ == "__main__":
   lru   =  LRUCache(20, 7)
   for   i  in range(90):
   lru[str(i)] = i * i + 0.1

   print "lru = ", lru
   del   lru[78]
   lru[10]  =  100
   print "lru mod = ", lru
   d  =  lru.portOut()
   print "portOut = ", d
   lru2  =  LRUCache.portIn(d)
   print "lru2 = ", lru2
   print repr(lru2)
   lru3  =  eval(repr(lru2) )
   print "lru3 = ", lru3
   
