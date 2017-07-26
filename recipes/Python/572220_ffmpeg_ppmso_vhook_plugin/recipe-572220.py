#!/usr/bin/env python
# Copyright 2008 by Konrads Smelkovs <konrads.smelkovs@gmail.com>

import sys,os,re,time
import Image, ImageOps
from StringIO import StringIO
DEBUG=False

class NoMorePPM(Exception):
    """Signals that there are no more PPM files
    """
    

def read_one_ppm(f):
    """
    Read exactly one PPM file from a concatenated stream of PPM files.
    Designed to be used for ffmpeg vhook processing
    @return: PPM string
    """
    
    ppm=""
    formatDef=f.readline() # Read format definition from stream
    if formatDef=="":
        # Supposedly we've reached end of file
        raise NoMorePPM()

    format=re.match("P\d", formatDef, re.I)
    assert format is not None
    ppm+=formatDef
    sizeDef=f.readline()
    sizeMatch=re.match("(\d+)\s+(\d+)",sizeDef)
    assert sizeMatch is not None

    
    (x,y)=sizeMatch.groups()
    if DEBUG:
        sys.stderr.write("X: %s, Y: %s\n" % (x,y))
    ppm+=sizeDef
    maxCol=f.readline()
    ppm+=maxCol
    ppm+=f.read(int(x)*int(y)*3)    # Read 24bit units
    if DEBUG:
        sys.stderr.write("Len: %s\n" % str(ppm.__len__()))
    return ppm


def main():
    i=0
    while(True):
        try:
            
            ppm=StringIO(read_one_ppm(sys.stdin))
            im=Image.open(ppm)
        
            #encode.encode(im, bool(i%2))
            im2=ImageOps.flip(im)
            tmpo=StringIO()
            im2.save(tmpo,"PPM")
            if DEBUG:
                ppm.seek(0)
                f=file("/tmp/source-%i.ppm" % i,"wb")
                f.write(ppm.read())
                f.close()
                tmpo.seek(0)
                f=file("/tmp/output-%i.ppm" % i,"wb")
                f.write(tmpo.read())
                f.close()
                ppm.seek(0)
                
            tmpo.seek(0)
            sys.stdout.write(tmpo.read())
            sys.stdout.flush() #Must flush each frame
            if DEBUG:
                sys.stderr.write("Wrote frame %i\n" % i)
            i+=1
        except NoMorePPM, e:
            time.sleep(0.01)    # Handle empty buffer
        
    
if __name__=="__main__":
    main()
