## How to use string.Template from python 2.4

Originally published: 2004-09-09 06:23:32
Last updated: 2004-09-13 10:55:54
Author: John Nielsen

New to python 2.4 is the string.Template class. It is similar to the formatting python already had in which the % operator with strings was used in a recognizable sprintf style of formatting from C. In addition to format types, you also had a choice with a tuple or dictionary mapping.  String.Template simplifies it to only the string format type and dictionary mapping. This makes string formatting easier to remember and use. This example shows you the basics of using the template and the difference with the old style.