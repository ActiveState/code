###Swapping two variables without using a third (temporary) variable

Originally published: 2015-09-19 19:51:21
Last updated: 2015-09-19 19:51:22
Author: Vasudev Ram

This recipe shows how to swap the values of two variables without making use of a third, temporary variable. The traditional method of swapping two variables is using a temp variable.\n\nThe first method shown here, swaps two variables an and b without using a temp variable. The variables a and b are integers:\n\na = 1, b = 2\n# Prints original values of a and b, i.e. 1 and 2:\nprint a, b\na = a + b\nb = a - b\na = a - b\n# Prints swapped values of a and b, i.e. 2 and 1:\nprint a, b\n\nThe above swap method, using arithmetic expressions, will not work for non-numeric data types, and may also not work (at least in some cases) for floats. But the method below should work for any type of Python variable:\n\nIt even works for function objects. If you have:\n\ndef foo(): print "This is foo()."\ndef bar(): print "This is bar()."\n\nand then:\n\nfoo(), bar()\n\nand then:\n\nfoo, bar = bar, foo\n\nthen see what happens to values foo and bar, when you do:\n\nfoo()\nbar()\n\n\n\n\n