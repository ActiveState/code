###Coding Standard Adaptor

Originally published: 2006-02-16 20:17:17
Last updated: 2006-02-16 20:17:17
Author: Moe Aboulkheir

this recipe contains a function, "rename_members", which takes an object, and two strings describing variable naming conventions (e.g. "allcamel", "underscores", etc).  it translates attribute names on the given object from the first naming convention to the second (it doesn't delete the original attributes).  the function also takes an optional acceptance function, which will be passed each attribute.  the default acceptance function is "callable".