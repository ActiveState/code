## win32com - Accessing AutoCAD entities  
Originally published: 2005-08-30 13:48:52  
Last updated: 2005-08-30 13:48:52  
Author: Ed Blake  
  
Autodesk's AutoCAD drafting software has for a number of versions included an increasingly complete COM interface.  Using the Python win32com modules we have been able to automate some aspects the software; unfortunately because of the organization of the interface certain methods and properties were inaccessible from Python.  In recent versions of the win32 modules a new function has been added though: win32com.client.CastTo().  By casting our objects as the correct type we now have access to much of the object model that used to be unreachable.\n\nIn this example we search the ModelSpace collection for text objects.  Once found we then cast them and alter one of the text specific properties.  To test this code open AutoCAD and in a blank file add at least one dtext object with 'Spam' as its value.