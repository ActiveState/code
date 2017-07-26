"""
Small scanf-implementation.

Python has powerful regular expressions but sometimes they are totally overkill
when you just want to parse a simple-formatted string.
C programmers use the scanf-function for these tasks (see link below).

This implementation of scanf translates the simple scanf-format into
regular expressions. Unlike C you can be sure that there are no buffer overflows
possible.


For more information see
  * http://www.python.org/doc/current/lib/node49.html
  * http://en.wikipedia.org/wiki/Scanf
"""
import re
import sys


__all__ = ["scanf"]


DEBUG = False



# As you can probably see it is relatively easy to add more format types
scanf_translate = [
    (re.compile(_token), _pattern, _cast) for _token, _pattern, _cast in [
    ("%c", "(.)", lambda x:x),
    ("%(\d)c", "(.{%s})", lambda x:x),
    ("%(\d)[di]", "([+-]?\d{%s})", int),
    ("%[di]", "([+-]?\d+)", int),
    ("%u", "(\d+)", int),
    ("%[fgeE]", "(\d+\.\d+)", float),
    ("%s", "(\S+)", lambda x:x),
    ("%([xX])", "(0%s[\dA-Za-f]+)", lambda x:int(x, 16)),
    ("%o", "(0[0-7]*)", lambda x:int(x, 7)),
    ]]



# Cache formats
SCANF_CACHE_SIZE = 1000
scanf_cache = {}


def _scanf_compile(format):
    """
    This is an internal function which translates the format into regular expressions
    
    For example:
    >>> format_re, casts = _scanf_compile('%s - %d errors, %d warnings')
    >>> print format_re.pattern
    (\S+) \- ([+-]?\d+) errors, ([+-]?\d+) warnings
    
    Translated formats are cached for faster use
    """
    compiled = scanf_cache.get(format)
    if compiled:
        return compiled

    format_pat = ""
    cast_list = []
    i = 0
    length = len(format)
    while i < length:
        found = None
        for token, pattern, cast in scanf_translate:
            found = token.match(format, i)
            if found:
                cast_list.append(cast)
                groups = found.groupdict() or found.groups()
                if groups:
                    pattern = pattern % groups
                format_pat += pattern
                i = found.end()
                break
        if not found:
            char = format[i]
            # escape special characters
            if char in "()[]-.+*?{}<>\\":
                format_pat += "\\"
            format_pat += char
            i += 1
    if DEBUG:
        print "DEBUG: %r -> %s" % (format, format_pat)
    format_re = re.compile(format_pat)
    if len(scanf_cache) > SCANF_CACHE_SIZE:
        scanf_cache.clear()
    scanf_cache[format] = (format_re, cast_list)
    return format_re, cast_list



def scanf(format, s=None):
    """
    scanf supports the following formats:
      %c       One character
      %5c      5 characters
      %d       int value
      %7d      int value with length 7
      %f       float value
      %o       octal value
      %X, %x   hex value
      %s       string terminated by whitespace

    Examples:
    >>> scanf("%s - %d errors, %d warnings", "/usr/sbin/sendmail - 0 errors, 4 warnings")
    ('/usr/sbin/sendmail', 0, 4)
    >>> scanf("%o %x %d", "0123 0x123 123")
    (66, 291, 123)


    If the parameter s is a file-like object, s.readline is called.
    If s is not specified, stdin is assumed.

    The function returns a tuple of found values
    or None if the format does not match.
    """

    if s == None: s = sys.stdin
    if hasattr(s, "readline"): s = s.readline()

    format_re, casts = _scanf_compile(format)
    found = format_re.match(s)
    if found:
        groups = found.groups()
        return tuple([casts[i](groups[i]) for i in range(len(groups))])



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, report=True)
