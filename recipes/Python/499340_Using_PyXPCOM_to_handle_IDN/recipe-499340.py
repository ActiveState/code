from xpcom import _xpcom
from xpcom import components

cls = components.classes['@mozilla.org/network/idn-service;1']
obj = cls.getService(components.interfaces.nsIIDNService)

hangul_kr = u'\ud55c\uae00.kr'
print obj.convertUTF8toACE(hangul_kr)

# xn--bj0bj06e.kr
