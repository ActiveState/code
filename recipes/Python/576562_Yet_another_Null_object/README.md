## Yet another Null object 
Originally published: 2008-11-11 15:24:20 
Last updated: 2008-11-11 15:24:20 
Author: George Sakkis 
 
This recipe builds on two previously posted recipes for a [null](http://code.activestate.com/recipes/68205/) or [dummy](http://code.activestate.com/recipes/576447/) object by modifying a few methods (e.g. as in SQL, `Null == Null` is Null, not True), supporting most (all?) special methods (e.g. int(Null)) and providing correct pickling/unpickling.