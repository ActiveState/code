## Word Wrap for Proportional Fonts  
Originally published: 2011-11-11 21:29:20  
Last updated: 2011-11-11 21:29:21  
Author: Michael Fogleman  
  
Word wrap function / algorithm for wrapping text using proportional (versus 
fixed-width) fonts.

`text`: a string of text to wrap
`width`: the width in pixels to wrap to
`extent_func`: a function that returns a (w, h) tuple given any string, to
               specify the size (text extent) of the string when rendered. 
               the algorithm only uses the width.

Returns a list of strings, one for each line after wrapping.