# -*- coding:iso8859-1 -*-
import locale

# using your default locale (user settings)
locale.setlocale(locale.LC_ALL,"")
#locale.setlocale(locale.LC_ALL,"fi") or something else

stuff="aåbäcÖöAÄÅBCabcÅÄÖabcÅÄÖ"

# using sorted-function
print "Wrong order:"
print "".join(sorted(stuff))  # not using locale

print "Right order:"
print "".join(sorted(stuff,cmp=locale.strcoll)) # using locale


# in place sorting
stufflist=list(stuff)

print "Wrong order:"
stufflist.sort()  # not using locale
print "".join(stufflist)  

print "Right order:"
stufflist.sort(cmp=locale.strcoll) # using locale
print "".join(stufflist) 
