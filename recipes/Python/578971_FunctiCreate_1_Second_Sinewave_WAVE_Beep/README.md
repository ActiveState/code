## A Function To Create A 1 Second Sinewave WAVE Beep File.  
Originally published: 2014-11-23 19:24:45  
Last updated: 2014-11-23 19:24:46  
Author: Barry Walker  
  
sinebeep.py

Creating an audio file called...

beep.wav

...that can be played using almost ANY audio player available.

This simple snippet of code generates a 1 second sinewave WAVE file.
It IS saved inside the CURRENT drawer so that you can find it... ;o)

This works on:-
Classic stock AMIGA A1200, using Python 1.4.0.
WinUAE and E-UAE, AmigaOS 3.0.x using Python 1.4.0 to 2.0.1.
Windows, to at least 7, using Python 2.0.1 to 3.3.2.
Various Linux flavours using Python 2.4.6 to 3.2.2.
Apple OSX 10.7.x and above using Python 2.5.6 to 3.4.1.

The file size is 8044 bytes and _IF_ you need to it can be palyed directly
without a player on some Linux flavours that have the /dev/dsp device.
It is an 8 bit, unsigned integer, mono, 8000Hz sampling speed 8000 byte
RAW file with the WAVE header added.

It will still work with PulseAudio and OSS using...

cat /full/path/to/beep.wav > /dev/dsp

...but with a momenatry click due to the 44 header bytes; but hey it is
a beep alternative...

Enjoy finding simple solutions to often very difficult problems.

Bazza.