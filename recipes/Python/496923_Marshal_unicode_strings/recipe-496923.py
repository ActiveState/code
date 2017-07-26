----- unicodemarshal.py -----
from xml.marshal import generic

class UnicodeMarshaller(generic.Marshaller):
    tag_unicode = 'unicode'

    def m_unicode(self, value, dict):
        name = self.tag_unicode
        L = ['<' + name + '>']
        s = value.encode('utf-8')
        if '&' in s or '>' in s or '<' in s:
            s = s.replace('&', '&amp;')
            s = s.replace('<', '&lt;')
            s = s.replace('>', '&gt;')
        L.append(s)
        L.append('</' + name + '>')
        return L


class UnicodeUnmarshaller(generic.Unmarshaller):
    def __init__(self):
        self.unmarshal_meth['unicode'] = ('um_start_unicode','um_end_unicode')
        # super maps the method names to methods
        generic.Unmarshaller.__init__(self)

    um_start_unicode = generic.Unmarshaller.um_start_generic

    def um_end_unicode(self, name):
        ds = self.data_stack
        # the value is a utf-8 encoded unicode
        ds[-1] = ''.join(ds[-1])
        self.accumulating_chars = 0



---- example ----
>>> import sys,codecs
>>> from unicodemarshal import UnicodeMarshaller, UnicodeUnmarshaller
>>>
>>> if hasattr(sys, 'setdefaultencoding'):
...     sys.setdefaultencoding('utf-8')
...
>>>
>>> def openUTF8File(path, mode):
...     fp = codecs.open(filename=path, mode=mode, encoding='utf-8')
...     return fp
...
>>>
>>> myList = ['text',
...             u'german umlaut: \xfc \xf6 <>&']
>>>
>>> fp = openUTF8File("test.xml", mode='w')
>>> UnicodeMarshaller().dump(myList, fp)
>>> fp.close()
>>>
>>> fp = openUTF8File("test.xml", mode='r')
>>> myList = UnicodeUnmarshaller().load(fp)
>>> for s in myList:
...     print type(s)
...
>>> fp.close()
<type 'str'>
<type 'unicode'>
