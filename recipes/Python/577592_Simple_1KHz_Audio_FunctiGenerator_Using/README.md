## Simple 1KHz Audio Function Generator Using Standard Python In Linux...  
Originally published: 2011-03-01 18:33:26  
Last updated: 2011-03-01 19:37:16  
Author: Barry Walker  
  
Simple 1KHz Audio Function Generator Using Standard Python In Linux - afg.py
----------------------------------------------------------------------------

This code is a stand alone program to generate a signal, at the earphone sockets, of 1KHz.
It is a basic audio signal generator and can be used as a starter test signal source for amateur electronics
enthusiasts testgear suite(s).

It needs /dev/audio to work; if you haven't got it then install oss-compat from your distro's repository.

Ensure the audio system is NOT in use for this to work.

Sine, Square, Triangle, Sawtooth+, Sawtooth-, Pulse+ and Pulse- signals are generated in 10 second bursts.
The waveforms generated are unfiltered and therefore not "pure", but hey, an audio function generator
signal source, for free, without external hardware, AND, using standard Python, what more do you want... :)
An oscilloscope will show the waveforms generated at the earphone socket.

Noise is not included but that is SO easy that I left it out FTTB.
(This will be a future upload. ;o)

All that is required to make this a piece of audio test equipment is a cable plugged into to the earphone
socket.

Assuming it is copied into the module(s) drawer just type:-

>>> import afg[RETURN/ENTER]

And away you go...

This is Public Domain and you may do with it as you like.

Read the program for more information.
(There will be more to come in the future... :)