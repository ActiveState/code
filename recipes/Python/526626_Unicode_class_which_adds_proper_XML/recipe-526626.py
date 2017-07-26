from sys import getdefaultencoding
from xml.sax.saxutils import quoteattr


class UnicodeXML(unicode):
    r"""Version of the unicode class which adds XML declaration on encoding.

    >>> xml = UnicodeXML("<root>Root</root>")
    >>> print xml.encode("windows-1251")
    <?xml version="1.0" encoding="windows-1251"?>
    <root>Root</root>
    >>> print xml.encode("utf-8")
    <?xml version="1.0" encoding="utf-8"?>
    <root>Root</root>

    If XML declaration already present it will be removed:

    >>> xml = UnicodeXML(
    ...     '<?xml version="1.0" encoding="utf-8"?>\n<root>Root</root>')
    >>> print xml.encode("windows-1251")
    <?xml version="1.0" encoding="windows-1251"?>
    <root>Root</root>
    """

    def encode(self, *args):
        if len(args) > 2:
            raise TypeError("too much arguments for encode()")
        elif not args:
            encoding = getdefaultencoding()
        else:
            encoding = args[0]

        if not self.startswith("<?xml"):
            body = self
        else:
            try:
                i = self.index("?>")
            except ValueError:
                raise ValueError("unproper XML declaration")
            body = self[i + 2:].lstrip()

        decl = '<?xml version="1.0" encoding=%s?>\n' % quoteattr(encoding)
        return decl + unicode(body).encode(*args)
