## Automatic delegation through descriptors  
Originally published: 2005-04-25 10:22:23  
Last updated: 2005-04-25 10:22:23  
Author: Diego Novella  
  
When you want a class instance to act as if it was an instance of another class (at least from some aspect), but for some reason you can't use multiple inheritance, You have to deal with some kind of "delegation": You embed an object of the other instance as an attribute of your main instance, and then create as much attributes as you can that "point to" corresponding attribute of the embedded instance. To avoid all that coding stuff, here's a function, "immerse", that automatically sets as class properties all attributes that an instance of another class have, and that are not in the main class.\n