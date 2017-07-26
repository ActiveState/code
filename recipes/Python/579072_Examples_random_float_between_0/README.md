## Examples for random float between 0 and 1

Originally published: 2015-06-25 17:55:33
Last updated: 2015-06-25 17:55:33
Author: Stephen Chappell

I was researching how floats are stored in a computer and was trying to think up a way to generate random values between 0 and 1. Python already provides an implementation allowing this already, and two of the functions below are directly inspired by that code, but the third is a slightly different way of doing the same thing. A similar version of this code has been used to implement similar functionality in C# at one time. Others might also find it useful if they want to create equivalent code in a separate language while having access to random bytes but not random floats. It should be noted that the various implementations get slower as you go down the list.