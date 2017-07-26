## xzip - Iterative zip function for very large collections  
Originally published: 2009-03-30 14:54:40  
Last updated: 2009-03-30 14:54:40  
Author: Tucker Beck  
  
The xzip function provides the same functionality as zip (python builtin), but utilizes a generator list comprehension so that zipped collections can be accessed iteratively.

Example:
for t in xzip( xrange( 1000000 ), xrange( 1000000, 2000000, 1 ), xrange( 888,100000000, 1 ):
    print t

This Will begin to produce output immediately, because the collections are zipped iteratively
The output of this code is exactly equivalent to:

for t in zip( xrange( 1000000 ), xrange( 1000000, 2000000, 1 ), xrange( 888,100000000, 1 ):
    print t

However, the second block (using zip) must first build the zipped collection entirely before the
for loop can iterate over it.  This could take a long time.

Note, I used xrange here so that we don't have to wait for python to build the initial lists.
The xzip function would probably show its usefulness most if one had several huge collections that
needed to be combined iteratively.

I developed this function to zip long lists ( >100000 ) of vertex triples with color triples in a volume
visualizer.

