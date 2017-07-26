## Position The Cursor Almost Anywhere Inside Standard Text Mode Python Terminal.  
Originally published: 2012-06-17 17:10:28  
Last updated: 2012-06-17 17:10:29  
Author: Barry Walker  
  
A DEMO showing the power of the ANSI (ASCII) _Esc_ codes in standard text mode Python.

ANSI _Esc_ codes here:-    http://www.termsys.demon.co.uk/vtansi.htm

There are only three important things from the ANSI _Esc_ codes that are needed to obtain a neat finish to a program written in standard text mode Python:-

1) Clearing the screen. (Already done without the dedicated ANSI _Esc_ code!)

2) Colours and other character attributes. (Already done!)

3) A forced printing of a character or string from a given location inside the Terminal window.

To clear the screen does NOT require another dedicated ANSI _Esc_ code, (although it exists). This code uses the print("\r\n") method which works in all cases coupled with the one function supplied......

For The Classic AMIGA, E-UAE, WinUAE and Linux using Python(s) 1.4.0 to Python 3.2.2. Read the code for more information...

Enjoy finding simple solutions to often very difficult problems...

Bazza, G0LCU.
