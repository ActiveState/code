## Python Easily Packetize / Slice / Chunk TextOriginally published: 2011-09-30 05:33:09 
Last updated: 2011-09-30 05:34:57 
Author: __nero  
 
I needed to chunk up some text to send over UDP and didn't want to have messy for loops with an if condition for size and then the little bit left over.  All that struck me as very messy.  I then thought of the re module and came up with a very simple solution to chunk up data.