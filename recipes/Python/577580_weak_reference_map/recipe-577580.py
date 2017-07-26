#!/usr/bin/env python
# 
#   Copyright 2010-  Hui Zhang
#   E-mail: hui.zh012@gmail.com
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from functools import partial
from weakref import ref

### weak ref key holder
def _ref(value, ondel):
    try:
        vref = ref(value, ondel)
    except:
        vref = lambda:value
    return vref

class weakmap(object):
    def __init__(self):
        self.__map = {}
        self.__valmemo = {}
        self.__backref = {}
        
    def set(self, key, value):
        ikey, ival = id(key), id(value)
        self.__map[ikey] = (ival, 
                            _ref(key, partial(self.forget_key, ikey))
                            )
        if ival not in self.__valmemo:
            self.__valmemo[ival] = _ref(value, partial(self.forget_value, ival))
        self.__backref.setdefault(ival, set()).add(ikey)
            
    def get(self, key, **kwargs):
        ikey = id(key)
        if ikey in self.__map:
            return self.__valmemo[self.__map[ikey][0]]()
        if 'default' in kwargs:
            return kwargs['default']
        raise KeyError(str(key))
    
    def pop(self, key):
        ikey = id(key)
        if ikey in self.__map:
            value = self.__valmemo[self.__map[ikey][0]]()
            self.forget_key(ikey)
            return value
        else:
            raise KeyError(str(key))     

    def forget_key(self, keyid, obj=None):
        if keyid in self.__map:
            ival = self.__map.pop(keyid)[0]
            self.__backref[ival].remove(keyid)
            if not self.__backref[ival]:
                self.__backref.pop(ival)
                self.__valmemo.pop(ival)
            
    def forget_value(self, valueid, obj=None):
        for ikey in self.__backref.get(valueid, ()):
            if ikey in self.__map: 
                self.__map.pop(ikey)
        for d in [self.__backref, self.__valmemo]:
            if valueid in d: 
                d.pop(valueid)
            
    def __iter__(self):
        for k, v in self.__map.iteritems():
            k = v[1]()
            v = self.__valmemo[v[0]]()
            yield (k, v)

class weakkeymap(object):
    def __init__(self):
        self.__map = {}
        
    def set(self, key, value):
        ikey = id(key)
        self.__map[ikey] = (value, 
                            _ref(key, partial(self.forget_key, ikey))
                            )
            
    def get(self, key, **kwargs):
        ikey = id(key)
        if ikey in self.__map:
            return self.__map[ikey][0]
        if 'default' in kwargs:
            return kwargs['default']
        raise KeyError(str(key))
    
    def pop(self, key):
        ikey = id(key)
        if ikey in self.__map:
            return self.__map.pop(ikey)[0]
        else:
            raise KeyError(str(key))     

    def forget_key(self, keyid, obj=None):
        if keyid in self.__map:
            self.__map.pop(keyid)
            
    def __iter__(self):
        for k, v in self.__map.iteritems():
            k = v[1]()
            yield (k, v[0])
