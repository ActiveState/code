## Create module directly from a filesystem pathOriginally published: 2011-07-15 04:13:24 
Last updated: 2011-07-15 04:13:59 
Author: Nick Coghlan 
 
Given a filesystem path, use it to create a valid Python module. Based on ``runpy.run_path()``, so accepts Python source files, compiled Python files and directories and zipfiles containing __main__.py files as valid targets.