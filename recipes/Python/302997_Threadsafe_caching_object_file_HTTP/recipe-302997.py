# -*- coding: iso-8859-1 -*-

from os import stat
from time import time, mktime
from rfc822 import parsedate
from calendar import timegm
import urllib2
import re
import weakref
import new

try:
    from threading import Lock
except ImportError:
    from dummy_threading import Lock

NOT_INITIALIZED = object()

class Entry(object):
    """ A cache entry, mostly an internal object. """
    def __init__(self, key):
        object.__init__(self)
        self._key=key
        self._value=NOT_INITIALIZED
        self._lock=Lock()

class Cache(object):
    """ An abstract, multi-threaded cache object. """
    
    def __init__(self, max_size=0):
        """ Builds a cache with a limit of max_size entries.
            If this limit is exceeded, the Least Recently Used entry is discarded.
            if max_size==0, the cache is unbounded (no LRU rule is applied).
        """
        object.__init__(self)
        self._maxsize=max_size
        self._dict={}
        self._lock=Lock()
        
        # Header of the access list
        if self._maxsize:
            self._head=Entry(None)
            self._head._previous=self._head
            self._head._next=self._head

    def __setitem__(self, name, value):
        """ Populates the cache with a given name and value. """
        key = self.key(name)
        
        entry = self._get_entry(key)
        
        entry._lock.acquire()
        try:
            self._pack(entry,value)
            self.commit()
        finally:
            entry._lock.release()

    def __getitem__(self, name):
        """ Gets a value from the cache, builds it if required.
        """
        return self._checkitem(name)[2]

    def __delitem__(self, name):
        self._lock.acquire()
        try:
            key = self.key(name)
            del self._dict[key]
        finally:
            self._lock.release()

    def _get_entry(self,key):
        self._lock.acquire()
        try:
            entry = self._dict.get(key)
            if not entry:
                entry = Entry(key)
                self._dict[key]=entry
                if self._maxsize:
                    entry._next = entry._previous = None
                    self._access(entry)
                    self._checklru()
            elif self._maxsize:
                self._access(entry)
            return entry
        finally:
            self._lock.release()

    def _checkitem(self, name):
        """ Gets a value from the cache, builds it if required.
            Returns a tuple is_new, key, value, entry.
            If is_new is True, the result had to be rebuilt.
        """
        key = self.key(name)
        
        entry = self._get_entry(key)

        entry._lock.acquire()
        try:
            value = self._unpack(entry)
            is_new = False
            if value is NOT_INITIALIZED:
                opened = self.check(key, name, entry)
                value = self.build(key, name, opened, entry)
                is_new = True
                self._pack(entry, value)
                self.commit()
            else:
                opened = self.check(key, name, entry)
                if opened is not None:
                    value = self.build(key, name, opened, entry)
                    is_new = True
                    self._pack(entry, value)
                    self.commit()
            return is_new, key, value, entry
        finally:
            entry._lock.release()

    def mru(self):
        """ Returns the Most Recently Used key """
        if self._maxsize:
            self._lock.acquire()
            try:
                return self._head._previous._key
            finally:
                self._lock.release()
        else:
            return None

    def lru(self):
        """ Returns the Least Recently Used key """
        if self._maxsize:
            self._lock.acquire()
            try:
                return self._head._next._key
            finally:
                self._lock.release()
        else:
            return None

    def key(self, name):
        """ Override this method to extract a key from the name passed to the [] operator """
        return name

    def commit(self):
        """ Override this method if you want to do something each time the underlying dictionary is modified (e.g. make it persistent). """
        pass

    def clear(self):
        """ Clears the cache """
        self._lock.acquire()
        try:
            self._dict.clear()
            if self._maxsize:
                self._head._next=self._head
                self._head._previous=self._head
        finally:
            self._lock.release()

    def check(self, key, name, entry):
        """ Override this method to check whether the entry with the given name is stale. Return None if it is fresh
            or an opened resource if it is stale. The object returned will be passed to the 'build' method as the 'opened' parameter.
            Use the 'entry' parameter to store meta-data if required. Don't worry about multiple threads accessing the same name,
            as this method is properly isolated.
        """
        return None

    def build(self, key, name, opened, entry):
        """ Build the cached value with the given name from the given opened resource. Use entry to obtain or store meta-data if needed.
             Don't worry about multiple threads accessing the same name, as this method is properly isolated.
        """
        raise NotImplementedError()
           
    def _access(self, entry):
        " Internal use only, must be invoked within a cache lock. Updates the access list. """
        if entry._next is not self._head:
            if entry._previous is not None:
                # remove the entry from the access list
                entry._previous._next=entry._next
                entry._next._previous=entry._previous
            # insert the entry at the end of the access list
            entry._previous=self._head._previous
            entry._previous._next=entry
            entry._next=self._head
            entry._next._previous=entry
            if self._head._next is self._head:
                self._head._next=entry

    def _checklru(self):
        " Internal use only, must be invoked within a cache lock. Removes the LRU entry if needed. """
        if len(self._dict)>self._maxsize:
            lru=self._head._next
            lru._previous._next=lru._next
            lru._next._previous=lru._previous
            del self._dict[lru._key]

    def _pack(self, entry, value):
        """ Store the value in the entry. """
        entry._value=value

    def _unpack(self, entry):
        """ Recover the value from the entry, returns NOT_INITIALIZED if it is not OK. """
        return entry._value

class WeakCache(Cache):
    """ This cache holds weak references to the values it stores. Whenever a value is not longer
        normally referenced, it is removed from the cache. Useful for sharing the result of long
        computations but letting them go as soon as they are not needed by anybody.
    """
        
    def _pack(self, entry, value):
        entry._value=weakref.ref(value, lambda ref: self.__delitem__(entry._key))
        
    def _unpack(self, entry):
        if entry._value is NOT_INITIALIZED:
            return NOT_INITIALIZED
            
        value = entry._value()
        if value is None:
            return NOT_INITIALIZED
        else:
            return value

class FileCache(Cache):
    """ A file cache. Returns the content of the files as a string, given their filename.
        Whenever the files are modified (according to their modification time) the cache is updated.
        Override the build method to obtain more interesting behaviour.
    """
    def __init__(self, max_size=0, mode='rb'):
        Cache.__init__(self, max_size)
        self.mode=mode
    
    def check(self, key, name, entry):
        timestamp = stat(key).st_mtime 

        if entry._value is NOT_INITIALIZED:
            entry._timestamp = timestamp
            return file(key, self.mode)
        else:
            if entry._timestamp != timestamp:
                entry._timestamp = timestamp
                return file(key, self.mode)
            else:
                return None

    def build(self, key, name, opened, entry):
        """ Return the content of the file as a string. Override this for better behaviour. """
        try:
            return opened.read()
        finally:
            opened.close()

def parseRFC822Time(t):
    return mktime(parsedate(t))

re_max_age=re.compile('max-age\s*=\s*(\d+)', re.I)

class HTTPEntity(object):
    def __init__(self, entity, metadata):
        self.entity=entity
        self.metadata=metadata
    
    def __repr__(self):
        return 'HTTPEntity(%s, %s)'%(repr(self.entity), self.metadata)
        
    def __str__(self):
        return self.entity

class HTTPCache(Cache):
    """ An HTTP cache. Returns the entity found at the given URL.
        Uses Expires, ETag and Last-Modified headers to minimize bandwidth usage.
        Partial Cache-Control support (only max-age is supported).
    """
    def check(self, key, name, entry):
        request = urllib2.Request(key)
        
        try:
            if time()<entry._expires:
                return None
        except AttributeError:
            pass            
        try:
            header, value = entry._validator
            request.headers[header]=value
        except AttributeError:
            pass
        opened = None
        try:
            opened = urllib2.urlopen(request)
            headers = opened.info()

            # expiration handling            
            expiration = False
            try:
                match = re_max_age.match(headers['cache-control'])
                if match:
                        entry._expires=time()+int(match.group(1))
                        expiration = True
            except (KeyError, ValueError):
                pass
            if not expiration:
                try:
                    date = parseRFC822Time(headers['date'])
                    expires = parseRFC822Time(headers['expires'])
                    entry._expires = time()+(expires-date)
                    expiration = True
                except KeyError:
                    pass
            
            # validator handling
            validation = False
            try:
                entry._validator='If-None-Match', headers['etag']
                validation = True
            except KeyError:
                pass
            if not validation:
                try:
                    entry._validator='If-Modified-Since', headers['last-modified']
                except KeyError:
                    pass

            return opened
        except urllib2.HTTPError, error:
            if opened: opened.close()
            if error.code==304:
                return None
            else:
                raise error

    def build(self, key, name, opened, entry):
        try:
            return HTTPEntity(opened.read(), dict(opened.info()))
        finally:
            opened.close()

re_not_word = re.compile(r'\W+')

class ModuleCache(FileCache):
    """ A module cache. Give it a file name, it returns a module
        which results from the execution of the Python script it contains.
        This module is not inserted into sys.modules.
    """
    def __init__(self, max_size=0):
        FileCache.__init__(self, max_size, 'r')
    
    def build(self, key, name, opened, entry):
        try:
            module = new.module(re_not_word.sub('_',key))
            module.__file__ = key
            exec opened in module.__dict__
            return module
        finally:
            opened.close()

class HttpModuleCache(HTTPCache):
    """ A module cache. Give it an HTTP URL, it returns a module
        which results from the execution of the Python script it contains.
        This module is not inserted into sys.modules.
    """
    def __init__(self, max_size=0):
        HTTPCache.__init__(self, max_size)
    
    def build(self, key, name, opened, entry):
        try:
            module = new.module(re_not_word.sub('_',key))
            module.__file__ = key
            text = opened.read().replace('\r\n', '\n')
            code = compile(text, name, 'exec')
            exec code in module.__dict__
            return module
        finally:
            opened.close()

class FunctionCache(Cache):
    def __init__(self, function, max_size=0):
        Cache.__init__(self, max_size)
        self.function=function
    
    def __call__(self, *args, **kw):
        if kw:
            # a dict is not hashable so we build a tuple of (key, value) pairs
            kw = tuple(kw.iteritems())
            return self[args, kw]
        else:
            return self[args, ()]
    
    def build(self, key, name, opened, entry):
        args, kw = key
        return self.function(*args, **dict(kw))
