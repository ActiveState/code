from sets import Set
import string

class KeyedDict(dict):

    def __init__(self,keys):
        self.__keys = Set(keys)

    def __setitem__(self,key,val):
        if key not in self.__keys:
            keylist = string.join(self.__keys,",")
            raise TypeError("Tried to use key '"+key+"'.\nCan only add items with one of the following keys: "+keylist)

        return dict.__setitem__(self,key,val)

if __name__ == '__main__':

    d = KeyedDict(("fred","barney"))

    ## these should work
    d['fred']='flintstone'
    d['barney']='rubble'

    ## now catch the exception
    try:
        d['wilma']='flintstone'
    except TypeError,e:
        print "TypeError correctly thrown"
