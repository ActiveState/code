#!/usr/bin/env python
#
# word_wrap.py
#
# Copyright (c) 2001 Alan Eldridge. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the "Artistic License" which is
# distributed with the software in the file LICENSE.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Artistic
# License for more details.
#
# Thank you.
#
# Alan Eldridge 2001-09-16 alane@wwweasel.geeksrus.net
#
# $Id: word_wrap.py,v 1.4 2001/10/14 05:04:37 alane Exp $
#
# 2001-09-16 alane@wwweasel.geeksrus.net
#

import string

def wrap_str(str, max):
    ll = []
    lines = string.split(str, '\n')
    if len(lines) > 1:
        return wrap_list(lines, max)
    words = string.split(lines[0])
    for i in range(len(words)):
        if len(words[i]) == 0:
            del words[i]
    while len(words):
        cc = 0
        cw = 0
        for w in words:
            tmp = (cc > 0) + cc + len(w)
            if tmp > max:
                break
            cc = tmp
            cw = cw + 1
        if cw == 0:
            # must break word in middle
            ll.append(words[cw][:max-1] + '+')
            words[cw] = words[cw][max-1:]
        else:
            ll.append(string.join(words[:cw]))
            words = words[cw:]
    return ll

def wrap_list(lines, max):
    ll = []
    for l in lines:
        if len(ll):
            ll.append('')
        ll = ll + wrap_str(l, max)
    return ll

#
#EOF
##
