## Components and Abilities (different implementation of Component architecture)  
Originally published: 2009-07-23 10:58:51  
Last updated: 2009-07-23 13:26:32  
Author: Danny G  
  
I define a 'Component' as an attribute (typing optional) that instances can assign objects to.  Nothing special there, but their usefulness comes in with 'Abilities'.  If a class inherits from 'ClassWithAbilities', it will be given a special attribute 'abilities' that will grow/shrink when other classes with abilities are assigned to an instances attributes. It increases/decreases the functionality of the instance depending on what objects are assigned to it.  All of these abilities are accessed through the 'abilities' attribute.  This is a redesign of [Recipe 576852](http://code.activestate.com/recipes/576852/), but I believe is different enough to warrant a new recipe.