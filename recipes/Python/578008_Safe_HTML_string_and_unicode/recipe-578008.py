from xml.sax.saxutils import quoteattr


class SafeHTMLMixin(object):

    def sanitize(self, s):
        """sanitize value following
        https://www.owasp.org/index.php/XSS_%28Cross_Site_Scripting%29_Prevention_Cheat_Sheet#RULE_.231_-_HTML_Escape_Before_Inserting_Untrusted_Data_into_HTML_Element_Content
        """
        if isinstance(s, (list, tuple)):
            return tuple(self.sanitize(x) for x in s)
        elif not isinstance(s, SafeHTMLMixin):
            return quoteattr(
                s,
                entities={'"': '&quot;', '/': '&#x2F;', "'": '&#x27;'})[1:-1]
        else:
            return s

    def __add__(self, s):
        return self.__class__(super(SafeHTMLMixin, self).__add__(self.sanitize(s)))

    def __radd__(self, s):
        return self.__class__(self.sanitize(s)) + self

    def __mul__(self, i):
        return self.__class__(super(SafeHTMLMixin, self).__mul__(i))

    def __rmul__(self, i):
        return self.__class__(super(SafeHTMLMixin, self).__rmul__(i))

    def __mod__(self, s):
        return self.__class__(super(SafeHTMLMixin, self).__mod__(self.sanitize(s)))

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           super(SafeHTMLMixin, self).__repr__())


class SafeHTMLStr(SafeHTMLMixin, str):
    """a string that will sanitize all str concatenated to it (or inserted
    via format)

    SafeHTMLStr itself is not quoted::

      >>> SafeHTMLStr('<ABC/>') + SafeHTMLStr('<script src="x"/>')
      SafeHTMLStr('<ABC/><script src="x"/>')

    While any string or unicode input is quoted and keep being SafeHTML::
      
      >>> SafeHTMLStr('<ABC/>') + '<script src="x"/>'
      SafeHTMLStr('<ABC/>&lt;script src=&quot;x&quot;&#x2F;&gt;')

      >>> SafeHTMLStr('<ABC/>') + u'<script src="x"/>'
      SafeHTMLStr('<ABC/>&lt;script src=&quot;x&quot;&#x2F;&gt;')
      
      >>> '<script src="x"/>' + SafeHTMLStr('<ABC/>')
      SafeHTMLStr('&lt;script src=&quot;x&quot;&#x2F;&gt;<ABC/>')
      
      >>> SafeHTMLStr('<ABC/>') * 2
      SafeHTMLStr('<ABC/><ABC/>')
      
      >>> SafeHTMLStr('<ABC>%s</ABC>') % '<script src="x"/>'
      SafeHTMLStr('<ABC>&lt;script src=&quot;x&quot;&#x2F;&gt;</ABC>')
      
      >>> SafeHTMLStr('<ABC %s>%s</ABC>') % (
      ...      SafeHTMLStr('spam="foo"'), '<script src="x"/>')
      SafeHTMLStr('<ABC spam="foo">&lt;script src=&quot;x&quot;&#x2F;&gt;</ABC>')
    """


class SafeHTMLUnicode(SafeHTMLMixin, unicode):
    """a unicode string that will sanitize all str concatenated to it
    (or inserted via format)

    SafeHTMLUnicode itself is not quoted::

      >>> SafeHTMLUnicode(u'<ABC/>') + SafeHTMLUnicode(u'<script src="x"/>')
      SafeHTMLUnicode(u'<ABC/><script src="x"/>')

    While any string or unicode input is quoted and keep being SafeHTML::
      
      >>> SafeHTMLUnicode(u'<ABC/>') + '<script src="x"/>'
      SafeHTMLUnicode(u'<ABC/>&lt;script src=&quot;x&quot;&#x2F;&gt;')

      >>> SafeHTMLUnicode(u'<ABC/>') + u'<script src="x"/>'
      SafeHTMLUnicode(u'<ABC/>&lt;script src=&quot;x&quot;&#x2F;&gt;')
      
      >>> '<script src="x"/>' + SafeHTMLUnicode(u'<ABC/>')
      SafeHTMLUnicode(u'&lt;script src=&quot;x&quot;&#x2F;&gt;<ABC/>')
      
      >>> SafeHTMLUnicode(u'<ABC/>') * 2
      SafeHTMLUnicode(u'<ABC/><ABC/>')
      
      >>> SafeHTMLUnicode(u'<ABC>%s</ABC>') % '<script src="x"/>'
      SafeHTMLUnicode(u'<ABC>&lt;script src=&quot;x&quot;&#x2F;&gt;</ABC>')
      
      >>> SafeHTMLUnicode(u'<ABC %s>%s</ABC>') % (
      ...      SafeHTMLUnicode(u'spam="foo"'), '<script src="x"/>')
      SafeHTMLUnicode(u'<ABC spam="foo">&lt;script src=&quot;x&quot;&#x2F;&gt;</ABC>')
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
