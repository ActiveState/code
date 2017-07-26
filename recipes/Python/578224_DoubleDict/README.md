###DoubleDict

Originally published: 2012-07-24 21:22:43
Last updated: 2012-07-24 21:24:14
Author: Stephen Chappell

After seeing requests for being able to access keys in a dictionary by value, the following recipe was born. It creates the `DoubleDict` class and allows just that. To ensure that only one key is returned when accessing it by value, values must be unique just as keys are unique, and this rule is automatically enforced. Most dictionary methods are supported, and many more are added to allow working with the dictionary from the view of the values instead of the keys. Several optional metaclasses are also provided to enable optional features in the `DoubleDict` class such as data consistency checks and atomic method execution.