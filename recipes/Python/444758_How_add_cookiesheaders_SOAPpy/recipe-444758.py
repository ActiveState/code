#
# Author : t3rmin4t0r
# Mail   : gopalv82 -AT- yahoo.com
# Site   : http://t3.dotgnu.info/
# 

import sys, os, string
from SOAPpy import WSDL,HTTPTransport,Config,SOAPAddress
import ClientCookie
import urllib2

Config.cookieJar = ClientCookie.MozillaCookieJar()
# Uncomment the following line if you have cookies.txt
# Config.cookieJar.load("cookies.txt")

class CookieTransport(HTTPTransport):
  def call(self, addr, data, namespace, soapaction = None, encoding = None,
    http_proxy = None, config = Config):

    if not isinstance(addr, SOAPAddress):
      addr = SOAPAddress(addr, config)
    
    cookie_cutter = ClientCookie.HTTPCookieProcessor(config.cookieJar)
    hh = ClientCookie.HTTPHandler()
    hh.set_http_debuglevel(1)

    # TODO proxy support
    opener = ClientCookie.build_opener(cookie_cutter, hh)

    t = 'text/xml';
    if encoding != None:
      t += '; charset="%s"' % encoding
    opener.addheaders = [("Content-Type", t),
              ("Cookie", "Username=foobar"), # ClientCookie should handle
              ("SOAPAction" , "%s" % (soapaction))]
              
    response = opener.open(addr.proto + "://" + addr.host + addr.path, data)
    data = response.read()

    # get the new namespace
    if namespace is None:
      new_ns = None
    else:
      new_ns = self.getNS(namespace, data)

    print '\n' * 4 , '-'*50
    # return response payload
    return data, new_ns

# From xmethods.net

wsdlURL = "http://www.doughughes.net/WebServices/fortune/fortune.cfc?wsdl"

proxy = WSDL.Proxy(wsdlURL, transport = CookieTransport)

print proxy.getFortune()
