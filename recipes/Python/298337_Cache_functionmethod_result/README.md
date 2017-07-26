## Cache function/method result  
Originally published: 2004-08-03 05:54:55  
Last updated: 2004-08-03 05:54:55  
Author: Sakesun Roykiattisak  
  
I use this for my database lookup function to minimize sql execution.
It can also be useful in other contexts.
I think it work even without "make_immutable", but it's probably safer this way.
The class "DictTuple" is ugly. However, AFAIK, there are no ImmutableDict.