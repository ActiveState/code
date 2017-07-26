## zip_pad(), a lazy zip() that pads all but the longest iterable with None 
Originally published: 2006-08-31 05:51:31 
Last updated: 2006-08-31 05:51:31 
Author: Peter Otten 
 
On the rare occasion that you want to fill the sequences passed to zip() with a padding value, at least use something fast.\nYou can optionally specify a padding value other than None.