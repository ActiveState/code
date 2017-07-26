# websiteTxtSearcher.py
# Searches a website recursively for any given string.
# FB - 201009105
import urllib2
from os.path import basename
import urlparse
from BeautifulSoup import BeautifulSoup # for HTML parsing

global urlList
urlList = []

# recursively search starting from the root URL
def searchUrl(url, level, searchText): # the root URL is level 0
    # do not go to other websites
    global website
    netloc = urlparse.urlsplit(url).netloc.split('.')
    if netloc[-2] + netloc[-1] != website:
        return

    global urlList
    if url in urlList: # prevent using the same URL again
        return

    try:
        urlContent = urllib2.urlopen(url).read()
        urlList.append(url)
    except:
        return

    soup = BeautifulSoup(''.join(urlContent))
    # remove script tags
    c=soup.findAll('script')
    for i in c:
        i.extract() 
    # get text content of the URL
    try:
        body_texts = soup.body(text=True)
    except:
        return
    text = ''.join(body_texts) 

    # search
    if text.find(searchText) > -1:
        print url
        print

    # if there are links on the webpage then recursively repeat
    if level > 0:
        linkTags = soup.findAll('a')
        if len(linkTags) > 0:
            for linkTag in linkTags:
                try:
                    linkUrl = linkTag['href']
                    searchUrl(linkUrl, level - 1, searchText)
                except:
                    pass

# main
rootUrl = 'http://www.yahoo.com'
netloc = urlparse.urlsplit(rootUrl).netloc.split('.')
global website
website = netloc[-2] + netloc[-1]
searchUrl(rootUrl, 1, " computer ")
