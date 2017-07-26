###Import of subpackages from different physical locations

Originally published: 2008-01-10 06:03:03
Last updated: 2008-01-10 06:03:03
Author: Dirk Holtwick

If you want do distribute different modules in separate packages but under the same top directory that may be a problem when importing those modules. Since Python 2.5 the "pkgutil", described in the Python documentation under chapter 29.3, solves this problem.