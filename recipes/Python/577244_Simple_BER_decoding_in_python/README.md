## Simple BER decoding in pythonOriginally published: 2010-05-26 10:05:22 
Last updated: 2010-05-26 10:05:22 
Author: Dima Tisnek 
 
Splits a string into BER TLV's and returns a dict of {type(hex): value(binary)}\nDoesn't interpret tags, Descend into compound tags.