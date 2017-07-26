text=u"""Europython 2005
G\u00f6teborg, Sweden
\u8463\u5049\u696d
Hotel rates 100\N{euro sign}
"""

import codecs 

def printu(ustr):
    print ustr.encode('raw_unicode_escape')
    
def saveu(ustr, filename='output.txt'):
    file(filename,'wb').write(codecs.BOM_UTF8 + ustr.encode('utf8'))
