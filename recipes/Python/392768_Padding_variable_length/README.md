## Padding variable length sequences 
Originally published: 2005-03-24 20:20:54 
Last updated: 2005-03-25 04:27:43 
Author: George Sakkis 
 
Python tuple unpacking works only for fixed length sequences, that is one cannot write something like:\nfor (x,y,z=0,*rest) in [(1,2,3), (4,5), (6,7,8,9,10)]: print x,y,z,rest\n\nThis recipe returns a pad function that implements this functionality (albeit with less concise syntax). Using the recipe, the example above then can be written as:\npad = padfactory(minLength=2,defaults=(0,),extraItems=True)\nfor x,y,z,rest in map(pad, [(1,2,3), (4,5), (6,7,8,9,10)]): print x,y,z,rest\n