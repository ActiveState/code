def _textlist(self, _addtail=False):
    '''Returns a list of text strings contained within an element and its sub-elements.

    Helpful for extracting text from prose-oriented XML (such as XHTML or DocBook).
    '''
    result = []
    if self.text is not None:
        result.append(self.text)
    for elem in self:
        result.extend(elem.textlist(True))
    if _addtail and self.tail is not None:
        result.append(self.tail)
    return result


# inject the new method into the ElementTree framework
from xml.etree.ElementTree import _Element
_Element.textlist = _textlist


## ---------- Sample calls -----------

from xml.etree.ElementTree import XML
from textwrap import fill

xhmtl_fragment = XML('''
<ul>
<li>XHTML documents start with an <span class="code">&lt;html&gt;</span> tag - there is no such thing as an <span class="code">&lt;xhtml&gt;</span> tag.</li>
<li>It is required that you declare the XHTML namespace inside the opening <span class="code">&lt;html&gt;</span> tag.</li>
<li>This XHTML example covered the use of XHTML transitional - for XHTML strict or frameset, use the appropriate
<a title="Declaring a DocType" href="/xhtml/doctype/" >DOCTYPE Declaration</a>.</li>
<li>Remember that declaring a DOCTYPE with a valid identifier at the top of an XHTML page puts most browers
in <i>standards</i> mode- so remember not to use old browser hacks, and non-standard tags. (Otherwise, use just use regular HTML)</li>
<li>For some browsers, including Microsoft Internet Explorer 6, if you start an XHTML page with the XML declaration,
the browser goes into <i>quirks</i> mode, an unfortunate bug. The workaround is to delete the optional 
declaration and declare the the encoding using a meta tag.</li>
<li>The DOCTYPE declaration has to be in all uppercase characters, just like in the XHTML example code.</li>
</ul>
''')

print fill(''.join(xhmtl_fragment.textlist()))


docbook_fragment = XML('''
<book id="ashortbook">
  <title>History of Computer Programming</title>
  <chapter id="afirstchapter">
    <title>Chapter 1 -- Evolution</title>
    <para>In the beginning, there was machine language.   Then, arose assember.</para>
    <para>From those humble beginnings, a thousand languages were born.</para>
  </chapter>
  <chapter id="asecondchapter">
    <title>Chapter 2 -- Consolidation </title>
    <para>Eventually, all designs converged on variants on LISP.</para>
  </chapter>
</book>
''')

print '\n'.join(map(fill, docbook_fragment.textlist()))


## ---------- Sample output -----------

'''
 XHTML documents start with an <html> tag - there is no such thing as
an <xhtml> tag. It is required that you declare the XHTML namespace
inside the opening <html> tag. This XHTML example covered the use of
XHTML transitional - for XHTML strict or frameset, use the appropriate
DOCTYPE Declaration. Remember that declaring a DOCTYPE with a valid
identifier at the top of an XHTML page puts most browers in standards
mode- so remember not to use old browser hacks, and non-standard tags.
(Otherwise, use just use regular HTML) For some browsers, including
Microsoft Internet Explorer 6, if you start an XHTML page with the XML
declaration, the browser goes into quirks mode, an unfortunate bug.
The workaround is to delete the optional  declaration and declare the
the encoding using a meta tag. The DOCTYPE declaration has to be in
all uppercase characters, just like in the XHTML example code.

History of Computer Programming


Chapter 1 -- Evolution

In the beginning, there was machine language.   Then, arose assember.

From those humble beginnings, a thousand languages were born.


Chapter 2 -- Consolidation

Eventually, all designs converged on variants on LISP.
'''
