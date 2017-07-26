## Windows clipboard viewer  
Originally published: 2004-12-04 12:50:56  
Last updated: 2004-12-04 12:50:56  
Author: Georg Nelles  
  
With the "SetClipboardViewer" function you can add a window to the chain of clipboard viewers. Whenever the content of the clipboard changes, a message is send to the clipboard viewer windows. A clipboard viewer window must process two messages and pass them to the next window in the chain.\nWith a sample about hooking the window procedure of a wxPython Frame, I made up the following clipboard viewer.