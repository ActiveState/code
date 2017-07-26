## pkgconfig parser

Originally published: 2005-12-10 06:17:32
Last updated: 2005-12-10 06:17:32
Author: Dunk Fordyce

This recipe creates a class to allow access to variables stored in pkg-config files ( or '.pc' files ). This is usefull in conjunction with distutils to get correct information for compiling external C/C++ modules. Variable substitution is performed with string.Template.