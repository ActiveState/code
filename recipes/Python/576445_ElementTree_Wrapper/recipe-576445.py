from xml.etree import cElementTree
import re

#Compatibility with 3.0
try:
  #3.x
  import io
  def is_file(ob):
    return isinstance(ob, io.IOBase)
  def is_text(ob):
    return type(ob) == str
except:
  #2.x
  def is_file(ob):
    return isinstance(ob, file)
  def is_text(ob):
    return isinstance(ob, basestring)


def attr_str(obj):
  return ' '.join('%s = "%s"' % (key,value) for key,value in obj.items())

def text(obj):
  if type(obj) in (int,float):
    return str(obj)
  elif is_text(obj):
    return obj
  return str(obj)

PREFIX_PAT = re.compile('(\{.*\})')

class xml(object):
  """
  Usage:
    xml(tag, child, ..., attr = value, ...)
      returns new element with specified child elements and attributes
    xml(tag, text, child, ..., attr = value, ...)
      returns new element with specified text, child elements, and attributes
    xml(literal)
      returns new element for literal xml string
    xml(xmlable)
      returns xmlable.__xml__()

  Example:
    from xmlwrapper import xml
    table_elt = xml('table', xml('tr',xml('td',"header",colspan = "2")),
                             xml('tr',xml('td',xml('b',"bold text")),
                                      xml('td',"plain text")))
    table_elt['border'] = "1"
    open("test.html","w").write(str(xml('html',xml('body',table_elt))))
    print table_elt.navlist('tr')

  Example of __xml__ interface:
    class xmldict(dict):
      def __xml__(self):
        xml_elt = xml('dict')
        for key in self:
          xml_elt.append(xml('dictent',xml('key',str(key)),
                                       xml('value',str(self[key]))))
        return xml_elt

    e = xmldict()
    e['foo'] = 'bar'
    print xml(e)
  """
  def __new__(cls,tag,thing = None,*args,**kwargs):
    if hasattr(tag,'__xml__'):
      return tag.__xml__()
    self = object.__new__(xml)
    if cElementTree.iselement(tag):
      self.__content = tag
    elif isinstance(tag,cElementTree.ElementTree):
      self.__content = tag.getroot()
    elif is_file(tag):
      self.__content = cElementTree.parse(tag).getroot()
    elif isinstance(tag,str) and len(tag) > 0 and tag[0] == '<':
      self.__content = cElementTree.fromstring(tag)
    else:
      if type(tag) != str:
        raise TypeError("Cannot convert %s object to xml" % str(type(tag)))
      self.__content = cElementTree.fromstring('<%s/>' % tag)
      if is_text(thing) or type(thing) == int:
        self.__content.text = text(thing)
      elif thing != None:
        self.append(xml(thing))
      for subthing in args:
        self.append(xml(subthing))
      for key,value in kwargs.items():
        if key == '__class' or key == 'klass':
          self['class'] = value
        else:
          self[key] = value
    if '{' in self.__content.tag:
      self.__prefix = PREFIX_PAT.search(self.__content.tag).groups()[0]
    else:
      self.__prefix = ''
    return self
  def clear(self):
    self.__content.clear()
  def append(self,xml_obj):
    assert type(xml_obj) == xml
    self.__content.append(xml_obj.__content)
  def setprefix(self, prefix):
    self.__prefix = prefix
  def getprefix(self):
    return self.__prefix
  def remove(self,xml_obj):
    assert type(xml_obj) == xml
    self.__content.remove(xml_obj.__content)
  def __xml__(self):
    return self
  def __str__(self):
    return cElementTree.tostring(self.__content)
  def __repr__(self):
    return str(self)
  def __getitem__(self,attr):
    qattr = self.__prefix + attr
    if qattr in self.__content.keys():
      return self.__content.get(qattr)
    raise AttributeError("<%s> element does not have attribute %s" % (self.tag, attr))
  def get(self,attr, default):
    return self.__content.get(self.__prefix + attr, default)
  def __setitem__(self,attr,value):
    assert type(attr) == str and type(value) == str
    self.__content.set(attr,value)
  def getxml(self):
    return self.__content
  def __get_text(self):
    if self.__content.text:
      return self.__content.text
    return ''
  def __set_text(self, value):
    if not is_text(value):
      raise ValueError("xmlwrapper: cannot set text of element to object of type %s" % str(type(value)))
    self.__content.text = value
  text = property(__get_text,__set_text)
  def __get_tag(self):
    return self.__strip_key(self.__content.tag)
  def __set_tag(self,tag_value):
    assert type(tag_value) == str
    self.__content.tag = self.__prefix + tag_value
  tag = property(__get_tag,__set_tag)
  def pretty_list(self):
    str_list = []
    for child_elt in self.__content.getchildren():
      for pretty_str in xml(child_elt).pretty_list():
        str_list.append(pretty_str)
    str_list = ["  " + pretty_str for pretty_str in str_list]
    head_str = ' '.join(str_item for str_item in [self.tag, attr_str(self.__content.attrib)] if str_item.strip())
    if str_list:
      str_list = ["<%s>" % head_str, self.text] + str_list + ["</%s>" % self.tag]
    elif self.text:
      str_list = ["<%s>%s</%s>" % (head_str, self.text, self.tag)]
    else:
      str_list = ["<%s/>" % head_str]
    return str_list
  def pretty(self):
    return '\n'.join(pretty_str for pretty_str in self.pretty_list() if pretty_str.strip())
  def __strip_key(self,key):
    return key[len(self.__prefix):]
  def keys(self):
    return [self.__strip_key(key) for key in self.__content.keys()]
  def attrs(self):
    return self.keys()
  def items(self):
    return [(self.__strip_key(k),v) for k,v in self.__content.items()]
  def iterattrs(self):
    return self.__content.attrib.iterkeys()
  def iterelts(self):
    return iter(xml(child_elt) for child_elt in self.__content.getchildren())
  def __iter__(self):
    return self.iterelts()
  def __len__(self):
    return len(self.__content.getchildren())
  def __path_from_list(self,tag_list):
    return './/' + '//'.join(self.__prefix + tag for tag in tag_list)
  def nav(self,*tag_list):
    path = self.__path_from_list(tag_list)
    return self.find(path)
  def navlist(self,*tag_list):
    return self.findall(self.__path_from_list(tag_list))
  def find(self,path):
    elt = self.__content.find(path)
    return xml(elt) if elt != None else None
  def findall(self,path):
    return [xml(elt) for elt in self.__content.findall(path)]
  def join(self,iterable):
    """
    Usage:
      elt.join(iterable)
        returns list of elements from iterable separated by elt

    Example:
      xml('html', xml('body', *xml('br').join(xml('span',text) for text in ['foo','bar','baz'])))
    """
    join_list = []
    for elt in iterable:
      assert type(elt) == xml
      join_list.append(elt)
      join_list.append(self)
    if len(join_list) > 0:
      join_list.pop()
    return join_list
  def extend(self,iterable):
    for elt in iterable:
      assert type(elt) == xml
      self.append(elt)

def test1():
  class xmldict(dict):
    def __xml__(self):
      xml_elt = xml('dict')
      for key in self:
        xml_elt.append(xml('dictent',xml('key',str(key)),
                                     xml('value',str(self[key]))))
      return xml_elt

  e = xmldict()
  e['foo'] = 'bar'
  assert repr(xml(e)) == "<dict><dictent><key>foo</key><value>bar</value></dictent></dict>"

def test2():
  xml_test_data = [[xml('html', xml('body', *xml('br').join(xml('span',text) for text in ['foo','bar','baz']))),
                   "<html><body><span>foo</span><br /><span>bar</span><br /><span>baz</span></body></html>"],
                   [xml("<br/>"),"<br />"],
                  ]
  for v1,v2 in xml_test_data:
    assert repr(v1) == v2

def runtests():
  test1()
  test2()
  print("xmlwrapper: tests OK")

if __name__ == '__main__':
  runtests()
