## Simple audio with ctypes and SDL also for Tkinter  
Originally published: 2015-06-18 20:39:39  
Last updated: 2015-08-17 18:54:17  
Author: Jiri Justra  
  
I've needed just to play audio in my Tkinter application, but it seems there is no easy way to do this, so I have made this simple code. It is small ctypes wrapper around SDL_mixer.\n\nIt should work for Win and *nix also .. I've tested it on ubuntu-14.04.3-desktop-i386\n