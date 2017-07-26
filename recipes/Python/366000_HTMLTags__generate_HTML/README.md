## HTMLTags - generate HTML in PythonOriginally published: 2005-02-05 03:25:04 
Last updated: 2009-10-24 10:30:38 
Author: Pierre Quentel 
 
The HTMLTags module defines a class for each valid HTML tag, written in uppercase letters. To create a piece of HTML, the general syntax is :\n\n    t = TAG(innerHTML, key1=val1,key2=val2,...)\n\nso that "print t" results in :\n\n    <TAG key1="val1" key2="val2" ...>innerHTML</TAG>\n\nFor instance :\n\n    print A('bar', href="foo") ==> <A href="foo">bar</A>