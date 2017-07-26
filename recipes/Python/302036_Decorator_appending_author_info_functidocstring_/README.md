###Decorator for appending author info to the function docstring (Python 2.4)

Originally published: 2004-08-26 01:17:58
Last updated: 2004-08-26 01:17:58
Author: Dmitry Vasiliev

Some examples:\n\n<pre>\n>>> @author("John")\n... @author("Paul")\n... def test():\n...     "Test function"\n...\n>>> help(test)\nHelp on function test in module __main__:\n\ntest()\n    Author: John\n    Author: Paul\n    Test function\n</pre>