## Javascript Namespaces

Originally published: 2009-07-12 07:16:52
Last updated: 2009-07-12 07:21:40
Author: Mike Koss

This recipe enables you to modularize javascript libraries by placing all library code within a namespace object.  All namespaces are rooted at "window.global_namespace".  References between namespaces are supported by the Import function, which allows forward references to namespaces that have yet to be defined.\n\nSee code comment for more detailed examples.