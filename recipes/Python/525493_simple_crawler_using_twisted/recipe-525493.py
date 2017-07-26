#!/usr/bin/env python

from twisted.web import client, error
import os.path
import ConfigParser 
import getpass, base64
import webbrowser

class HTTPProgressDownloader(client.HTTPDownloader):    
    def __init__(self, url, outfile, headers=None):
        client.HTTPDownloader.__init__(self, url, outfile, headers=headers)
        self.status = None

    def noPage(self, reason): # called for non-200 responses
        if self.status == '304':
            print reason.getErrorMessage()
            client.HTTPDownloader.page(self, '')
        else:
            client.HTTPDownloader.noPage(self, reason)

    def gotHeaders(self, headers):
        # page data is on the way
        if self.status == '200':
            
            # initialize for progress bar
            if headers.has_key('content-length'):
                self.totallength = int(headers['content-length'][0])
            else:
                self.totallength = 0
            self.currentlength = 0.0
            print ''

            # update headers metadata 
            oldheaders = {}
            eTag = headers.get('etag','')
            if eTag:
                oldheaders['etag'] = eTag[0]
            modified = headers.get('last-modified','')
            if modified:
                oldheaders['last-modified'] = modified[0]
                
            config = ConfigParser.ConfigParser()
            config.read('metadata.ini')
                
            if config.has_section('headers'):
                config.remove_section('headers')    
                
            config.add_section('headers')
            for key, value in oldheaders.items():
                config.set('headers', key, value)
                
            config.write(open('metadata.ini','w'))
            

        return client.HTTPDownloader.gotHeaders(self, headers)

    def pagePart(self, data):
        if self.status == '200':
            self.currentlength += len(data)
            if self.totallength:
                percent = "%i%%" % (
                    (self.currentlength/self.totallength)*100)
                
            else:
                percent = '%dK' % (self.currentLength/1000)
            print "\033[1FProgress: " + percent
        return client.HTTPDownloader.pagePart(self, data)

def downloadWithProgress(url, outputfile, contextFactory=None, *args, **kwargs):
    scheme, host, port, path = client._parse(url)
    factory = HTTPProgressDownloader(url, outputfile, *args, **kwargs)
    if scheme == 'https':
        from twisted.internet import ssl
        if contextFactory == None :
            contextFactory = ssl.ClientContextFactory()
        reactor.connectSSL(host, port, factory, contextFactory)
    else:
        reactor.connectTCP(host, port, factory)

    return factory.deferred

def downloadPage( url, outputfile, RequestHeaders):
    downloadWithProgress(url, outputfile, headers=RequestHeaders).addCallback(
        downloadComplete).addErrback(
        handleBasicAuthentication,url,outputfile, RequestHeaders).addErrback(
        handleError)
        
def downloadComplete(result):
    print "download Complete"
    reactor.stop()

def handleBasicAuthentication(failure, url, outputfile, RequestHeaders):
    failure.trap(error.Error)
    if failure.value.status == '401':
        username = raw_input("user name:")
        password = getpass.getpass("password: ")
        basicAuth = base64.encodestring("%s:%s"%(username, password))
        authHeader = "Basic "+basicAuth.strip()
        AuthHeaders = {"Authorization": authHeader}
        RequestHeaders.update(AuthHeaders)
        return downloadWithProgress(url, outputfile, headers=RequestHeaders)
    else:
        return failure

def handleError(failure):
    print "Error: ", failure.getErrorMessage()
    reactor.stop()

def getRequestHeaders(url, outputfile):
    # update metadata and generate request headers
    
    RequestHeaders = {}
    
    config = ConfigParser.ConfigParser()
    if not os.path.isfile('metadata.ini'):
        section = 'download-metadata'
        config.add_section(section)
        config.set(section, "url", url)
        config.set(section, "filename", outputfile)
        config.write(open('metadata.ini','w'))
    else:
        config.read('metadata.ini')
        eTag = None
        if config.has_option('headers','etag'):
            eTag = config.get('headers','etag')
            if eTag:
                RequestHeaders['If-None-Match'] = eTag

        modified = None
        if config.has_option('headers','last-modified'):
            modified = config.get('headers','last-modified')
            if modified:
                RequestHeaders['If-Modified-Since'] = modified

    return RequestHeaders

if __name__ == '__main__':
    import sys
    from twisted.internet import reactor
    
    url, outputfile = sys.argv[1:]

    RequestHeaders = getRequestHeaders(url, outputfile)
    downloadPage(url, outputfile, RequestHeaders)

    reactor.run()
    webbrowser.open(outputfile)
