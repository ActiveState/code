###very poor man's xml parser and generator

Originally published: 2006-04-04 06:06:07
Last updated: 2006-04-18 13:53:33
Author: Ferdinand Jamitzky

Sometimes one needs a quick and dirty solution for parsing and generating xml. This recipe uses only the python parser itself for the parsing of xml. xml code is translated to valid python code and then evaluated. The generated objects can then be manipluated within python itself and treated as regular python objects.