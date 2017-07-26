'''
    Win Registry module
    (_winreg wrapper)
'''
import _winreg as reg

# convenience dicts
vTyp={
    reg.REG_BINARY : 'BIN',
    reg.REG_DWORD : 'DW',
    reg.REG_DWORD_BIG_ENDIAN : 'DWB',
    reg.REG_DWORD_LITTLE_ENDIAN : 'DWL',
    reg.REG_EXPAND_SZ : 'XSZ',
    reg.REG_LINK : 'LNK',
    reg.REG_MULTI_SZ : 'MSZ',
    reg.REG_RESOURCE_LIST : 'RES',
    reg.REG_SZ : 'STR',
    reg.REG_NONE : 'NUL',
    }
rTyp=dict((v, k) for k, v in vTyp.items())

indent='\t'     # the string used for indented output

class Val(object):
    # Registry Value
    def __init__(self, key, name, val, typ):
        self.key, self.name, self.val, self.typ = key, name, val, typ
    @property
    def indented(self):
        return '%s%s' % (indent*(self.key.level+1), self.__str__())
    def __str__(self):
        val=' - bin -' if self.typ==rTyp['BIN']  else self.val
        return '%s : %s' % (self.name, val)

class Key(object):
    # Registry Key
    def __init__(self, parent, name):
        self.parent, self.name = parent, name
        self.level=parent.level+1
        # ! ! ! opens keys in read/write mode ! ! !
        self.wrk=reg.OpenKey(parent.wrk, self.name, 0, reg.KEY_ALL_ACCESS)
        self._keys = self._vals = None
    @property
    def keys(self):
        # returns a dict of subkeys
        if not self._keys:
            self._keys={}
            for i in xrange(reg.QueryInfoKey(self.wrk)[0]):
                name=reg.EnumKey(self.wrk, i).lower()
                try:
                    self._keys[name]=Key(self, name)
                except WindowsError: pass
        return self._keys
    @property
    def vals(self):
        # returns the list of values
        if not self._vals:
            self._vals=[]
            for i in xrange(reg.QueryInfoKey(self.wrk)[1]):
                try:
                    self._vals.append(Val(self, *reg.EnumValue(self.wrk, i)))
                except WindowsError: pass
        return self._vals
    def __call__(self, path):
        # access to a key
        path=path.lower()
        key=self
        for p in path.split('/'):
            key=key.keys[p]
        return key
    def __str__(self):
        return '%s%s/' % (self.parent.__str__(), self.name)
    @property
    def indented(self):
        return '%s%s' % (indent*self.level, self.name)
    def walk(self):
        # walk thru the subkeys tree
        for key in self.keys.itervalues():
            yield key
            for k in key.walk():
                yield k
    def grep(self, text, kv='both', typ=(rTyp['STR'],)):
        # searching keys and/or values for some text
        for k in self.walk():
            if kv in ('keys', 'both') and text in k.name:
                yield k, None
            if kv in ('vals', 'both'):
                for v in k.vals:
                    if (v.typ in typ) and (text in v.val):
                        yield k, v
    def grep2(self, text, kv='both', typ=(rTyp['STR'],)):
        # a grep variant, might be more convinient in some cases
        kb=None
        for k in self.walk():
            if kv in ('keys', 'both') and text in k.name:
                if kv=='both':
                    yield k, False
                    kb=k
                else:
                    yield k
            if kv in ('vals', 'both'):
                for v in k.vals:
                    if (v.typ in typ) and (text in v.val):
                        if kv=='both':
                            if k!=kb:
                                yield k, False
                                kb=k
                            yield v, True
                        else:
                            yield v
    def create(self, path):
        # create a subkey, and the path to it if necessary
        k=self
        for p in path.split('/'):
            if p in k.keys:
                k=k.keys[p]
            else:
                reg.CreateKey(k.wrk, p)
                k=Key(k, p)
        return k
    def setVal(self, name, val, typ='str'):
        # set value
        typ=typ.upper()
        if typ=='DW': typ='DWL'
        typ=rTyp[typ]
        reg.SetValueEx(self.wrk, name, 0, typ, val)

class Hkey(Key):
    # Registry HKey
    def __init__(self, name):
        self.parent=None
        self.level=0
        self.name=name
        self.wrk=reg.ConnectRegistry(None, getattr(reg, name))
        self._keys=None
        self._vals=None
    def __str__(self):
        return '/%s/' % self.name

class Root(Key):
    # Registry Root
    def __init__(self):
        self.hkey={}
        for key in (k for k in dir(reg) if k.startswith('HKEY_')):
            try:
                chk = reg.ConnectRegistry(None, getattr(reg, key))
                inf = reg.QueryInfoKey(chk)
                reg.CloseKey(chk)
            except WindowsError: pass           # some keys may appear in _winreg but can't be reached
            else:
                hk = Hkey(key)
                try:
                    chk=hk.keys
                except WindowsError: pass       # some keys can be accessed but not enumerated
                else:                           # some keys work fine ...
                    name=key[5:].lower()
                    self.hkey[name]=hk          # for iterating
                    setattr(self, name, hk)     # for easy access
    @property
    def keys(self):
        return self.hkey

root=Root()         # we should need only one Root per application, so let's instanciate it here.

if __name__=='__main__':
    try:
        print '\n---- Keys names -----\n'
        for k in root.local_machine('software/python/pythoncore/2.5').keys: print k
        print '\n---- Keys full paths -----\n'
        for k in root.local_machine('software/python/pythoncore/2.5').keys.itervalues(): print k
        print '\n---- SubTree walking -----\n'
        for k in root.local_machine('software/python').walk(): print k
        print '\n---- More readable -----\n'
        for k in root.local_machine('software/python').walk():
            print k.indented
            for v in k.vals:
                    print '%s   (- %s -)  ' % (v.indented, vTyp[v.typ])
        print '\n---- Searching the whole registry -----\n' # or at least what you have access to
        for k in root.walk():
            if 'interpreter' in k.name:
                print k
                for v in k.vals:
                    print '\t', v
                for sk in k.walk():
                    print sk
                    for sv in sk.vals:
                        print '\t', sv
        print '\n---- Looking for a string -----\n'
        kb=None
        for k, v in root.current_user.grep('python'):
            if v:
                if k!=kb:
                    print k
                    kb=k
                print '\t', v
            else:
                print k
                kb=k
        print '\n---- Same thing, the other way -----\n'
        for i, isval in root.current_user.grep2('python'):
            print '\t%s'%i if isval else i
        print '\n---- Gathering some stats -----\n'
        from collections import defaultdict
        kv=defaultdict(int)
        for k in root.walk():
            for v in k.vals:
                kv[vTyp.get(v.typ, v.typ)]+=1
        for k, v in sorted(kv.items()):
            print '%s\t%10i' % (k, v)
        print '\nTotal\t%10i' % sum(kv.values())
        print '\n---- Creating some keys and values -----\n'
        print root.current_user.create('p/y/t/h/o/n')
        root.current_user('software').create('python').setVal('BDFL', 'Guido')
        k=root.current_user('software/python')
        k.setVal('ver', 3000, 'dw')
        for v in k.vals:
            print '%s   (- %s -)  ' % (v, vTyp[v.typ])
    except UnicodeError: pass
