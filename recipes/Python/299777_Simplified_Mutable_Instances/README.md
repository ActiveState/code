## Simplified Mutable Instances  
Originally published: 2004-08-15 04:26:41  
Last updated: 2004-08-15 04:26:41  
Author: Tim Fitz  
  
Often you want to just create an instance with nothing in it, then modify arbitrary values. According to the standard you should do:\nclass Something:\n  pass\nI propose the following better solution: