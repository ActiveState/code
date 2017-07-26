## Package / Module Versioning Bootstrap Loader & Manager 
Originally published: 2004-06-01 09:51:02 
Last updated: 2004-06-01 09:51:02 
Author: Clayton Brown 
 
These two scripts together allow packages to be migrated into a versioned directory structure, allowing a script to specify minimum version / interpretor / platform requirements at time of import, defaulting to the the newest/highest version when not specified, raising exceptions where necessary.\nSpecifying the level at which the PythonInterpretor or Package is Incompatible.\n\nversioner.py      - recurses a site-packages directory managing __init__.py's\nversion_loader.py - when placed in a directory with versioning runs at time package is imported ensuring selection/compatibility of package from those avaliable