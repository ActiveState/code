## Setting NamespacesOriginally published: 2012-07-05 02:28:28 
Last updated: 2012-07-05 02:39:42 
Author: Stephen Chappell 
 
Provides a simple way to deal with program variable versioning.\n\nThis module defines two classes to store application settings so that\nmultiple file versions can coexist with each other. Loading and saving\nis designed to preserve all data among the different versions. Errors\nare generated to protect the data when type or value violations occur.