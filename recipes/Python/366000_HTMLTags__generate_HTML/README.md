## HTMLTags - generate HTML in Python  
Originally published: 2005-02-05 03:25:04  
Last updated: 2009-10-24 10:30:38  
Author: Pierre Quentel  
  
The HTMLTags module defines a class for each valid HTML tag, written in uppercase letters. To create a piece of HTML, the general syntax is :

    t = TAG(innerHTML, key1=val1,key2=val2,...)

so that "print t" results in :

    <TAG key1="val1" key2="val2" ...>innerHTML</TAG>

For instance :

    print A('bar', href="foo") ==> <A href="foo">bar</A>