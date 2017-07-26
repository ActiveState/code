# linenum.py

import traceback, textwrap

def LN(*args, **kwargs):
    """Prints a line number and some text.

    A variable number of positional arguments are allowed. If
        LN(obj0, obj1, obj2)
    is called, the text part of the output looks like the output from
        print obj0, obj1, obj2
    The optional keyword "wrap" causes the message to be line-wrapped. The
    argument to "wrap" should be "1" or "True". "name" is another optional
    keyword parameter. This is best explained by an example:
        from linenum import LN
        def fun1():
            print LN('error', 'is', 'here')
        def fun2():
            print LN('error',  'is', 'here', name='mess')
        fun1()
        fun2()
    The output is:
        L3 fun1: error is here
        L5 mess: error is here
    """
    stack = traceback.extract_stack()
    a, b, c, d = stack[-2]
    out = []
    for obj in args:
        out.append(str(obj))
    text = ' '.join(out)
    if 'name' in kwargs:
        text = 'L%s %s: %s' % (b, kwargs['name'], text)
    else:
        text = 'L%s %s: %s' % (b, c, text)
    if 'wrap' in kwargs and kwargs['wrap']:
        text = textwrap.fill(text)
    return text

#=====================================================
# LNtest.py

#! /usr/bin/env python

from linenum import LN

def function():
    print LN()
    print LN('print', 'me')
    print LN('abc', name='AName')
    print LN('When the name variable is of the form ' \
      'package.module, normally, the top-level package', wrap=1)

function()
