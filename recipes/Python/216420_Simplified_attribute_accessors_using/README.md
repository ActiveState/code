## Simplified attribute accessors using overloadingOriginally published: 2003-08-17 00:57:14 
Last updated: 2003-08-17 00:57:14 
Author: Ulrich Hoffmann 
 
This recipe presents an ideom for simplified accessors, that combines\ntypical getter and setter functionality of an attribute into a single\noverloaded method, that instead of getATTRIBUTE and setATTRIBUTE can\nnow just be called ATTRIBUTE. When called without arguments it acts as\na getter and retrieves the attribute's value. When called with\narguments, the attribute is set to this value.\n\nUses a neat trick of an exclusive unique value in default arguments.