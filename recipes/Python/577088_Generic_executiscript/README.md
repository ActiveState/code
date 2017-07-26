## Generic execution script for a package/application

Originally published: 2010-03-06 15:48:22
Last updated: 2010-03-06 16:10:35
Author: Brett Cannon

If you keep your application's front-end execution logic in a `__main__.py` file within your package and change the `XXX` string to the name of your application's package, this script will handle executing your application for you just like how Python's `-m` option does it.