###Use Simple Plugins to Seemlessly Modify Modules at Import Time

Originally published: 2011-06-07 22:47:40
Last updated: 2011-07-12 18:55:18
Author: Eric Snow

This recipe uses the PEP 302 import hooks to expose all imported modules to devious behavior.\n\nSimply put, the module is imported like normal and then passed to a hacker object that gets to do whatever it wants to the module.  Then the return value from the hack call is put into sys.modules.\n\nRecipe 577741 and recipe 577742 are more concrete examples of using this recipe.