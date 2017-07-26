from __future__ import print_function
import sys

# data_type_sizes_w_list_comp.py
# A program to show the sizes in bytes, of values of various 
# Python data types.`

# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram - https://vasudevram.github.io

#class Foo:
class Foo(object):
    pass

def gen_func():
    yield 1

def setup_data():
    a_bool = bool(0)
    an_int = 0
    a_long = long(0)
    a_float = float(0)
    a_complex = complex(0, 0)
    a_str = ''
    a_tuple = ()
    a_list = []
    a_dict = {}
    a_set = set()
    an_iterator = iter([1, 2, 3])
    a_function = gen_func
    a_generator = gen_func()
    an_instance = Foo()

    data = (a_bool, an_int, a_long, a_float, a_complex,
        a_str, a_tuple, a_list, a_dict, a_set,
        an_iterator, a_function, a_generator, an_instance)
    return data

data = setup_data()

print("\nPython data type sizes:\n")

header = "{} {} {}".format(\
    "Data".center(10), "Type".center(15), "Length".center(10))
print(header)
print('-' * 40)

rows = [ "{} {} {}".format(\
    repr(item).center(10), str(type(item)).center(15), \
    str(sys.getsizeof(item)).center(10)) for item in data[:-4] ]
print('\n'.join(rows))
print('-' * 70)

rows = [ "{} {} {}".format(\
    repr(item).center(10), str(type(item)).center(15), \
    str(sys.getsizeof(item)).center(10)) for item in data[-4:] ]
print('\n'.join(rows))
print('-' * 70)
