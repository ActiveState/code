from types import IntType, TupleType, StringType, FloatType, LongType, ListType, DictType, NoneType
from struct import pack, unpack
from cStringIO import StringIO

class EncodeError(Exception):
    pass
class DecodeError(Exception):
    pass

#contains dictionary of coding functions, where the dictionary key is the type.
encoder = {}

def enc_dict_type(obj):
    data = "".join([encoder[type(i)](i) for i in obj.items()])
    return "%s%s%s" % ("D", pack("!L", len(data)), data)
encoder[DictType] = enc_dict_type

def enc_list_type(obj):
    data = "".join([encoder[type(i)](i) for i in obj])
    return "%s%s%s" % ("L", pack("!L", len(data)), data)
encoder[ListType] = enc_list_type

def enc_tuple_type(obj):
    data = "".join([encoder[type(i)](i) for i in obj])
    return "%s%s%s" % ("T", pack("!L", len(data)), data)
encoder[TupleType] = enc_tuple_type

def enc_int_type(obj):
    return "%s%s" % ("I", pack("!i", obj))
encoder[IntType] = enc_int_type

def enc_float_type(obj):
    return "%s%s" % ("F", pack("!f", obj))
encoder[FloatType] = enc_float_type

def enc_long_type(obj):
    obj = hex(obj)[2:-1]
    return "%s%s%s" % ("B", pack("!L", len(obj)), obj)
encoder[LongType] = enc_long_type

def enc_string_type(obj):
    return "%s%s%s" % ("S", pack("!L", len(obj)), obj)
encoder[StringType] = enc_string_type

def enc_none_type(obj):
    return "N"
encoder[NoneType] = enc_none_type

def encode(obj):
    """Encode simple Python types into a binary string."""
    try:
        return encoder[type(obj)](obj)
    except KeyError, e:
        raise EncodeError, "Type not supported. (%s)" % e

#contains dictionary of decoding functions, where the dictionary key is the type prefix used.
decoder = {}

def build_sequence(data, cast=list):
    size = unpack('!L', data.read(4))[0]
    items = []
    data_tell = data.tell
    data_read = data.read
    items_append = items.append
    start_position = data.tell()
    while (data_tell() - start_position) < size:
        T = data_read(1)
        value = decoder[T](data)
        items_append(value)
    return cast(items)

def dec_tuple_type(data):
    return build_sequence(data, cast=tuple)
decoder["T"] = dec_tuple_type

def dec_list_type(data):
    return build_sequence(data, cast=list)
decoder["L"] = dec_list_type

def dec_dict_type(data):
    return build_sequence(data, cast=dict)
decoder["D"] = dec_dict_type

def dec_long_type(data):
    size = unpack('!L', data.read(4))[0]
    value = long(data.read(size),16)
    return value
decoder["B"] = dec_long_type

def dec_string_type(data):
    size = unpack('!L', data.read(4))[0]
    value = str(data.read(size))
    return value
decoder["S"] = dec_string_type

def dec_float_type(data):
    value = unpack('!f', data.read(4))[0]
    return value
decoder["F"] = dec_float_type

def dec_int_type(data):
    value = unpack('!i', data.read(4))[0]
    return value
decoder['I'] = dec_int_type

def dec_none_type(data):
    return None
decoder['N'] = dec_none_type

def decode(data):
    """
    Decode a binary string into the original Python types.
    """
    buffer = StringIO(data)
    try:
        value = decoder[buffer.read(1)](buffer)
    except KeyError, e:
        raise DecodeError, "Type prefix not supported. (%s)" % e
    return value


if __name__ == "__main__":
    value = [None,["simon","wittber"],(1,2),{1:2.1,3:4.3},999999999999999999999999999999999999999]
    data = encode(value)
    print data
    x = decode(data)
    for item in zip(value,x):
        print item[0],"---",item[1]
    print "-" * 10
    print x
