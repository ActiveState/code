## Setting Namespaces  
Originally published: 2012-07-05 02:28:28  
Last updated: 2012-07-05 02:39:42  
Author: Stephen Chappell  
  
Provides a simple way to deal with program variable versioning.

This module defines two classes to store application settings so that
multiple file versions can coexist with each other. Loading and saving
is designed to preserve all data among the different versions. Errors
are generated to protect the data when type or value violations occur.