#!/usr/local/bin/python2.7
# encoding: utf-8

import locale

alllocale = locale.locale_alias
for k in alllocale.keys():
    print 'locale[%s] %s' % (k, alllocale[k])    
