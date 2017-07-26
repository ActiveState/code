## Python helper to open SciTe .session files in Windows Explorer  
Originally published: 2008-04-19 07:49:14  
Last updated: 2008-04-19 07:49:14  
Author: Fred Pacquier  
  
Associating Scite .session files with "scite.exe -loadsession:" poses a problem in Windows because of the backslashes in the file path. To avoid this, copy this script to the Scite directory and associate it with .session files instead. Then you can double-click on a .session file in any project directory and it will be loaded in SciTe.