## Another approach to the "automatic super" issue  
Originally published: 2005-05-07 15:36:38  
Last updated: 2005-05-08 03:10:21  
Author: Diego Novella  
  
This is another way to deal with questions related to the "autosuper" topic. I have used a metaclass "auto" that keep track of every execution context for
the methods in the classes it generates, allowing the user to write "upcall(*args,**kwargs)" from inside a method - say "mymethod" - to mean
"super(C,self).mymethod(*args,**kwargs)", where C is the class the current method is defined in. It's even possible to write just "delegate()" instead of
"super(C,self).mymethod(*args,**kwargs)", when you want the method in the base class to be passed the same parameters the current methods are passed to.