## Cache function/method resultOriginally published: 2004-08-03 05:54:55 
Last updated: 2004-08-03 05:54:55 
Author: Sakesun Roykiattisak 
 
I use this for my database lookup function to minimize sql execution.\nIt can also be useful in other contexts.\nI think it work even without "make_immutable", but it's probably safer this way.\nThe class "DictTuple" is ugly. However, AFAIK, there are no ImmutableDict.