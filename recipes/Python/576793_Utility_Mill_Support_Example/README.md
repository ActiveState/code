## Utility Mill Support Example 
Originally published: 2009-06-03 14:36:25 
Last updated: 2009-06-03 14:36:25 
Author: Stephen Chappell 
 
For those of you wondering how use "utility_mill" (my previous recipe), check out "hard_test()" and "soft_test()" in this example usage. The code in the lower sections generates test data and is only useful if trying to understand the "expressions" recipe initially ported from C#. The hard test shows how easy it is to execute a utility that you know the name of. The most recent version is used, but this can be inefficient. The soft test runs the same utility once a minute but only updates the version once an hour. This can saves the Utility Mill some extra work that may not be necessary.