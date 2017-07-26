import urllib2, re
from os import path

# global re
imre = None
gifre = None

def download(url,fname):
    try:
        print "Downloading "+url+" ... ",
        furl = urllib2.urlopen(url)
        f = file(fname,'wb')
        f.write(furl.read())
        f.close()
        print "OK"
        return 1
    except:
        print "Failed"
        return 0

def gifsub(matchobj):
    return gifre.findall(matchobj.group(0))[0]

# Main procedure
def grab(wurl, outdir, wfile, wgif, lgif, cachedir = 'cache',
         tmpfile = 'tmp.htm'):
    global imre, gifre
    imre = re.compile(wgif)
    gifre = re.compile(lgif)
    # path to temporary file
    tmpf = path.join(cachedir,tmpfile)
    print "Retrieving page..."
    download(wurl, tmpf)
    f = file(tmpf,'r')
    s = f.read()
    f.close()
    all = imre.findall(s)
    res = []
    res2 = []
    # Fill up result list
    for i in all:
        if i not in res:
            res.append(i)
            res2.append(gifre.findall(i)[0])
    result = zip(res, res2)

    # Replace web links with local links
    ns = re.sub(wgif,
                gifsub, s)
    f = file(path.join(outdir,wfile),'wb')
    f.write(ns)
    f.close()

    # Download images
    for i in result:
        if not path.exists(path.join(outdir,i[1])):
            download(i[0], path.join(outdir,i[1]))

    print "Done."

if __name__ == '__main__':
    # Document URL
    wurl = 'http://www.somesiteaddress.net/page.html'
    # Path to the local directory to save the document
    outdir = '~/downloads/somesite'
    # Filename for saved page in the local directory 
    wfile = 'index.html'
    # Patterns for images:
    # - process all gif images from <http://img.anothersiteaddress.net/images>
    #   i.e. <http://img.anothersiteaddress.net/images/image.gif>
    wgif = 'http://img\.anothersiteaddress\.net/images/[^+]*?\.gif'
    # - replace the original image URL with the simple filename
    #   i.e. <http://img.anothersiteaddress.net/images/image.gif>
    #   will be <image.gif>
    lgif = '[_a-zA-Z0-9]+\.gif'

    # Directory for storing temporary files
    cachedir = '~/downloads/temp'
    # Temporary filename
    tmpfile = 'temp.htm'

    # Call the main procedure
    grab(wurl, outdir, wfile, wgif, lgif, cachedir, tmpfile)
