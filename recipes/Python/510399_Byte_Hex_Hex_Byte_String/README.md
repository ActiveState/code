## Byte to Hex and Hex to Byte String Conversion  
Originally published: 2007-03-21 06:35:40  
Last updated: 2007-03-21 06:35:40  
Author: Simon Peverett  
  
I write a lot of ad-hoc protocol analysers using Python. Generally, I'm dealing with a byte stream that I want to output as a string of hex. Sometimes, I want to convert it back again. Eventually, I got round to putting the functions in a module so I wouldn't keep cut and pasting them :)