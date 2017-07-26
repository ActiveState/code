## Simple enum mechanism  
Originally published: 2012-01-14 18:21:10  
Last updated: 2012-01-15 12:30:31  
Author: Thomas Lehmann  
  
**Here are the basic ideas (orientation: C++)**:\n * You are responsible to find names for constants and this code provides a way to give values which differ from each other\n * The context is to allow different enums with values starting by 0\n * If you like to use constants like here: "Orientation.TOP" then place those constants in the relating class\n * You still can assign your own values\n\n**About the code**:\n * It's not much code also it might look like (implementation + documentation + unittests)\n * The __docformat__ is for epydoc. Temporarily remove the "@singleton" when trying to generate the HTML documentation (can not yet be handled by epydoc).\n\n**Example(s)**:\nHave a look at the unittests please.