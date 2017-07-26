###Simple Matlab/Ocave like arrays conversion to numpy.arrays in python interpreter

Originally published: 2016-09-22 12:25:28
Last updated: 2016-09-22 12:25:30
Author: Przemyslaw Podczasi

Matlab/Octave syntax for 1D/2D arrays is more packed and doesn't require putting extra ',' and extra '[', ']' between dimensions.\nFor this I wrote a parser that intercepts python interpreter and using numpy functionality parses Matlab's style arrays 1D and 2D into numpy.arrays.