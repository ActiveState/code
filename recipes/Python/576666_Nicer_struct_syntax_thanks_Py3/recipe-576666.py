import struct

def preargs(cls):
    def _pre_init(*args1, **kwargs1):
        def _my_init(*args2, **kwargs2):
            args = args1 + args2
            kwargs1.update(kwargs2)
            return cls(*args, **kwargs1)
        return _my_init
    return _pre_init

class BinaryMetaType(type):
    def __getitem__(self, val):
        return array(self, val)

class BinaryType(metaclass=BinaryMetaType):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def to_binary(self, val):
        pass

    def from_binary(self, binary):
        pass

class SimpleBinaryType(BinaryType):
    def __init__(self, fmt):
        self._struct = struct.Struct(fmt)

    def to_binary(self, val):
        return self._struct.pack(val)

    def from_binary(self, binary):
        return (self._struct.size,
                self._struct.unpack(binary[:self._struct.size])[0])

@preargs
class array(BinaryType):
    def __init__(self, arrtype, arrlen, **kwargs):
        super().__init__(**kwargs)
        self._arrtype, self._arrlen = arrtype(**kwargs), arrlen

    def to_binary(self, val):
        res = []
        for i,v in enumerate(val):
            res.append(self._arrtype.to_binary(v))
            if i+1 == self._arrlen: break
        return b''.join(res)

    def from_binary(self, binary):
        res = []
        ssum = 0
        for i in range(self._arrlen):
            s,v = self._arrtype.from_binary(binary[ssum:])
            ssum += s
            res.append(v)
        return ssum, res

class dword(SimpleBinaryType):
    def __init__(self, **kwargs):
        super().__init__('I', **kwargs)

class char(SimpleBinaryType):
    def __init__(self, **kwargs):
        super().__init__('c', **kwargs)

class BinaryBuilder(dict):
    def __init__(self, **kwargs):
        self.members = []
        self._kwargs = kwargs

    def __setitem__(self, key, value):
        if key ==  '__module__': return
        if key not in self:
            self.members.append((key, value(**self._kwargs)))
        super().__setitem__(key, value)

class Binary(type):
    @classmethod
    def __prepare__(*bases, **kwargs):
        # In the future kwargs can contain things such as endianity
        # and alignment
        return BinaryBuilder(**kwargs)

    def __new__(cls, name, bases, classdict):
        # There are nicer ways of doing this, but as a hack it works
        def fixupdict(d):
            @classmethod
            def to_binary(clas, datadict):
                res = []
                for k,v in clas.members:
                    res.append(v.to_binary(datadict[k]))
                return b''.join(res)

            @classmethod
            def from_binary(cls, bytesin):
                res = {}
                ssum = 0
                for k,v in cls.members:
                    i, d = v.from_binary(bytesin[ssum:])
                    ssum += i
                    res[k] = d
                return ssum, res

            nd = {'to_binary': to_binary,
              'from_binary': from_binary,
              'members': d.members}
            return nd

        return super().__new__(cls, name, bases, fixupdict(classdict))


#### How one would use the above module

class BMP(metaclass=Binary):
    # The point was to try and get this C-like syntax
    bfType = char[2]
    bfSize = dword
    bfReserved = dword
    bfOffBits = dword

print(BMP.from_binary(b'BM6\x00$\x00\x00\x00\x00\x006\x00\x00\x00'))
print(BMP.to_binary(
    {'bfType': 'BM',
     'bfSize': 2359350,
     'bfReserved': 0,
     'bfOffBits': 54}))
