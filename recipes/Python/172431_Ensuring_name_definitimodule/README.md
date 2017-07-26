## Ensuring a name definition in a module namespace

Originally published: 2003-01-06 13:47:23
Last updated: 2008-07-31 09:32:27
Author: Steven Cummings

Ensure that a name exists in a target namespace. If it does not, make it available in the target namespace using the given definition. The target should be a namespace dictionary (presumably for a module, see the discussion below otherwise). The default target is __builtins__ (specificially, __builtins__.__dict__).