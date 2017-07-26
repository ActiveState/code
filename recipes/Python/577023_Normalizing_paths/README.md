## Normalizing paths  
Originally published: 2010-01-26 14:35:12  
Last updated: 2010-01-26 14:39:00  
Author: Gustavo Narea  
  
While dealing with paths, it's often necessary to make sure they all have the same structure so any operation you perform on them can be reliable, specially when it comes to comparing two or more paths. Unusual paths like "/this//is//a///path" or "another/path" can cause unexpected behavior in your application and this is where this function comes into play.