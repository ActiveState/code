def protect_utf8(wrapped_function, encoding='UTF-8'):

    """Temporarily convert a UTF-8 string to Unicode to prevent breakage.

    protect_utf8 is a function decorator that can prevent naive
    functions from breaking UTF-8.

    If the wrapped function takes a string, and that string happens to be valid
    UTF-8, convert it to a unicode object and call the wrapped function.  If a
    conversion was done and if a unicode object was returned, convert it back
    to a UTF-8 string.

    The wrapped function should take a string as its first parameter and it may
    return an object of the same type.  Anything else is optional.  For
    example:

        def truncate(s):
            return s[:1]

    Pass "encoding" if you want to protect something other than UTF-8.

    Ideally, we'd have unicode objects everywhere, but sometimes life is not
    ideal. :)

    """

    def proxy_function(s, *args, **kargs):
        unconvert = False
        if isinstance(s, str):
            try:
                s = s.decode(encoding) 
		unconvert = True
	    except UnicodeDecodeError:
	        pass
	ret = wrapped_function(s, *args, **kargs)
	if unconvert and isinstance(ret, unicode):
	    ret = ret.encode(encoding)
	return ret

    return proxy_function


def truncate(s, length=1, etc="..."):
    """Truncate a string to the given length.

    If truncation is necessary, append the value of "etc".

    This is really just a silly test.

    """
    if len(s) < length:
        return s
    else:
        return s[:length] + etc
truncate = protect_utf8(truncate)           # I'm stuck on Python 2.3.


if __name__ == '__main__':
    assert (truncate('\xe3\x82\xa6\xe3\x82\xb6\xe3\x83\x86', etc="") == 
            '\xe3\x82\xa6')
    assert truncate('abc') == 'a...'
    assert truncate(u'\u30a0\u30b1\u30c3', etc="") == u'\u30a0'
