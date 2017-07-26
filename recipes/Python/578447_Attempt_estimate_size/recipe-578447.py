from sys import getsizeof
import types
from inspect import getmembers
from collections import (deque, defaultdict, Counter,
                                    OrderedDict, Iterable)


types_basic = {
e[1] for e in filter(lambda x: isinstance(x[1], type),
                     getmembers(types))
}
types_basic.discard(types.InstanceType)
types_basic.discard(types.ObjectType)

#for method-wrappers
types_basic.add(type(types_basic.__str__))

types_kv = {dict, OrderedDict, defaultdict, types.DictProxyType, Counter}
types_listlike = {list, set, frozenset, tuple, deque}

types_basic -= types_kv
types_basic -= types_listlike

types_kv = tuple(types_kv)
types_listlike = tuple(types_listlike)
types_basic = tuple(types_basic)

def get_size_of(obj):
    """Non-recursive function, that takes Python object,
    walk through its sub-objects and return a sum of size of each pointers
    and basic types.

    """
    size = 0
    seen = set()
    stack = deque()

    stack.append(obj)
    seen.add(id(obj))

    while stack:
        cur = stack.pop()

        size += getsizeof(cur)
        if isinstance(cur, types_basic):
            seen.add(cur)
        elif isinstance(cur, types_listlike):
            for e in list(cur):
                if id(e) not in seen:
                    stack.append(e)
                    seen.add(id(e))
        elif isinstance(cur, types_kv):
            for k, v in cur.items():
                if id(k) not in seen:
                    stack.append(k)
                    seen.add(id(k))
                if id(v) not in seen:
                    stack.append(v)
                    seen.add(id(v))
        else:
            for attr in dir(cur):
                try:
                    o = getattr(cur, attr)
                except AttributeError:
                    continue
                if id(o) not in seen:
                    stack.append(o)
                    seen.add(id(o))
    return size
