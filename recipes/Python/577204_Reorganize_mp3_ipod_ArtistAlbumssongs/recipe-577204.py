# Limitation: Work only with .mp3, 
# Dependancies: read Tags with eyeD3

import os, sys
import eyeD3
from os.path import join, splitext, basename, exists
from collections import defaultdict
from pdb import set_trace
from shutil import copy2

artists = defaultdict( set )
albums  = defaultdict( list )

input  = '/path/to/input/folder'
output = '/path/to/output/folder'

for dn, _, files in os.walk(input):
    for f in files:
        fn = join(dn, f)

        _, ext = splitext(fn)
        if ext == '.mp3':
            try:
                audioFile = eyeD3.Mp3AudioFile(fn)
                tag = audioFile.getTag()
                
                artist = tag.getArtist()
                album = tag.getAlbum()
                title = tag.getTitle()
                track = tag.getTrackNum()

                full_title = title
                if track != (None, None):
                    # a regular printf format could take care of the ugly zfill / int cast
                    # but I could not remember the syntax ...
                    full_title = '%s %s' % (str(track[0]).zfill(2), title)

                albums[album].append( (full_title, fn) )
                artists[artist].add(album)

            except ValueError:
                print 'Error with', fn

for artist, albums_set in artists.iteritems():

    print artist, list(albums_set)
    artist_dn = join(prefix, artist)

    for album in albums_set:
        print '\t', album
        dn = join(artist_dn, album)
        dn = dn.strip()
        if not exists(dn):
            os.makedirs(dn)

        for title, fn in albums[album]:
            if not title:
                title = splitext(basename(fn))[0]

            # escape path separator
            title = title.replace(os.sep, '-')

            tget = join(dn, title + '.mp3')

            print 2 * '\t', title, tget

            try:
                copy2(fn, tget)
            except IOError:
                set_trace()
