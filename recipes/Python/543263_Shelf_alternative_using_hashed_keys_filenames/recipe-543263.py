#!/usr/bin/env python
# by Brian O. Bush, Thu 24-Jan-2008 06:53 bushbo
from __future__ import with_statement

import os, sys, pickle, md5, threading

# This file cache is thread-safe
class FileCache:
    def __init__(self, path): 
        self.path = path # path assumed existing; check externally
        if not os.path.exists(self.path): 
            os.makedirs(self.path)        
        self.gen_key = lambda x: md5.new(x).hexdigest()
        self.lock = threading.Lock()
    def get(self, key, default=None):
        with self.lock:
            retval = default
            fn = os.path.join(self.path, self.gen_key(key))
            try:
                f = file(fn, 'r')
                retval = pickle.load(f)
                f.close()                
            except IOError: pass
            return retval
    def __getitem__(self, key):
        return self.get(key)
    def __setitem__(self, key, value):
        with self.lock:
            fn = os.path.join(self.path, self.gen_key(key))
            f = open(fn, 'wb')
            pickle.dump(value.__dict__, f)
            f.close()

if __name__=='__main__':
    class Site:
        def __init__(self, name, hits=0):
            self.name = name
            self.hits = hits
        def __str__(self):
            return '%s, %d hits' % (self.name, self.hits)
    cache = FileCache('test')
    sites = [Site('cnn.com'), Site('kd7yhr.org', 1), Site('asdf.com', 3)]
    # We will use the site url as the key for our cache
    # Comment out the next two lines to test cache reading
    for site in sites:    
        cache[site.name] = site
    entry = cache.get('cnn.com')
    if entry: print Site(**entry)
