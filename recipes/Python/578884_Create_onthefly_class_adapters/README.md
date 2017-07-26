## Create on-the-fly class adapters with functools.partial  
Originally published: 2014-05-29 18:48:24  
Last updated: 2014-05-29 18:48:28  
Author: Christoph Schueler  
  
functools.partial could not only applied to functions it also works with classes.
This opens some interesting perspectives, like on-the-fly creation of class
adapters, as the following code illustrates.