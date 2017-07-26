## Loading c extensions from a repository build area 
Originally published: 2015-10-12 09:38:48 
Last updated: 2015-10-12 09:38:49 
Author: Robin Becker 
 
I test reportlab with multiple pythons. Rather than having to install into different virtualenvs I prefer to build my C-extensions in the repository using pythonxx setup.py build_ext and place the repository source folder onto the python path (using eg a link). However, this means I must load the extensions from somewhere other than their natural place. The BuiltExtensionFinder can be used for this.