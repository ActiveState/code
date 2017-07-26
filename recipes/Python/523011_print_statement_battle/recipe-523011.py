# -*- coding: Windows-1251 -*-

_goodchars=dict()

def console(msg):
    '''
    Author: Denis Barmenkov <denis.barmenkov@gmail.com>
    Date: 02-jul-2007

    Write string to stdout.
    On UnicodeEncodeError exception all the unsafe chars from string
    replaced by its python representation
    '''
    global _goodchars
    try:
        print msg
    except UnicodeEncodeError:
        # get error, 
        res=''
        for i in list(msg):
            # try to put unknown characters thru print statement:
            if i not in _goodchars:
                try:
                    print i # try print character, some extra trash on screen
                            # for each unknown printable character 
                    _goodchars[i]=i # safe character, save it as is
                except UnicodeEncodeError:
                    # format character as python string constant
                    code=ord(i)
                    if code < 256:
                        t='\\x%02x' % code # 8-bit value
                    elif code < 65536:
                        t='\\u%04x' % code # 16-bit value unicode
                    else:
                        t='\\U%08x' % code # other values as 32-bit unicode
                    _goodchars[i]=t # or '.' for readability ;-)
            res+=_goodchars[i]  # append to result
        print res

if __name__=='__main__':
    import codecs
    import sys

    reload(sys)

    # prepare my encodings
    sys.setdefaultencoding('cp1251')                  # set default encoding for source
    sys.stdout=codecs.getwriter('cp866')(sys.stdout)  # set DOS cyrillic codepage

    test_string='\xab'

    try:
        print 'Using print statement:', test_string
    except UnicodeEncodeError:
        print 'UnicodeEncodeError exception while using print!'
        
    print 'Using console():',
    console(test_string)
