## Object snoop - experiment with Python special methods 
Originally published: 2010-09-05 16:46:48 
Last updated: 2010-09-05 17:54:50 
Author: Wai Yip Tung 
 
In Python, classes can define their own behavior with respect to language operators. For example, if a class defines __getitem__(), then x[i], where x is an instance of the clas, will be execute by a call to x.__getitem__(i).\n\nWhile Python has an extensive documentation on the special methods, reading a specification may not be the best way to reveal the intricate details. **object_snoop** allows user to observe how Python expressions and statements are translated into special method calls. object_snoop defines most special methods. It simple print a trace and returns a fixed but sensible result. Users are invited to build complex expressions to experiment how Python special methods work.\n