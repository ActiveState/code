import memcache
import simplejson
 
class SimplejsonWrapper(object):
    def __init__(self, file, protocol=None):
        self.file = file
 
    def dump(self, value)
        simplejson.dump(value, self.file)
 
    def load(self):
        return simplejson.load(self.file)


cache = memcache.Client(['127.0.0.1:11211'], pickler=SimplejsonWrapper, unpickler=SimplejsonWrapper)
