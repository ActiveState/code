from __future__ import unicode_literals

import email, email.header, email.utils

def decode_header(value):
    l = email.header.decode_header(value)
    l2 = []
    for value, charset in l:
        if charset:
            value = value.decode(charset)
        l2.append(value)
    return ' '.join(l2)
    
def get_header(msg, header):
    h = header.lower()
    if msg.has_key(h): 
        return decode_header(msg[h])
    return None
    
def parseaddr(msg, name):
    'name = (from|to)'
    value = msg[name]
    name, addr = email.utils.parseaddr(value)
    return decode_header(name), addr
    
def formataddr(name, addr):
    encoding = 'utf-8'
    pair = (name.encode(encoding), encoding)
    h = str(email.header.make_header((pair,)))
    return email.utils.formataddr((h, addr))
