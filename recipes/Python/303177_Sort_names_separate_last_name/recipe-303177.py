"""Provides functionality for taking in an iterable that returns names and then
separates them by last name initial and sorts them."""

import itertools

def groupnames(name_iterable):
    """Return a dict keyed by last name initial with a value of a tuple of the
    names sorted by last first name.

    The items returned by name_iterable are expected to be strings containing
    the names formatted as ``first middle last`` with middle being optional.

    >>> groupnames(('Anna Martelli', 'Alex Martelli', 'Todd Cannon', 'Gwen C',
    ... 'John Doe'))
    {'C': ('Gwen C', 'Todd Cannon'), 'M': ('Alex Martelli', 'Anna Martelli'), 'D': ('John Doe',)}

    """
    sorted_names = sorted(name_iterable, key=sortkeyfunc)
    name_dict = {}
    for key, group in itertools.groupby(sorted_names, groupkeyfunc):
        name_dict[key] = tuple(group)
    return name_dict

def sortkeyfunc(name):
    """Return name in last-first-middle order"""
    name_parts = name.split()
    new_name = ' '.join((name_parts[-1], name_parts[0]))
    if len(name_parts) == 3:
        new_name = ' '.join((new_name, name_parts[1]))
    return new_name

def groupkeyfunc(name):
    """Return the last name initial"""
    return name.split()[-1][0]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
