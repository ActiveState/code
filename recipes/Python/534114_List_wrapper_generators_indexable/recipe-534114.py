# -*- coding: UTF-8 -*-

# Created by Florian Leitner on 2007-10-15.
# Copyright (c) 2007 Florian Leitner.
# All rights reserved.
 
# GNU GPL LICENSE
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; latest version thereof,
# available at: <http://www.gnu.org/licenses/gpl.txt>.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA

"""gcache module

Provides wrappers to allow generators to be accessed by subscript indices.

The generator is only iterated as far as required to return the requested
items.

Determining its length or using negative indices will automatically lead to
the complete consumption of the generator, as well as using any special syntax
like:

if elt in glist:
    ...

Copyright (c) 2007 Florian Leitner. All rights reserved.
"""

import os
from bsddb3 import db, dbshelve

__version__ = "1.0"
__author__ = "Florian Leitner"

class dbcache(list):
    """Extends the full functionality of lists to a generator.
    
    The generator items are stored in an external database. The storages is
    inteded to be as small as possible by storing only one copy of each
    generator item (uniqueness being defined as id(item)).
    
    Note the cache will restore items although if you extend this list beyond
    the generator, then delete items in your code, fetching them again from
    the cache (the item now has a new id!) and the again put them back into
    the cache. This does not break anything, but it is not very efficient.
    
    Using id() should be thread safe (the number id() returns is the address
    in memory), additionally the temporary storage created by this mechanism
    in /tmp uses id(self) and os.getpid() to create its own, thread- and
    process-safe cache.
    """
    
    dbfile_directory = "/tmp"
    dbfile_prefix = "bdbcache-"
    dbfile_suffix = ".bdb"
    
    def __init__(self, generator, directory=None, prefix=None, suffix=None):
        """Create a new generator list cache.
        
        generator - the generator to cache
        directory - optional directory to create the cache
                    (defaults to dbfile_directory)
        prefix - filename prefix for the cache (defaults to dbfile_prefix)
        suffix - filename suffix for the cache (defaults to dbfile_suffix)
        
        Following attributes are bound to the instance:
        generator - the generator itself
        uid - the unique ID of this cache ("%s-%s" % (os.getpid(), id(self))
        path - the path to the cachefile
        cache - the cache object
        
        Note that using negative indices automatically leads to consuming
        the whole generator.
        """
        assert hasattr(generator, "next") and \
            hasattr(generator, "__iter__")
        super(dbcache, self).__init__()
        if directory is None:
            directory = dbcache.dbfile_directory
        if prefix is None:
            prefix = dbcache.dbfile_prefix
        if suffix is None:
            suffix = dbcache.dbfile_suffix
        self.generator = generator
        self.uid = "%i-%i" % (os.getpid(), id(self))
        self.path = "%s/%s%s%s" % \
            (directory, suffix, self.uid, prefix)
        try:
            os.unlink(self.path)
        except OSError:
            pass
        self.__idx = None
        self.__len = None
        self.cache = dbshelve.DBShelf()
        self.cache.open(self.path, None, db.DB_HASH, db.DB_CREATE)
    
    def __del__(self):
        """Delete the instance and destroy the cache file (if it still
        exists).
        """
        self.cache.close()
        del self.cache
        try:
            os.unlink(self.path)
        except OSError:
            pass
    
    def __contains__(self, elm):
        """Checks if id(elt) == id(s[i]) for any i already cached."""
        key = self.__key(elm)
        return self.cache.has_key(key)
    
    def __getitem__(self, k):
        """Using a negative index will consume the generator."""
        if isinstance(k, slice):
            return [self.__getitem__(i)
                    for i in xrange(k.start, k.stop, k.step)]
        size = self.__size()
        if size <= k:
            try:
                self.__cache(k - size + 1)
            except StopIteration:
                raise IndexError("list index out of range")
        key = super(dbcache, self).__getitem__(k)
        return self.cache.get(key)
    
    def __getslice__(self, i, j):
        """Using negative indices will consume the generator."""
        size = self.__size()
        if size <= j:
            try:
                self.__cache(j - size + 1)
            except StopIteration:
                # note: Python does not raise anything if j is to large!
                pass
        return [self.cache.get(key)
                for key in super(dbcache, self).__getslice__(i, j)]
    
    def __iter__(self):
        """Return an iterator over all items - consumes the generator."""
        self.__idx = 0
        self.__len = self.__size()
        return self
    
    def __len__(self):
        """Calling len(s) will consume the generator."""
        try:
            while True:
                self.__next()
        except StopIteration:
            pass
        return self.__size()
    
    def __setitem__(self, k, v):
        """Replace s[k] with v and returns the original element."""
        old_key = super(dbcache, self).__getitem__(k)
        new_key = self.__key(v)
        old_val = self.cache.get(old_key)
        super(dbcache, self).__setitem__(k, new_key)
        if super(dbcache, self).count(old_key) == 0:
            self.cache.delete(old_key)
        if not self.cache.has_key(new_key):
            self.cache.put(new_key, v)
        return old_val
    
    def __cache(self, n):
        """Cache the next n elements or raises StopIteration."""
        i = 0
        while i < n:
            self.__next()
            i += 1
    
    def __key(self, elt):
        """Return the key for an element."""
        return str(id(elt))
    
    def __next(self):
        """Get the next element..."""
        elm = self.generator.next()
        # ...which raised a StopIteration - or now add it to the mapping
        key = self.__key(elm)
        super(dbcache, self).append(key)
        if not self.cache.has_key(key):
            self.cache.put(key, elm)
        return elm
    
    def __size(self):
        """Get the current size of the cache list."""
        return super(dbcache, self).__len__()
    
    def append(self, elm):
        key = self.__key(elm)
        super(dbcache, self).append(key)
        if not self.cache.has_key(key):
            self.cache.put(key, elm)
    
    def extend(self, iterable):
        for elm in iterable:
            self.append(elm)
    
    def count(self, elm):
        """Return number of i's for which id(s[i]) == id(elm)."""
        key = self.__key(elm)
        return super(dbcache, self).count(key)
    
    def index(self, elm, *args):
        """Return smallest i such that id(s[i]) == id(elm)."""
        key = self.__key(elm)
        return super(dbcache, self).index(key, *args)
    
    def insert(self, i, elm):
        key = self.__key(elm)
        super(dbcache, self).insert(i, key)
        if not self.cache.has_key(key):
            self.cache.put(key, elm)
    
    def next(self):
        """Next element - can consume the generator."""
        if self.__idx < self.__len:
            key = super(dbcache, self).__getitem__(self.__idx)
            self.__idx += 1
            return self.cache.get(key)
        else:
            return self.__next()
    
    def remove(self, elm):
        key = self.__key(elm)
        super(dbcache, self).remove(key)
        if super(dbcache, self).count(key) == 0:
            self.cache.delete(key)
    
    def pop(self, *i):
        key = super(dbcache, self).pop(*i)
        val = self.cache.get(key)
        if super(dbcache, self).count(key) == 0:
            self.cache.delete(key)
        return val
    
    def sort(self, *comp, **kws):
        keys = [super(dbcache, self).__getitem__(i)
                for i in xrange(self.__size())]
        values = [self.cache.get(k) for k in keys]
        values.sort(*comp, **kws)
        new_keys = [self.__key(v) for v in values]
        for i, k in enumerate(new_keys):
            super(dbcache, self).__setitem__(i, k)
