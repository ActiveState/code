## Extract, expand and execute command from QEditor menu file in file association

Originally published: 2010-11-05 22:01:38
Last updated: 2010-11-05 22:01:40
Author: Phil Rist

Given a path to a primary file and a menu path, a section name and a command key,\nextract a command from a QEditor menu and execute it.  Useful from context menu\nentries.  Example use DoM.py -m {o}\\menus.ini do.py * list, on my computer\nsearches c:\\source\\python\\menus.ini for the first command whose key begins with \nlist.  The command is executed without capturing its standard output.