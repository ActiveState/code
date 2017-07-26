###Classifying characters using nested conditional expressions

Originally published: 2017-04-27 21:22:27
Last updated: 2017-04-27 21:26:00
Author: Vasudev Ram

Python has a feature called conditional expressions, similar to C's ternary operator. For example:\n\nprint n, 'is odd' if n % 2 == 1 else 'is even'\n\nHere, the conditional expression is this part of the print statement above:\n\n'is odd' if n % 2 == 1 else 'is even'\n\nThis expression evaluates to 'is odd' if the condition after the if keyword is True, and evaluates to 'is even' otherwise.\n\nThe Python Language Reference section for conditional expressions shows that they can be nested. This recipe shows that we can use nested conditional expressions (within a return statement in a user-defined function) to classify characters into lowercase letters, uppercase letters, or neither.\n\nIt also shows how to do the same task using map, lambda and string.join, again with a nested conditional expression, but without using return or a user-defined function.\n\n