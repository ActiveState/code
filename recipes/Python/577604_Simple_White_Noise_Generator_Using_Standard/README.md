## Simple White Noise Generator Using Standard Python In Linux.  
Originally published: 2011-03-10 18:03:54  
Last updated: 2011-03-10 18:03:55  
Author: Barry Walker  
  
Simple White Noise Generator Using Standard Python In Linux - noise.py

This code is a stand alone program to generate a signal, at the earphone sockets, of white noise.

It needs /dev/dsp to work; if you haven't got it then install oss-compat from your distro's repository.
(NOTE:- /dev/audio could also be used but I decided to use /dev/dsp to show that this was within easy
reach of standard Python too.)

Ensure the audio system is NOT in use for this to work and all the levels are set up for your normal requirements.
In my case root level WAS NOT required but that does not mean that root level IS NOT required - so be aware.

All that is required to make this a piece of audio test equipment is a cable plugged into to the earphone
socket. The output level is fully controllable inside the code and the noise is generated in about 10 second
bursts

Assuming it is copied into the module(s) drawer just type:-

>>> import noise[RETURN/ENTER]

And away you go...

This is Public Domain and you may do with it as you like.

Read the program for more information.
(There will be more to come in the future... :)

Enjoy finding simple solutions to often very difficult problems... ;o)


73...

Bazza, G0LCU...

Team AMIGA...
