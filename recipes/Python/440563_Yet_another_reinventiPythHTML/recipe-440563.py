import sys
import cStringIO

#handle character escaping...
import re
from htmlentitydefs import codepoint2name

character2name = {}
for i,j in codepoint2name.iteritems():
    if i <= 127:
        character2name[chr(i)] = '&%s;'%j
    else:
        character2name[unichr(i)] = '&#%d;'%i
del i;del j;del codepoint2name
escape = re.compile('(%s)'%('|'.join(list(character2name))))

def repl(matchobj):
    return character2name.get(matchobj.group(0), '?')

#handle special tags
no_ends = dict.fromkeys(('br p input img area base basefont col '
                         'frame hr isindex link meta param iframe').split())
no_escape = dict.fromkeys('script raw'.split())
raw = dict.fromkeys('pre'.split())

#the base tag generator

class T(object):
    def __getattr__(self, tagname):
        return tag(tagname)

T = T()

class tag(object):
    __slots__ = ['name', 'attrs', 'contents']
    def __init__(self, name, attrs=None, contents=None):
        self.name = name.lower()
        self.attrs = attrs
        self.contents = contents
    def __call__(self, *args, **kwargs):
        if kwargs and self.attrs:
            d = dict(self.attrs)
            d.update(kwargs)
            kwargs = d
        __klass = kwargs.pop('klass', None)
        if __klass:
            kwargs['class'] = __klass
        if args and kwargs:
            return tag(self.name, kwargs, args)
        elif kwargs:
            return tag(self.name, kwargs, self.contents)
        elif args:
            return tag(self.name, self.attrs, args)
        return self
    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            if self.attrs is None:
                self.attrs = {}
            self.attrs[key] = value
        else:
            raise TypeError('attribute assignments must only be to named attributes')
    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            if not self.contents:
                raise IndexError('tuple index out of range')
            return self.contents[key]
        raise TypeError('content fetch must only be from indexed attributes')
    def render(self, where=None, called=0):
        if where is None:
            x = cStringIO.StringIO()
            self.render(x)
            x.seek(0)
            return x.read()
        if self.name != 'raw':
            if self.attrs:
                x = []
                for key, value in self.attrs.iteritems():
                    x.append("%s='%s'"%(key, value))
                where.write('\n' + called*'  ' + '<%s %s>'%(self.name, ' '.join(x).encode('utf-8')))
            else:
                where.write('\n' + called*'  ' + '<%s>'%self.name)
        x = where.tell()
        if self.contents:
            c2n = character2name
            for i in self.contents:
                if hasattr(i, 'render'):
                    i.render(where, called+1)
                elif self.name in no_escape:
                    where.write(str(i).encode('utf-8'))
                else:
                    st = str(i)
                    chrs = dict.fromkeys(st)
                    for i in chrs:
                        if i in c2n:
                            break
                    else:
                        chrs = None
                    if chrs:
                        #we found something that needs to be translated
                        st = escape.sub(repl, st)
                    where.write(st.encode('utf-8'))
        if self.name != 'raw' and self.name not in no_ends:
            if self.name not in raw and where.tell()-x > 25:
                where.write('\n' + called*'  ' +'</%s>'%self.name)
            else:
                where.write('</%s>'%self.name)
        if not called:
            where.write('\n')
            
'''
>>> print T.html(
...     T.body(
...         "hello world", T.br, "how are you?", T.br,
...         T.table(*[T.tr(*map(T.td, map(str, range(0+i, 3+i)))) for i in xrang
e(3)])
...                 )).render()

<html>
  <body>hello world
    <br>how are you?
    <br>
    <table>
      <tr>
        <td>0</td>
        <td>1</td>
        <td>2</td>
      </tr>
      <tr>
        <td>1</td>
        <td>2</td>
        <td>3</td>
      </tr>
      <tr>
        <td>2</td>
        <td>3</td>
        <td>4</td>
      </tr>
    </table>
  </body>
</html>

>>>
>>> x = T.html(
...     T.body(bgcolor='red')(
...         T.font(size='+1')('Welcome to this wonderful web page!'),
...         T.br, "How are you doing today?",
...         T.br, T.input(type='text', size='25', value='say something')
...         )).render()
>>> print x

<html>
  <body bgcolor='red'>
    <font size='+1'>Welcome to this wonderful web page!
    </font>
    <br>How are you doing today?
    <br>
    <input type='text' value='say something' size='25'>
  </body>
</html>

>>>
>>> print T.html(
...     T.body(
...         T.pre(x))).render()

<html>
  <body>
    <pre>
&lt;html&gt;
  &lt;body bgcolor='red'&gt;
    &lt;font size='+1'&gt;Welcome to this wonderful web page!
    &lt;/font&gt;
    &lt;br&gt;How are you doing today?
    &lt;br&gt;
    &lt;input type='text' value='say something' size='25'&gt;
  &lt;/body&gt;
&lt;/html&gt;
</pre>
  </body>
</html>

>>>
>>> def generate_something():
...     return T.b("I was generated from a function")
...
>>> print T.html(T.body(generate_something())).render()

<html>
  <body>
    <b>I was generated from a function
    </b>
  </body>
</html>

>>>
'''
