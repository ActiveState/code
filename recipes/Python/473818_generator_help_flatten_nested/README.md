## A generator to help flatten nested loops

Originally published: 2006-02-01 20:38:59
Last updated: 2006-02-02 04:48:05
Author: Scott Lees

Transforms nested loops like\n<pre>for x in range(width):\n    for y in range(height):\n        do_something(x,y)</pre>\ninto:\n<pre>for x,y in nest(width, height):\n    do_something(x,y)</pre>