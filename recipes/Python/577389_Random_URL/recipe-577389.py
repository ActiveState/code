# randomURL.py
# Finds and displays a random webpage.
# FB - 201009127
import random
import urllib2
import os

while(True):
    ip0 = str(random.randint(0, 255))
    ip1 = str(random.randint(0, 255))
    ip2 = str(random.randint(0, 255))
    ip3 = str(random.randint(0, 255))
    url = 'http://' + ip0 + '.' + ip1 + '.'+ ip2 + '.'+ ip3
    print url
    try:
        urlContent = urllib2.urlopen(url).read()
        if urlContent.find('<html') > -1 or urlContent.find('<HTML') > -1:
            break
    except:
        pass

print "Found URL: " + url
os.system('start ' + url)
