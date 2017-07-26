## List with fast membership test (__contains__)Originally published: 2010-04-09 00:51:18 
Last updated: 2010-04-18 05:52:57 
Author: Paul Bohm 
 
Just a list subclass with a fast hash based __contains__ provided by a Set. Inheriting from list was far more work than I had anticipated AND the code below is still buggy.\n\nStill, this provides O(1) indexed access and O(1) contains. If you use this expect the slicing code to be broken despite the attempts to get it right. Fixes graciously accepted!