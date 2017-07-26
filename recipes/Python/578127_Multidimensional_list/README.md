## Multidimensional list

Originally published: 2012-05-12 05:51:37
Last updated: 2012-05-12 06:21:11
Author: Glenn 

Pass a tuple of positive integers of length N (any length) as dimensions to MDarray, and a list is created with the length equal to the product NNN of the dimensions specified in the tuple. The items are initialized to None, or to the value of the optional init parameter.  As a special case, passing an integer for dims creates a square array of that size (converts the integer to a tuple of length two with the same value for both entries).\n\nYou can then index the list with single numbers in range(NNN), or by a tuple of the same length N with which the list was created.\n\n    ary = MDarray(( 5, 6, 8 ), 0 )\n    ix = ary.index_from_tuple(( 2, 4, 3 ))\n    print( ix ) # 87\n    print( ary[ 2, 4, 2 ], ary[ 2, 4, 3 ], ary[ 2, 4, 4 ]) # 0, 0, 0\n    print( ary[ 86 ], ary[ 87 ], ary[ 88 ]) # 0, 0, 0\n    ary[ 2, 4, 3 ] = 25\n    print( ary[ 2, 4, 2 ], ary[ 2, 4, 3 ], ary[ 2, 4, 4 ]) # 0, 25, 0\n    print( ary[ 86 ], ary[ 87 ], ary[ 88 ]) # 0, 25, 0