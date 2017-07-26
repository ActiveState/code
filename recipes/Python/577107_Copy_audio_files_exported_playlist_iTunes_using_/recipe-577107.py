import sys
import os
import plistlib
import urlparse
import urllib

verbose = True
fn = sys.argv[1]
dest = sys.argv[2]
d = plistlib.readPlist(fn)
tracks = d['Tracks']
for tkey in d['Tracks'].keys():
    aupath = urlparse.urlparse(urllib.unquote(tracks[tkey]['Location'])).path
    if verbose:
        print(aupath)
    # copy audio file
    src = file(aupath, 'rb')
    destf = file(os.path.join(dest, os.path.basename(aupath)), 'wb')
    audio = src.read()
    src.close()
    destf.write(audio)
    destf.close()
