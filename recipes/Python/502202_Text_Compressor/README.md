## Text Compressor  
Originally published: 2007-02-01 21:41:29  
Last updated: 2007-02-01 21:41:29  
Author: Stephen Chappell  
  
This recipe introduces a novel way of compressing
text and is meant primarily as an exercise. The
procedures work best on standard 7-BIT ASCII and
worst on binary encoded data. Please note that
function "encode" returns a string and a key
that must be passed to function "decode" in
order to recover the original data.