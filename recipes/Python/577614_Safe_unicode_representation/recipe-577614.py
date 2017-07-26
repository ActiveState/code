def safe_unicode(obj):
    """Return the unicode/text representation of `obj` without throwing UnicodeDecodeError

    Returned value is only a *representation*, not necessarily identical.
    """
    if type(obj) not in (six.text_type, six.binary_type):
        obj = six.text_type(obj)
    if type(obj) is six.text_type:
        return obj
    else:
        return obj.decode(errors='ignore')
