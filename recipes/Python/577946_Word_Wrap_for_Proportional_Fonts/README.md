## Word Wrap for Proportional FontsOriginally published: 2011-11-11 21:29:20 
Last updated: 2011-11-11 21:29:21 
Author: Michael Fogleman 
 
Word wrap function / algorithm for wrapping text using proportional (versus \nfixed-width) fonts.\n\n`text`: a string of text to wrap\n`width`: the width in pixels to wrap to\n`extent_func`: a function that returns a (w, h) tuple given any string, to\n               specify the size (text extent) of the string when rendered. \n               the algorithm only uses the width.\n\nReturns a list of strings, one for each line after wrapping.