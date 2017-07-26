## Simple enum mechanism  
Originally published: 2012-01-14 18:21:10  
Last updated: 2012-01-15 12:30:31  
Author: Thomas Lehmann  
  
**Here are the basic ideas (orientation: C++)**:
 * You are responsible to find names for constants and this code provides a way to give values which differ from each other
 * The context is to allow different enums with values starting by 0
 * If you like to use constants like here: "Orientation.TOP" then place those constants in the relating class
 * You still can assign your own values

**About the code**:
 * It's not much code also it might look like (implementation + documentation + unittests)
 * The __docformat__ is for epydoc. Temporarily remove the "@singleton" when trying to generate the HTML documentation (can not yet be handled by epydoc).

**Example(s)**:
Have a look at the unittests please.