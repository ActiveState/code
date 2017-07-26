###Simple reverse converter of unicode code points string

Originally published: 2009-09-22 19:58:33
Last updated: 2009-09-22 20:02:32
Author: Ryan 

It's a simple recipe to convert a str type string with pure unicode code point (e.g string = **"\\u5982\\u679c\\u7231"** ) to an unicode type string. \nActually, this method has the same effect with **'u'** prefix. But differently, it allows you to pass a variable of code points string as well as a constant one.\n  