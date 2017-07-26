## Benford's Law demo

Originally published: 2010-10-19 10:56:50
Last updated: 2010-10-19 10:56:51
Author: Glenn Hutchings

Here's a simple program to demonstrate [Benford's Law](http://en.wikipedia.org/wiki/Benford%27s_law), which also shows the simple power of [matplotlib](http://matplotlib.sourceforge.net).  It reads from a bunch of files (or stdin, if none specified), extracts the leading digits of all number-like strings found, and plots the distribution in a window together with the expected result if Benford's law applies.