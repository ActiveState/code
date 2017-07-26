"""
vlc2cue.py

By Anton Vredegoor. Last edit: Monday July 25, 2011.

Send comments to: anton.vredegoor@gmail.com

License: GPL, however there are no warranties, use at your own risk.

This needs vlc.py, see http://wiki.videolan.org/Python_bindings

The idea is to play an online audio stream locally while also 
saving it to an mp3 file and record some meta data in a cue file. 

I made this because I often forget the name of the song I 
listened to, so I have to wait till it is played again, or compare
twitter feeds with the file date of my recorded mp3. And vlc
seems not to record meta info, at least not for mp3.

Writing this also made me appreciate and become more
comfortable with vlc.py. It is very nice! 

As a further benefit, vlc and many other players (foobar f.e.) can 
read cue files. So now I not only have the names of the songs I like 
but by clicking on them in the playlist (a playlist that has multiple 
songs in a single mp3 file) the cursor moves more or less to the 
starting time of the song.  It probably depends on the accuracy 
with which the broadcaster announces the change of track.
"""

import vlc
import time
import os

def new_filename(ext = '.mp3'):
    "find a free filename in 00000000..99999999"
    D = set(x[:8] for x in os.listdir('.')
        if (x.endswith(ext) or x.endswith('.cue')) and len(x) == 12)
    for i in xrange(10**8):
        s = "%08i" %i
        if s not in D:         
            return s

def initialize_cue_file(name,instream,audiofile):
    "create a cue file and write some data, then return it"
    cueout = '%s.cue' %name
    outf = file(cueout,'w')
    outf.write('PERFORMER "%s"\n' %instream)
    outf.write('TITLE "%s"\n' %name)
    outf.write('FILE "%s" WAVE\n' %audiofile)
    outf.flush()
    return outf
    
def initialize_player(instream, audiofile):
    "initialize  a vlc player which plays locally and saves to an mp3file"
    inst = vlc.Instance()   
    p = inst.media_player_new()   
    cmd1 = "sout=#duplicate{dst=file{dst=%s},dst=display}" %audiofile
    cmd2 ="no-sout-rtp-sap"
    cmd3 = "no-sout-standard-sap"
    cmd4 ="sout-keep"
    med=inst.media_new(instream,cmd1,cmd2,cmd3,cmd4)   
    med.get_mrl()    
    p.set_media(med)
    return p, med

def write_track_meta_to_cuefile(outf,instream,idx,meta,millisecs):
    "write the next track info to the cue file"
    outf.write('  TRACK %02i AUDIO\n' %idx)
    outf.write('    TITLE "%s"\n' %meta)
    outf.write('    PERFORMER "%s"\n' %instream)
    m = millisecs // 60000
    s = (millisecs - (m*60000)) // 1000
    hs = (millisecs - (m*60000) - (s*1000)) //10
    ts = '%02i:%02i:%02i'  %(m,s,hs)
    outf.write('    INDEX 01 %s\n' %ts)
    outf.flush()
    
def test():
    #some online audio stream for which this currently works ....
    instream = 'http://streamer-mtc-aa05.somafm.com:80/stream/1018'
    #if the output filename ends with mp3 vlc knows which mux to use
    ext = '.mp3'
    name = new_filename(ext)
    audiofile = '%s%s' %(name,ext)
    outf = initialize_cue_file(name,instream,audiofile)
    p,med = initialize_player(instream, audiofile)
    p.play()
    np = None
    i = 0
    while 1:
        time.sleep(.1)
        new = med.get_meta(12)
        if new != np:
            i +=1
            t = p.get_time()
            print "millisecs: %i" %t
            write_track_meta_to_cuefile(outf,instream,i,new,t)
            np = new
            print "now playing: %s" %np

if __name__=='__main__':
    test()
        
        
