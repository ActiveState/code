###Deep list() to convert a nested tuple-of-tuples

Originally published: 2002-01-06 13:22:59
Last updated: 2002-01-06 13:22:59
Author: Drew Perttula

list() will convert a tuple to a list, but any elements that are also tuples\nwill stay as such. This utility function fully converts an arbitrary "tuple tree" to a same-structured list.