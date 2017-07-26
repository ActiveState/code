def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')


# ------------------------------------------------------------------------
# Sample code below to illustrate their usage

def write_unicode_to_file(filename, unicode_text):
    """
    Write unicode_text to filename in UTF-8 encoding.
    Parameter is expected to be unicode. But it will also tolerate byte string.
    """
    fp = file(filename,'wb')
    # workaround problem if caller gives byte string instead
    unicode_text = safe_unicode(unicode_text)
    utf8_text = unicode_text.encode('utf-8')
    fp.write(utf8_text)
    fp.close()
