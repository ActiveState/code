def oa(o):
    for at in dir(o):
        print at,

'''
Sample calls and output for oa() below:

# object attributes of a dict:
oa({})
__class__ __cmp__ __contains__ __delattr__ __delitem__ __doc__ __eq__ __format__
__ge__ __getattribute__ __getitem__ __gt__ __hash__ __init__ __iter__ __le__ __len__ 
__lt__ __ne__ __new__ __reduce__ __reduce_ex__ __repr__ __setattr__ __setitem__ 
__sizeof__ __str__ __subclasshook__ clear copy fromkeys get has_key items
iteritems iterkeys itervalues keys pop popitem setdefault update values viewitems 
viewkeys viewvalues

# object attributes of a list:
oa([])
__add__ __class__ __contains__ __delattr__ __delitem__ __delslice__ __doc__ __eq__ 
__format__ __ge__ __getattribute__ __getitem__ __getslice__ __gt__ __hash__ __iadd__ 
__imul__ __init__ __iter__ __le__ __len__ __lt__ __mul__ __ne__ __new__
__reduce__ __reduce_ex__ __repr__ __reversed__ __rmul__ __setattr__ __setitem__
__setslice__ __sizeof__ __str__ __subclasshook__ append count extend index insert 
pop remove reverse sort

# object attributes of an int:
oa(1)
__abs__ __add__ __and__ __class__ __cmp__ __coerce__ __delattr__ __div__ __divmod__ 
__doc__ __float__ __floordiv__ __format__ __getattribute__ __getnewargs__ __hash__ 
__hex__ __index__ __init__ __int__ __invert__ __long__ __lshift__ __mod__
__mul__ __neg__ __new__ __nonzero__ __oct__ __or__ __pos__ __pow__ __radd__ __rand__ 
__rdiv__ __rdivmod__ __reduce__ __reduce_ex__ __repr__ __rfloordiv__ __rlshift__ 
__rmod__ __rmul__ __ror__ __rpow__ __rrshift__ __rshift__ __rsub__ __rtruediv__ 
__rxor__ __setattr__ __sizeof__ __str__ __sub__ __subclasshook__ __truediv__ 
__trunc__ __xor__ bit_length conjugate denominator imag numerator real
'''

def oar(o):
    for at in dir(o):
        if not at.startswith('__') and not at.endswith('__'):
            print at,

'''
# regular (meaning non-dunder) object attributes of a dict:
oar({})
clear copy fromkeys get has_key items iteritems iterkeys itervalues keys pop popitem 
setdefault update values viewitems viewkeys viewvalues

# regular object attributes of an int:
oar(1)
bit_length conjugate denominator imag numerator real

# regular object attributes of a string:
oar('')
_formatter_field_name_split _formatter_parser capitalize center count decode encode 
endswith expandtabs find format index isalnum isalpha isdigit islower isspace 
istitle isupper join ljust lower lstrip partition replace rfind rindex rjust rpartition 
rsplit rstrip split splitlines startswith strip swapcase title translate upper zfil
'''
