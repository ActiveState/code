import sys,os,urllib

__doc__ = \
"""
pls2wmp.py - Play a PLS playlist file in Windows Media Player
USAGE:
pls2wmp.py <URL or filename>
EXAMPLE:
pls2wmp.py http://shoutcast.com/sbin/shoutcast-playlist.pls?rn=4869&file=filename.pls
pls2wmp.py filename.py

To hook up to IE:
Tools->Folder Options->File Types
New, PLS, point to a batch file that says this:
c:\python25\python.exe c:\scripts\pls2wmp.py %*
"""

def entryGen(f):
    entry = {}
    for l in f:
        if l.lower().startswith('file'):
            entry['ref'] = '<REF HREF="' + (l.split('=')[-1]).strip().lower() + '"/>'
        elif l.lower().startswith('title'):
            entry['title']='<TITLE>' + (l.split('='))[-1].strip() + '</TITLE>'
        if len(entry) == 2:
            yield '\n'.join(['<ENTRY>',
                             entry['ref'],
                             entry['title'],
                             '</ENTRY>'])
            entry = {}

def createASX(url):
    """ 
    Translates the supplied file or url PLS file to 
    an ASX file for WMP. Returns the filename 
    """
    asxf = open(os.path.join(os.environ['TEMP'],'pls2asx.asx'),mode='w')
    asxf.write("<ASX VERSION=\"3.0\">\n")
    asxf.write("<TITLE>wiki.cdyne.com PLS Winamp to Windows Media</TITLE>\n")
    try:
        f = open(url)
    except:
        f = urllib.urlopen(url)
    for entry in entryGen(f):
        asxf.write(entry+'\n')
    asxf.write('</ASX>')
    asxf.close()
    return asxf.name

def main():
    if len(sys.argv) < 2 or sys.arv[1] in ('-h','--help'):
        print __doc__
    else:
        url = sys.argv[1]
        asx = createASX(url)
        os.startfile(asx)
    
if __name__ == '__main__':
    main()
