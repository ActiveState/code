"""
Author: Lloyd Moore <lloyd@workharderplayharder.com>
Usage: 
	print perm("01", 2)
	> ["00", "01", "10", "11"]

	print perm("abcd", 2)
	> [ 'aa', 'ab', 'ac', 'ad', 
		'ba', 'bb', 'bc', 'bd', 
		'ca', 'cb', 'cc', 'cd', 
		'da', 'db', 'dc', 'dd' ]


"""
def perm(chars, m, wrd="", wrds=[]):
    if len(wrd) == m: return wrd
    for i in range(0, len(chars)):
        w = perm(chars, m, wrd+chars[i])
        if type(w) == type(""): wrds.append(w)
    return wrds
