from httplib import HTTP 
from urlparse import urlparse 

def checkURL(url): 
     p = urlparse(url) 
     h = HTTP(p[1]) 
     h.putrequest('HEAD', p[2]) 
     h.endheaders() 
     if h.getreply()[0] == 200: return 1 
     else: return 0 

if __name__ == '__main__': 
     assert checkURL('http://slashdot.org') 
     assert not checkURL('http://slashdot.org/notadirectory') 
