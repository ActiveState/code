import urllib, os

class myURLOpener(urllib.FancyURLopener):
    """Create sub-class in order to overide error 206.  This error means a
       partial file is being sent,
       which is ok in this case.  Do nothing with this error.
    """
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass

loop = 1
dlFile = "2.6Distrib.zip"
existSize = 0
myUrlclass = myURLOpener()
if os.path.exists(dlFile):
    outputFile = open(dlFile,"ab")
    existSize = os.path.getsize(dlFile)
    #If the file exists, then only download the remainder
    myUrlclass.addheader("Range","bytes=%s-" % (existSize))
else:
    outputFile = open(dlFile,"wb")

webPage = myUrlclass.open("http://localhost/%s" % dlFile)

#If the file exists, but we already have the whole thing, don't download again
if int(webPage.headers['Content-Length']) == existSize:
    loop = 0
    print "File already downloaded"

numBytes = 0
while loop:
    data = webPage.read(8192)
    if not data:
        break
    outputFile.write(data)
    numBytes = numBytes + len(data)

webPage.close()
outputFile.close()

for k,v in webPage.headers.items():
    print k, "=",v
print "copied", numBytes, "bytes from", webPage.url
