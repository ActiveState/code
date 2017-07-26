###Multiple handlers for xml.sax parser

Originally published: 2006-01-05 20:53:33
Last updated: 2006-01-05 20:53:33
Author: Jeremy Dunck

SAX is commonly used on large XML files because they don't fit nicely into core memory necessary for the friendlier DOM API.\n\nWhen dealing with -really- large XML files, multiple passes over the file becomes costly.\n\nThe SAX handler in this recipe allows you to handle an XML file multiple ways in a single pass by dispatching to the handlers you supply.