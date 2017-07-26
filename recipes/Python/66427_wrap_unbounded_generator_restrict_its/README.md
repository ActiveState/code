## wrap unbounded generator to restrict its output  
Originally published: 2001-07-25 16:01:55  
Last updated: 2001-07-25 16:01:55  
Author: Tom Good  
  
With Python 2.2+, you can make generators that return unbounded output.  By creating a "wrapper" generator that runs the first generator, you can restrict its output to some defined subset.