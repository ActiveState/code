## Simple Collection class  
Originally published: 2002-01-11 10:00:34  
Last updated: 2002-01-11 10:00:34  
Author: skip   
  
A collection groups a set of objects together and forwards attribute lookups to all elements of the collection that contain the desired attribute.  It's not an error for an element of the collection to be missing an attribute.  The list returned is just missing that value.  The same holds true when forwarding __call__.