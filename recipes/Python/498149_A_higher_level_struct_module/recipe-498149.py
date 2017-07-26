import struct

class Format(object):
    """Endianness and size format for structures."""
    Native          = "@"       # Native format, native size
    StandardNative  = "="       # Native format, standard size
    LittleEndian    = "<"       # Standard size
    BigEndian       = ">"       # Standard size
    
class Element(object):
    """A single element in a struct."""
    id=0
    def __init__(self, typecode):
        Element.id+=1           # Note: not thread safe
        self.id = Element.id
        self.typecode = typecode
        self.size = struct.calcsize(typecode)

    def __len__(self):
        return self.size

    def decode(self, format, s):
        """Additional decode steps once converted via struct.unpack"""
        return s

    def encode(self, format, val):
        """Additional encode steps to allow packing with struct.pack"""
        return val

    def __str__(self):
        return self.typecode

    def __call__(self, num):
        """Define this as an array of elements."""
        # Special case - strings already handled as one blob.
        if self.typecode in 'sp':
            # Strings handled specially - only one item
            return Element('%ds' % num)
        else:
            return ArrayElement(self, num)

    def __getitem__(self, num): return self(num)

class ArrayElement(Element):
    def __init__(self, basic_element, num):
        Element.__init__(self, '%ds' % (len(basic_element) * num))
        self.num = num
        self.basic_element = basic_element

    def decode(self, format, s):
        # NB. We use typecode * size, not %s%s' % (size, typecode), 
        # so we deal with typecodes that already have numbers,  
        # ie 2*'4s' != '24s'
        return [self.basic_element.decode(format, x) for x in  
                    struct.unpack('%s%s' % (format, 
                            self.num * self.basic_element.typecode),s)]

    def encode(self, format, vals):
        fmt = format + (self.basic_element.typecode * self.num)
        return struct.pack(fmt, *[self.basic_element.encode(format,v) 
                                  for v in vals])

class EmbeddedStructElement(Element):
    def __init__(self, structure):
        Element.__init__(self, '%ds' % structure._struct_size)
        self.struct = structure

    # Note: Structs use their own endianness format, not their parent's
    def decode(self, format, s):
        return self.struct(s)

    def encode(self, format, s):
        return self.struct._pack(s)

name_to_code = {
    'Char'             : 'c',
    'Byte'             : 'b',
    'UnsignedByte'     : 'B',
    'Int'              : 'i',
    'UnsignedInt'      : 'I',
    'Short'            : 'h',
    'UnsignedShort'    : 'H',
    'Long'             : 'l',
    'UnsignedLong'     : 'L',
    'String'           : 's',  
    'PascalString'     : 'p',  
    'Pointer'          : 'P',
    'Float'            : 'f',
    'Double'           : 'd',
    'LongLong'         : 'q',
    'UnsignedLongLong' : 'Q',
    }

class Type(object):
    def __getattr__(self, name):
        return Element(name_to_code[name])

    def Struct(self, struct):
        return EmbeddedStructElement(struct)
        
Type=Type()

class MetaStruct(type):
    def __init__(cls, name, bases, d):
        type.__init__(cls, name, bases, d)
        if hasattr(cls, '_struct_data'):  # Allow extending by inheritance
            cls._struct_info = list(cls._struct_info) # use copy.
        else:
            cls._struct_data=''
            cls._struct_info=[]     # name / element pairs

        # Get each Element field, sorted by id.
        elems = sorted(((k,v) for (k,v) in d.iteritems() 
                        if isinstance(v, Element)),
                        key=lambda x:x[1].id)

        cls._struct_data += ''.join(str(v) for (k,v) in elems)
        cls._struct_info += elems
        cls._struct_size = struct.calcsize(cls._format + cls._struct_data)

class Struct(object):
    """Represent a binary structure."""
    __metaclass__=MetaStruct
    _format = Format.Native  # Default to native format, native size

    def __init__(self, _data=None, **kwargs):
        if _data is None:
            _data ='\0' * self._struct_size
            
        fieldvals = zip(self._struct_info, struct.unpack(self._format + 
                                             self._struct_data, _data))
        for (name, elem), val in fieldvals:
            setattr(self, name, elem.decode(self._format, val))
        
        for k,v in kwargs.iteritems():
            setattr(self, k, v)

    def _pack(self):
        return struct.pack(self._format + self._struct_data, 
            *[elem.encode(self._format, getattr(self, name)) 
                for (name,elem) in self._struct_info])                

    def __str__(self):
        return self._pack()
    
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self._pack())
    
###################################################################
#  End of implementation - usage examples follow:
###################################################################

###################################################################
#
# Usage
#
# Using the above code, we can now define structures in a
# more readable class based syntax.  For example:
###################################################################
    
class Point(Struct):
    _format = Format.LittleEndian
    x = Type.Short
    y = Type.Short
    
p = Point('\x01\x00\x02\x00')

print p.x, p.y   # Prints 1,2
p.x, p.y = 100,200
print repr(p)     # Prints "Point('d\x00\xc8\x00')

assert(struct.pack('<hh',100,200) == str(p))
    
###################################################################
#
# Arrays and Embedded structures
#
# You can also embed arrays, (and arrays of arrays), as well
# as other structures within your struct definition.
###################################################################

class Shape(Struct):
    _format = Format.BigEndian
    name      = Type.String[8]
    numpoints = Type.Int
    points    = Type.Struct(Point)[4] # Array of 4 points.

s=Shape('Triangle\x00\x00\x00\x03\x00\x00\x00\x00\x05\x00\x05\x00\n\x00'
        '\x00\x00\x00\x00\x00\x00')

# This will print "Triangle [(0,0), (5,5), (10,0)]"
print s.name, [(p.x, p.y) for p in s.points[:s.numpoints]]

# The same structure could be created as:
s2=Shape(name='Triangle', numpoints=3, points=[
                                         Point(x=0,y=0),
                                         Point(x=5,y=5),
                                         Point(x=10,y=0),
                                         Point(x=0,y=0)])

assert str(s2) == str(s)

# Note that even though Shape is in BigEndian format, the Points
# keep their LittleEndian setting, so mixing formats is possible,
# and the same struct will always have the same representation
# regardless of its context.  Hence the following is true:

assert str(s.points[1]) == str( Point(x=5, y=5))

# It is also possible to define multi-dimensional arrays,
# which will be unpacked as lists of lists.
# In addition, it is possible to add methods and non-struct
# instance variables without interfering with the structure
# (Unless you overwrite structure field names of course)

class TicTacToe(Struct):
    board = Type.Char[3][3] # 3x3 array of chars

    ignored = 'This is not packed / unpacked by the structure'
    
    def display(self):
        print '\n'.join(''.join(row) for row in self.board)

game = TicTacToe('X.O.X...O')
print game.board  # [['X', '.', 'O'], ['.', 'X', '.'], ['.', '.', 'O']]

game.display()
# Prints: X.O
#         .X.
#         ..O

game.board[0][1] = 'X'
game.display()
# Prints: XXO
#         .X.
#         ..O
print str(game) # prints 'XXO.X...O'


###################################################################
#
# Inheritance
#
# Structures may also be inherited from, in which case, additional
# fields will occur after the existing ones.
#
###################################################################

class Point3D(Point):
    z = Type.Short

p = Point3D(x=1, y=2, z=3)

print repr(p)   # prints Point3D('\x01\x00\x02\x00\x03\x00')
