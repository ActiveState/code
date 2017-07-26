## A generator to help flatten nested loops  
Originally published: 2006-02-01 20:38:59  
Last updated: 2006-02-02 04:48:05  
Author: Scott Lees  
  
Transforms nested loops like
<pre>for x in range(width):
    for y in range(height):
        do_something(x,y)</pre>
into:
<pre>for x,y in nest(width, height):
    do_something(x,y)</pre>