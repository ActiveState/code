## Using doctests to verify a module's export listOriginally published: 2012-09-19 17:28:39 
Last updated: 2012-09-19 19:13:20 
Author: Sam Denton 
 
If you aren't very careful, modules can end up exporting more symbols than you intend.  For example, everything that you import is added to your module's name-space.  Then there's scaffolding and other stuff intended for internal use.  The usual advice is to name everything with a leading underscore, but that gets complicated fast:  "import sys as _sys", "from os import environ as _environ".  The alternative is to use "__all__ " to define exactly what you want to export, but then you need to maintain it as you add things to your module.  *Or do you?*