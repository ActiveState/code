## Reusing default function arguments 
Originally published: 2005-10-12 11:30:21 
Last updated: 2005-10-12 20:37:53 
Author: George Sakkis 
 
This recipe applies the "once and only once" principle to function default values. Often two or more callables specify the same default values for one or more arguments. This is especially typical when overriding a method. Using the defaultsfrom(func) decorator, a method may 'inherit' the default values from the super method. More generally, any function may inherit the default values from another one.