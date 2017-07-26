## Finding the location of the taskbar in wxPython  
Originally published: 2005-07-05 14:36:28  
Last updated: 2005-07-05 14:36:28  
Author: Jan Persson  
  
In Windows explorer the user can choose to have the taskbar field on any of the for sides of the screen (i.e top, bottom, left or right). This means that code that needs to display windows relative to this selection has to know where the taskbar is placed.\n\nThis little procedure finds the position of the taskbar field and returns "top",\n"bottom", "left" or "right" depending on the choice of the user.