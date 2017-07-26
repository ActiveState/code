import tempfile, sqlobject
class SubscriptableGenerator(object):
    
    class Data(sqlobject.SQLObject):
        data = sqlobject.PickleCol()
        
    def __init__(self, sqlite=None):
        if not sqlite:
            sqlite = tempfile.mkstemp('.db', 'subGenCache-')[1]            
            
        self.sqlite = sqlite
        uri = "sqlite://%s" % sqlite                
        c = sqlobject.connectionForURI(uri)
        sqlobject.sqlhub.processConnection = c            
        SubscriptableGenerator.Data.createTable(ifNotExists=True)
        
        self._genCounter = 1
        
    def __iter__(self):
        return self
          
    def next(self):            
        try:
            ret = SubscriptableGenerator.Data.get(self._genCounter).data
        except:
            try:
                ret = self.gen()
                SubscriptableGenerator.Data(data=ret)
            except StopIteration:
                raise StopIteration
        self._genCounter += 1
        return ret
    
    def _getFromCache(self, i):
        try:
            ret = SubscriptableGenerator.Data.get(i+1).data
        except:
            ret = self.gen()
            SubscriptableGenerator.Data(id=i+1, data=ret)
            
        #self._genCounter += 1
        return ret
    
    def __getitem__(self, k):
        if isinstance(k, slice):
            [self._getFromCache(i) for i in xrange(0, k.start)]
            
            return [self._getFromCache(i) for i in xrange(k.start, k.stop, 1 if k.start < k.stop else -1)]
        else:
            return self._getFromCache(k)
    
    # irreversible without a flush due to the fact that
    # the generator isn't called unless the _cache[k] is undefined
    def __setitem__(self, k, v):
        val = SubscriptableGenerator.Data.get(k+1)
        val.data = v
        
    def gen(self):
        raise NotImplementedError
