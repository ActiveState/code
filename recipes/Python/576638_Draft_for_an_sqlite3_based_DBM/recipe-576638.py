#!/usr/bin/env python3.0
''' Dbm based on sqlite -- Needed to support shelves

Key and values are always stored as bytes. This means that when strings are
used they are implicitly converted to the default encoding before being
stored.

Issues:

    # ??? how to coordinate with whichdb
    # ??? Size of text fields fixed or varchar (do we need blobs)
    # ??? does default encoding affect str-->bytes or PySqlite3 always use UTF-8
    # ??? if pure python overhead and pysqlite overhead is too high, rewrite in C
'''

__all__ = ['error', 'open']

import sqlite3
import collections
from operator import itemgetter

error = sqlite3.DatabaseError

class SQLhash(collections.MutableMapping):

    def __init__(self, filename=':memory:', flags='r', mode=None):
        # XXX add flag/mode handling
        #   c -- create if it doesn't exist
        #   n -- new empty
        #   w -- open existing
        #   r -- readonly

        MAKE_SHELF = 'CREATE TABLE IF NOT EXISTS shelf (key TEXT NOT NULL, value TEXT NOT NULL)'
        MAKE_INDEX = 'CREATE UNIQUE INDEX IF NOT EXISTS keyndx ON shelf (key)'
        self.conn = sqlite3.connect(filename)
        self.conn.text_factory = bytes
        self.conn.execute(MAKE_SHELF)
        self.conn.execute(MAKE_INDEX)
        self.conn.commit()

    def __len__(self):
        GET_LEN =  'SELECT COUNT(*) FROM shelf'
        return self.conn.execute(GET_LEN).fetchone()[0]

    def keys(self):
        return SQLhashKeysView(self)

    def values(self):
        return SQLhashValuesView(self)

    def items(self):
        return SQLhashItemsView(self)

    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, key):
        GET_ITEM = 'SELECT value FROM shelf WHERE key = ?'
        return self.conn.execute(GET_ITEM, (key,)).fetchone() is not None

    def __getitem__(self, key):
        GET_ITEM = 'SELECT value FROM shelf WHERE key = ?'
        item = self.conn.execute(GET_ITEM, (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key, value):       
        ADD_ITEM = 'REPLACE INTO shelf (key, value) VALUES (?,?)'
        self.conn.execute(ADD_ITEM, (key, value))
        self.conn.commit()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        DEL_ITEM = 'DELETE FROM shelf WHERE key = ?'       
        self.conn.execute(DEL_ITEM, (key,))
        self.conn.commit()

    def update(self, items=(), **kwds):
        if isinstance(items, collections.Mapping):
            items = items.items()
        UPDATE_ITEMS = 'REPLACE INTO shelf (key, value) VALUES (?, ?)'
        self.conn.executemany(UPDATE_ITEMS, items)
        self.conn.commit()
        if kwds:
            self.update(kwds)

    def clear(self):        
        CLEAR_ALL = 'DELETE FROM shelf;  VACUUM;'        
        self.conn.executescript(CLEAR_ALL)
        self.conn.commit()

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def __del__(self):
        self.close()    

class ListRepr:

    def __repr__(self):
        return repr(list(self))    

class SQLhashKeysView(collections.KeysView, ListRepr):
    
    def __iter__(self):
        GET_KEYS = 'SELECT key FROM shelf ORDER BY ROWID'
        return map(itemgetter(0), self._mapping.conn.cursor().execute(GET_KEYS))

class SQLhashValuesView(collections.ValuesView, ListRepr):
    
    def __iter__(self):
        GET_VALUES = 'SELECT value FROM shelf ORDER BY ROWID'
        return map(itemgetter(0), self._mapping.conn.cursor().execute(GET_VALUES))

class SQLhashItemsView(collections.ValuesView, ListRepr):
    
    def __iter__(self):
        GET_ITEMS = 'SELECT key, value FROM shelf ORDER BY ROWID'
        return iter(self._mapping.conn.cursor().execute(GET_ITEMS))

def open(file=None, *args):
    if file is not None:
        return SQLhash(file)
    return SQLhash()


if __name__ in '__main___':
    for d in SQLhash(), SQLhash('example'):
        print(list(d), "start")
        d['abc'] = 'lmno'
        print(d['abc'])    
        d['abc'] = 'rsvp'
        d['xyz'] = 'pdq'
        print(d.items())
        print(d.values())
        print(d.keys())
        print(list(d), 'list')
        d.update(p='x', q='y', r='z')
        print(d.items())
        
        del d['abc']
        try:
            print(d['abc'])
        except KeyError:
            pass
        else:
            raise Exception('oh noooo!')
        
        try:
            del d['abc']
        except KeyError:
            pass
        else:
            raise Exception('drat!')

        print(list(d))
        d.clear()
        print(list(d))
        d.update(p='x', q='y', r='z')
        print(list(d))
        d['xyz'] = 'pdq'

        print()
        d.close()
