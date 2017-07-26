# -*- coding: ISO-8859-1 -*-
import re
import string

_char_simple = "abcdefghijklmnopqrstuvwxyzaaaaaceeeeiiiioooooooouuuuyþ"
_char_lower  = "abcdefghijklmnopqrstuvwxyzâãäåæçèéêëìíîïðñòóôõöøùúûüýþ"
_char_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZÂÃÄÅÆÇÈÉÊ�<ÌÍÎÏÐÑÒÓÔÕÖØÙÚ�>ÜÝÞ"
_char_else = "0123456789ß×ÿ_"
_char_all = _char_lower + _char_upper + _char_else

_char_trans_lower = string.maketrans(_char_upper, _char_lower)
_char_trans_upper = string.maketrans(_char_lower, _char_upper)
_char_trans_simple = string.maketrans(_char_lower, _char_simple)

rx_ischar = re.compile("[^"+_char_all+"]*", re.DOTALL|re.MULTILINE)

def collapse(v):
    return " ".join(str(v).split()).strip()

def ilower(v):
    global _char_trans_lower
    return v.translate(_char_trans_lower)

def iupper(v):
    global _char_trans_upper
    return v.translate(_char_trans_upper)

def inormalize(v):
    global _char_trans_upper 
    v = v.translate(_char_trans_lower)
    return v.translate(_char_trans_simple)

def iwordlist(v, lower=0, minlen=0, simple=0):
    global _char_trans_lower, rx_ischar
    if lower or simple:
        v = v.translate(_char_trans_lower)
    if simple:
        v = v.translate(_char_trans_simple)
    wlist = rx_ischar.split(v)
    wlist.remove('')
    if minlen:
        wlist = filter(lambda x: len(x)>=minlen, wlist)
    return wlist

if __name__=="__main__":
    text = "Däs Äst\t êine 1  2 xx yy zzz xx TÜÖST "
    print text.lower()
    print ilower(text)
    print iupper(text)
    print inormalize(text)
    print collapse(text)
    print iwordlist(text)
    print iwordlist(text, 1)
    print iwordlist(text, 1, 2)
    print iwordlist(text, 1, 3)
    print iwordlist(text, simple=1)
