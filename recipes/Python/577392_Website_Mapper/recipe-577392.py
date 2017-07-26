# WebsiteMapper.py
# Prints a tree graph of any website.
# FB - 201009223
import urllib2
from os.path import basename
import urlparse
from BeautifulSoup import BeautifulSoup # for HTML parsing

global urlList
urlList = []

def printWebsiteMap(url, level = 0):

    # do not go to other websites
    global website
    parsedUrl = urlparse.urlsplit(url)
    scheme = parsedUrl.scheme
    netloc = parsedUrl.netloc
    netlocSplit = netloc.split('.')
    if netlocSplit[-2] + netlocSplit[-1] != website:
        return

    global urlList
    if url in urlList: # prevent using the same URL again
        return

    try:
        urlContent = urllib2.urlopen(url).read()
        soup = BeautifulSoup(''.join(urlContent))
        urlList.append(url)
    except:
        return

    if level == 0:
        print url
    else:
        print '  ' * (level - 1) + '|'
        print '  ' * (level - 1) + '|' +'__' * level + url

    global maxLevel
    if level < maxLevel:        
        # if there are links on the webpage then recursively repeat
        linkTags = soup.findAll('a')

        for linkTag in linkTags:
            try:
                linkUrl = linkTag['href']
                urlOk = True
                
                # skip if URL is a section on the same webpage
                if linkUrl.startswith('#'):
                    urlOk = False

                # skip if URL is an email
                # if linkUrl.lower().startswith('mailto:'):
                if linkUrl.find('@') > -1:
                    urlOk = False

                # skip if not an HTML URL 
                parsedUrl = urlparse.urlsplit(linkUrl)
                if parsedUrl.path.find('.') > -1: # is there a file name?
                    pathLower  = parsedUrl.path.lower()
                    if not (pathLower.endswith('.html') or pathLower.endswith('.htm')):
                        urlOk = False

                if urlOk:
                    # if relative URL then convert to absolute
                    if parsedUrl.scheme == '':
                        linkUrl = scheme + '://' + netloc + '/' + linkUrl

                    # remove '/' in the end if exists
                    if linkUrl.endswith('/'):
                        linkUrl = linkUrl.strip('/')

                    printWebsiteMap(linkUrl, level + 1)
            except:
                pass

# MAIN
rootUrl = 'http://www.bloodshed.net'
netloc = urlparse.urlsplit(rootUrl).netloc.split('.')
global website
website = netloc[-2] + netloc[-1]
global maxLevel
maxLevel = 9
printWebsiteMap(rootUrl)
