from urllib import urlencode
from urllib2 import urlopen

def shorten_url(long_url):
     username = 'aamir******' # use your Username/password 
     password = '******'
     bitly_url = "http://api.bit.ly/v3/shorten?login={0}&apiKey={1}&longUrl={2}&format=txt"
     req_url = urlencode(bitly_url.format(username, password, long_url))
     short_url = urlopen(req_url).read()
     return short_url

"""
Then call the function and it will return the shortened URL of the URL you pass in as an parameter.. 
"""
print shorten_url('http://google.com/amirhussain')
