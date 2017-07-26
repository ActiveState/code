# Web testing using Twill
# FB - 201011254
import time
import sys
from twill import get_browser
from twill.commands import *

# Navigate to Google
# b = get_browser()
# b.go("http://www.google.com/")
go("http://www.google.com/")
code(200) # assert page loaded fine
# showforms()

# Make a search
searchStr = 'Python'
formvalue(1, 'q', searchStr)
submit('btnG')
time.sleep(1)
code(200) # assert page loaded fine

##links = showlinks()
##for link in links:
##    print link

# assert the search result
try:
    find('<em>Python</em> Programming Language . Official Website') # will pass
    # find('regex') # will fail
except Exception as e:
    print e
    sys.exit() # if the link is not found then must not try to continue

# click the link (using regex)
follow('Python Programming Language . Official Website')
code(200) # assert page loaded fine

# assert current URL
try:
    print url('http://www.python.org/') # will pass
    print
    url('http://www.google.com/') # will fail
except Exception as e:
    print e
