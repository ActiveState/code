import os
import sys
import urllib

def _reporthook(numblocks, blocksize, filesize, url=None):
    #print "reporthook(%s, %s, %s)" % (numblocks, blocksize, filesize)
    base = os.path.basename(url)
    #XXX Should handle possible filesize=-1.
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b"*70)
    sys.stdout.write("%-66s%3d%%" % (base, percent))

def geturl(url, dst):
    print "get url '%s' to '%s'" % (url, dst)
    if sys.stdout.isatty():
        urllib.urlretrieve(url, dst,
                           lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url))
        sys.stdout.write('\n')
    else:
        urllib.urlretrieve(url, dst)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        url = sys.argv[1]
        base = url[url.rindex('/')+1:]
        geturl(url, base)
    elif len(sys.argv) == 3:
        url, base = sys.argv[1:]
        geturl(url, base)
    else:
        print "Usage: geturl.py URL [DEST]"
        sys.exit(1)
