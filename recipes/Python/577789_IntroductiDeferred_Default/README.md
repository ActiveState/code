###An Introduction to Deferred Default Arguments

Originally published: 2011-07-14 04:25:50
Last updated: 2011-08-12 23:08:30
Author: Eric Snow

If you have a function that calls another, passing through an argument, you likely want the default argument of your function to match that of the called function.\n\nDeferred default arguments is what I call the technique of using a sentinel for the default argument of your function and having the called function translate the sentinel into its own default argument.\n\nYou'll find a more thorough treatment after the recipe.