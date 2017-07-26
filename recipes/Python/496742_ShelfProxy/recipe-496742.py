import shelve


class InvalidationError(Exception):
    pass

class ShelfProxy(Proxy):
    __slots__ = ["_key", "_shelf", "_invalidated"]
    
    def __init__(self, obj, shelf, key):
        Proxy.__init__(self, obj)
        object.__setattr__(self, "_shelf", shelf)
        object.__setattr__(self, "_key", key)
        object.__setattr__(self, "_invalidated", False)
    
    def __del__(self):
        try:
            sync_proxy(self)
        except InvalidationError:
            pass

class ShelfWrapper(object):
    def __init__(self, shelf):
        self.__shelf = shelf
        self.__cache = {}
    
    def __del__(self):
        self.close()
        
    def __getattr__(self, name):
        return getattr(self.__shelf, name)
    
    def __contains__(self, key):
        return key in self.__shelf
    
    def __len__(self, key):
        return len(self.__shelf)
    
    def __delitem__(self, key):
        if key in self.__cache:
            object.__setattr__(self.__cache[key], "_invalidated", True)
            del self.__cache[key]
        del self.__shelf[key]
    
    def __getitem__(self, key):
        try:
            obj = self.__cache[key]
        except KeyError:
            self.__cache[key] = obj = ShelfProxy(self.__shelf[key], self.__shelf, key)
        return obj
    
    def __setitem__(self, key, value):
        if key in self.__cache:
            object.__setattr__(self.__cache[key], "_invalidated", True)
            self.__cache[key] = ShelfProxy(value, self.__shelf, key)
        self.__shelf[key] = value
    
    def sync(self):
        for obj in self.__cache.itervalues():
            try:
                sync_proxy(obj)
            except InvalidationError:
                pass
    
    def close(self):
        self.sync()
        self.__cache.clear()
        self.__shelf.close()


def sync_proxy(proxy):
    if object.__getattribute__(proxy, "_invalidated"):
        raise InvalidationError("the proxy has been invalidated (the key was reassigned)")
    shelf = object.__getattribute__(proxy, "_shelf")
    key = object.__getattribute__(proxy, "_key")
    obj = object.__getattribute__(proxy, "_obj")
    shelf[key] = obj
    shelf.sync()

def open(*args):
    return ShelfWrapper( shelve.open(*args) )


------ example ------
>>> db = open("blah.db")
>>> db["mylist"]=[1,2,3]
>>> db["mylist"].append(4)
>>> db["mylist"]
[1, 2, 3, 4]
>>> p = db["mylist"]
>>> type(p)
<class '__main__.ShelfProxy(list)'>
>>> p.append(5)
>>> p2 = db["mylist"]
>>> p2
[1, 2, 3, 4, 5]
>>> p2 is p
True

----- invalidation -----
When we reassign a key that have been proxies earlier, the proxy 
instance becomes invalidated, so it will not override the new value.

>>> db["mylist"] = 19
>>> sync_proxy(p)
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
  File "Proxy.py", line 152, in sync_proxy
    raise InvalidationError("the proxy has been invalidated (the key was reassigned)")
__main__.InvalidationError: the proxy has been invalidated (the key was reassigned)
>>>
>>> db["mylist"] += 1
>>> db["mylist"]
20
