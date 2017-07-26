## PackagePath  
Originally published: 2005-01-19 10:39:22  
Last updated: 2005-01-19 18:40:54  
Author: Shannon -jj Behrens  
  
If you have a hierarchy of packages in a library, permit the user
of your library to have his own hierarchy of packages that "overlays" yours.
That means he can even have classes named the same as your classes, and have
his classes "shadow" yours.  It also means that a project can be broken up into
several top-level directories, all of which have the same package hierarchy
within.