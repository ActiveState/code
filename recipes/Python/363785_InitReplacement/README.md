## InitReplacement

Originally published: 2005-01-19 10:54:34
Last updated: 2005-01-19 10:54:34
Author: Shannon -jj Behrens

Hack a class's __init__ method without subclassing the class\nbecause a) you can't modify the original class and b) you can't modify other\nclasses already using the first class.  This is a gross hack that should only\nbe used to work around flaws in libraries you have no control over.  I've\nchanged the names to protect the innocent.