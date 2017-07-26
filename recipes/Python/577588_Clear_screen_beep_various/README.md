## Clear screen and beep for various platforms.  
Originally published: 2011-02-26 14:26:02  
Last updated: 2011-02-26 14:26:02  
Author: Barry Walker  
  
This little module gives a clear screen and beep for the classic AMIGA, WinUAE, Windows and Linux all in
CLI/Command-Prompt/Terminal mode.

It works from Python 1.4.x to 2.7.x; talk about backwards compatibility... ;oD
With very little modification it will work on Python 3.x.x easily.)

See the file clsbeep.py attached for more information.

it is saved as clsbeep.py and placed into the Python - Lib drawer or where-ever the modules are located
and called as a module:-

>>> import clsbeep

Its usage is:-

clsbeep.cls() and clears the screen.
clsbeep.beep() and creates an error beep.
clsbeep.both() creates an error beep first then clears the screen.

It is Public Domain and if you modify it to suit other platforms please let me have a copy of your code... :)

Enjoy finding simple solutions to often very difficult problems. ;o)