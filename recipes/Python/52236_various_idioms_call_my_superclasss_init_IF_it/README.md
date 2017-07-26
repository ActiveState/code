## various idioms for "call my superclass's __init__ IF it has one"Originally published: 2001-03-21 01:22:19 
Last updated: 2001-04-27 14:48:19 
Author: Alex Martelli 
 
Python does not automatically call the __init__ (and __del__) methods of superclasses if subclasses define their own; explicit calling is needed, and it may be advisable to use a call-if-it-exists idiom.