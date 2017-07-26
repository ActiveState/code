## Add support for the "in" operator to the attributes map of minidom elementsOriginally published: 2006-06-23 11:11:02 
Last updated: 2006-06-23 18:54:14 
Author: Walker Hale 
 
When you parse XML using minidom, you can get a map of attributes for any element. The problem is that using the "in" operator on this map will raise an exception.  These three lines of code will fix that.