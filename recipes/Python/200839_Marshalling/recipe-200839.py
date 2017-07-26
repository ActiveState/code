"""
contains a function for marshalling literal (and only literal) Python
data into Javascript. Supports Python None, strings, ints and floats,
dates, lists, tuples and dictionaries.
"""

import re
_jsidentifierRE=re.compile(r'[a-zA-Z_\$][a-zA-Z_\$0-9]*$')

def is_valid_js_identifier(s):
    try:
        return bool(_jsidentifierRE.match(s))
    except TypeError:
        return 0

class MarshalException(ValueError):
    pass

class InvalidIdentifierException(MarshalException):
    pass

def get_identifier(s):
    if is_valid_js_identifier(s):
        return s
    raise InvalidIdentifierException, \
          "not a valid Javascript identifier: %s" % s

_marshalRegistry={str: repr,
                  int: repr,
                  float: repr,
                  type(None): lambda x: 'null'}

def _seq_to_js(s):
    return "[%s]" % ', '.join([to_js(y) for y in s])

_marshalRegistry[list]=_seq_to_js
_marshalRegistry[tuple]=_seq_to_js

def _dict_to_js(d):
    s=', '.join(["%s: %s" % (get_identifier(k), to_js(v)) \
                 for k, v in d.items()])
    return "{%s}" % s

_marshalRegistry[dict]=_dict_to_js

try:
    import mx.DateTime as M
except ImportError:
    pass
else:
    def _date_to_js(dt):
        return "new Date(%s)" % int(dt.ticks())
    _marshalRegistry[type(M.now())]=_date_to_js

def to_js(obj):
    # the isinstance test permits type subclasses
    for k in _marshalRegistry:
        if isinstance(obj, k):
            return _marshalRegistry[k](obj)
    raise MarshalException, obj
        
