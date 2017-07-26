#!/usr/bin/env python
"""Play sound files using the pygame mixer module."""


__program__   = "soundplay.py"
__author__    = "Christopher Arndt"
__version__   = "1.1"
__revision__  = "$Rev: 136 $"
__date__      = "$Date: 2007-06-06 19:18:47 +0200 (Mi, 06 Jun 2007) $"
__copyright__ = "Public domain"

import sys
import pygame

# global constants
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 30 # how often to check if playback has finished

def playsound(soundfile):
    """Play sound through default mixer channel in blocking manner.
    
    This will load the whole sound into memory before playback
    """

    sound = pygame.mixer.Sound(soundfile)
    clock = pygame.time.Clock()
    sound.play()
    while pygame.mixer.get_busy():
        clock.tick(FRAMERATE)

def playmusic(soundfile):
    """Stream music with mixer.music module in blocking manner.
    
    This will stream the sound from disk while playing.
    """

    clock = pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(FRAMERATE)

def playmusic2(soundfile):
    """Stream music with mixer.music module using the event module to wait
       until the playback has finished.

    This method doesn't use a busy/poll loop, but has the disadvantage that 
    you neet to initialize the video module to use the event module.
    
    Also, interrupting the playback with Ctrl-C does not work :-(
    
    Change the call to 'playmusic' in the 'main' function to 'playmusic2'
    to use this method.
    """

    pygame.init()

    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
    pygame.event.set_allowed(pygame.constants.USEREVENT)
    pygame.mixer.music.play()
    pygame.event.wait()

def main(args):
    # look at command line
    streaming = False
    if args and args[0] == '-s':
        streaming = True
        args.pop(0)
    if not args:
        print >>sys.stderr, "usage: soundplay [-s] FILE"
        print >>sys.stderr, "  -s    use streaming mode"
        return 2

    # initialize pygame.mixer module
    # if these setting do not work with your audio system
    # change the global constants accordingly
    try:
        pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
    except pygame.error, exc:
        print >>sys.stderr, "Could not initialize sound system: %s" % exc
        return 1

    try:
        for soundfile in args:
            try:
                # play it!
                if streaming:
                    playmusic(soundfile)
                else:
                    playsound(soundfile)
            except pygame.error, exc:
                print >>sys.stderr, "Could not play sound file: %s" % soundfile
                print exc
                continue
    except KeyboardInterrupt:
        # if user hits Ctrl-C, exit gracefully
        pass
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
