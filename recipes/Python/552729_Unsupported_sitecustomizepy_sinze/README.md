## Unsupported sitecustomize.py sinze Python 2.5Originally published: 2008-03-26 12:23:19 
Last updated: 2008-03-26 12:23:19 
Author: Dirk Holtwick 
 
Since Python 2.5 the automatic import of the module "sitecustomize.py" in the directory of the main program is not supported any more (even if the documentation says that it is). Putting this little script named "sitecustomize.py" in the default Python path like in "site-packages" should solve this problem.