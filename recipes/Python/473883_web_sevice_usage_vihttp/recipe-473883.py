from SOAPpy import SOAPProxy
import os, sys
# python sample code for the Currency Exchange service


if len(sys.argv)<>3:
    print "usage: %s germany sweden\n\tyou may try other countries"%(sys.argv[0])
    sys.exit(-1)


# in some intranets an issue: how to use a web proxy for WS. Here
# we assume a set environment variable 'http_proxy'.·
# This is common in unix environments. SOAPpy does not like
# a leading 'http://'
if os.environ.has_key("http_proxy"):·
    my_http_proxy=os.environ["http_proxy"].replace("http://","")
else:
     my_http_proxy=None

url = 'http://services.xmethods.net:80/soap'
n   = 'urn:xmethods-CurrencyExchange'


server = SOAPProxy(url, namespace=n, http_proxy=my_http_proxy)

print sys.argv[1], sys.argv[2], server.getRate(sys.argv[1], sys.argv[2])
