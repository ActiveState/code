#!/usr/bin/env python

def enum(*sequential, **named):
    # Check for duplicate keys
    names = list(sequential)
    names.extend(named.keys())
    if len(set(names)) != len(names):
        raise KeyError('Cannot create enumeration with duplicate keys!')

    # Build property dict
    enums = dict(zip(sequential, range(len(sequential))), **named)
    if not enums:
        raise KeyError('Cannot create empty enumeration')

    if len(set(enums.values())) < len(enums):
        raise ValueError('Cannot create enumeration with duplicate values!')

    # Function to be called as fset/fdel
    def err_func(*args, **kwargs):
        raise AttributeError('Enumeration is immutable!')

    # function to be called as fget
    def getter(cls, val):
        return lambda cls: val

    # Create a base type
    t = type('enum', (object,), {})

    # Add properties to class by duck-punching
    for attr, val in enums.iteritems():
        setattr(t, attr, property(getter(t, val), err_func, err_func))

    # Return an instance of the new class
    return t()


if __name__ == "__main__":
    """A small ammount of code to demo the functionality"""
    try:
        print 'Creating empty enum...',
        e = enum()
        print 'OK!'
    except KeyError as e:
        print 'ERROR:', e

    try:
        print 'Creating enum with duplicate keys...',
        e = enum('OK', 'OK', OK=2)
        print 'OK!'
    except KeyError as e:
        print 'ERROR:', e

    try:
        print 'Creating enum with duplicate values...',
        e = enum(OK=1, PASS=1)
        print 'OK!'
    except ValueError as e:
        print 'ERROR:', e

    try:
        print 'Creating valid enum...',
        e = enum('OK', 'CANCEL', 'QUIT', test=4, ok='YES')
        print 'OK!'
    except Exception as e:
        print 'ERROR:', e

    # Immutable?
    try:
        print 'Changing e.OK = "ASDF"...',
        e.OK = 'ASDF'
        print 'OK!'
    except AttributeError as ex:
        print 'ERROR:', ex

    try:
        print 'Deleting e.OK...',
        del e.OK
        print 'OK!'
    except AttributeError as ex:
        print 'ERROR:', ex

    print e
    print e.OK
    print e.CANCEL
    print e.QUIT
    print e.test
    print e.ok
