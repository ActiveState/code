###Implementing the make statement by hacking bytecodes

Originally published: 2006-11-04 13:43:00
Last updated: 2008-12-31 09:47:48
Author: Nilton Volpato

The make statement from PEP 359 is implemented using decorators and function definitions.\n\nThe make statement:\n\n    make <callable> <name> <tuple>:\n        <block>\n\nis implemented this way:\n\n    @make(<callable>, <tuple>)\n    def <name>():\n        <block>\n\nThe code also has some examples, using the make decorator to create a namespace and a class.