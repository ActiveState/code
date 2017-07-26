#!/usr/bin/env python

# recordjar.py - Parse a Record-Jar into a list of dictionaries.
# Copyright 2005 Lutz Horn <lutz.horn@gmx.de>
# Licensed unter the same terms as Python.

def parse_jar(flo):
    """Parse a Record-Jar from a file like object into a list of dictionaries.

    This method parses a file like object as described in "The Art of Unix
    Programming" <http://www.faqs.org/docs/artu/ch05s02.html#id2906931>.

    The records are divided by lines containing '%%'. Each record consists of
    one or more lines, each containing a key, a colon, and a value. Whitespace
    around both key and value are ignored.

    >>> import StringIO
    >>> flo = StringIO.StringIO("a:b\\nc:d\\n%%\\nx:y\\n")
    >>> out = parse_jar(flo)
    >>> print out
    [{'a': 'b', 'c': 'd'}, {'x': 'y'}]

    If a record contains a key more than once, the value for this key is a list
    containing the values in their order of occurence.

    >>> flo = StringIO.StringIO("a:b\\nc:d\\n%%\\nx:y\\nx:z\\n")
    >>> out = parse_jar(flo)
    >>> print out
    [{'a': 'b', 'c': 'd'}, {'x': ['y', 'z']}]

    Leading or trailing separator lines ('%%') and lines containing only
    whitespace are ignored.

    >>> flo = StringIO.StringIO("%%\\na:b\\nc:d\\n%%\\n\\nx:y\\nx:z\\n")
    >>> out = parse_jar(flo)
    >>> print out
    [{'a': 'b', 'c': 'd'}, {'x': ['y', 'z']}]
    """
    records = []
    for record in flo.read().split("%%"):
        dict = {}
        for line in [line for line in record.split("\n") if line.strip() != ""]:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            try:
                dict[key].append(value)
            except AttributeError:
                dict[key] = [dict[key], value]
            except KeyError:
                dict[key] = value
        if len(dict) > 0:
            records.append(dict)
    return records

def _test():
    import doctest, recordjar
    return doctest.testmod(recordjar)

if __name__ == "__main__":
    _test()
