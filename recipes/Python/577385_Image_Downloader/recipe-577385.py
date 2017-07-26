# ImageDownloader.py
# Finds and downloads all images from any given URL recursively.
# FB - 20140223
import sys
import os
import urllib2
from os.path import basename
import urlparse
from BeautifulSoup import BeautifulSoup # for HTML parsing

urlList = []

# recursively download images starting from the root URL
def downloadImages(url, level): # the root URL is level 0
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
        print url
    except:
        return

    soup = BeautifulSoup(''.join(urlContent))
    # find and download all images
    imgTags = soup.findAll('img')
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        imgUrl = url[ : url.find(".com") + 4] + imgUrl if (imgUrl[ : 4] != "http") else imgUrl
        # download only the proper image files
        if imgUrl.lower().endswith('.jpeg') or \
            imgUrl.lower().endswith('.jpg') or \
            imgUrl.lower().endswith('.gif') or \
            imgUrl.lower().endswith('.png') or \
            imgUrl.lower().endswith('.bmp'):
            try:
                imgData = urllib2.urlopen(imgUrl).read()
                global minImageFileSize
                if len(imgData) >= minImageFileSize:
                    print "    " + imgUrl
                    fileName = basename(urlparse.urlsplit(imgUrl)[2])
                    output = open(os.path.join(downloadLocationPath, fileName),'wb')
                    output.write(imgData)
                    output.close()
            except Exception, e:
                print str(e)
                # pass
    print
    print

    # if there are links on the webpage then recursively repeat
    if level > 0:
        linkTags = soup.findAll('a')
        if len(linkTags) > 0:
            for linkTag in linkTags:
                try:
                    linkUrl = linkTag['href']
                    downloadImages(linkUrl, level - 1)
                except Exception, e:
                    print str(e)
                    # pass

# MAIN
cla = sys.argv # command line arguments
if len(cla) != 5:
    print "USAGE:"
    print "[python] ImageDownloader.py URL MaxRecursionDepth DownloadLocationPath MinImageFileSize"
    os._exit(1)

rootUrl = cla[1]
maxRecursionDepth = int(cla[2])
downloadLocationPath = cla[3] # absolute path
if not os.path.isdir(downloadLocationPath):
    print downloadLocationPath + " is not an existing directory!"
    os._exit(2)

minImageFileSize = long(cla[4]) # in bytes
netloc = urlparse.urlsplit(rootUrl).netloc.split('.')
website = netloc[-2] + netloc[-1]
downloadImages(rootUrl, maxRecursionDepth)
