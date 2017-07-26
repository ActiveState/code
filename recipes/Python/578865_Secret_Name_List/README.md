## The Secret Name of List Comprehensions 
Originally published: 2014-04-21 20:09:42 
Last updated: 2014-04-21 20:09:43 
Author: He Gu 
 
Sometimes you want to have a list comprehension refer to itself, but you can't because it isn't bound to a name until after it is fully constructed. However, the interpreter creates a secret name that only exists while the list is being built. That name is (usually) "_[1]", and it refers to the bound method "append" of the list. This is our back door to get at the list object itself.