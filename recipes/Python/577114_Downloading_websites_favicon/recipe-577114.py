import sys
import shutil
import urllib2
import lxml.html


HEADERS = {
    'User-Agent': 'urllib2 (Python %s)' % sys.version.split()[0],
    'Connection': 'close',
}


def get_favicon(url, path='favicon.ico', alt_icon_path='alticon.ico'):

    if not url.endswith('/'):
        url += '/'

    request = urllib2.Request(url + 'favicon.ico', headers=HEADERS)
    try:
        icon = urllib2.urlopen(request).read()
    except(urllib2.HTTPError, urllib2.URLError):
        reqest = urllib2.Request(url, headers=HEADERS)
        try:
            content = urllib2.urlopen(request).read(2048) # 2048 bytes should be enought for most of websites
        except(urllib2.HTTPError, urllib2.URLError):
            shutil.copyfile(alt_icon_path, path)
            return
        icon_path = lxml.html.fromstring(x).xpath(
            '//link[@rel="icon" or @rel="shortcut icon"]/@href'
        )
        if icon_path:
            request = urllib2.Request(url + icon_path[:1], headers=HEADERS)
            try:
                icon = urllib2.urlopen(request).read()
            except(urllib2.HTTPError, urllib2.URLError):
                shutil.copyfile(alt_icon_path, path)
                return
    
    open(path, 'wb').write(icon)


if __name__ == '__main__':
    get_favicon('http://code.activestate.com', 'favicon.ico')
