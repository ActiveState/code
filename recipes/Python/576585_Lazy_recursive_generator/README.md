## Lazy, recursive generator function  
Originally published: 2008-12-14 09:56:13  
Last updated: 2008-12-14 10:04:29  
Author: Don Sawatzky  
  
This procedure was proposed as a challenge to Python and other languages as the most concise coding.  See Icon programming on the web.  This is a lazy, recursive generator.  It can be implemented several ways in Python with lists, iteration, and recursion.  However, the lists increase in size exponentially with each iteration and recursion plus they are saved in every recursion.  This recipe develops a lazy generator function.\n\n