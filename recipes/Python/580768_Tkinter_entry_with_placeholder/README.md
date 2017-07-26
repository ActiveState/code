## Tkinter entry with placeholder  
Originally published: 2017-03-31 20:03:57  
Last updated: 2017-04-06 14:21:03  
Author: Miguel Martínez López  
  
The function *add_placeholder_to* adds a placeholder to a tkinter entry.\n\nParameters:\n\n- *entry:* Tkinter widget to add placeholder\n- *placeholder:* Text of placeholder\n- *color:* Color of placeholder (optional)\n- *font*: Font of placeholder (optional)\n\nA placeholder state object is attached to attribute "placeholder_state" of entry widget for future reference. It makes more easier to configure state of placeholder, or change the preferences of the user for color and font for the placeholder.\n\nThis widget is added also to my Metro Tkinter recipe:\n\nhttps://code.activestate.com/recipes/580729-metro-ui-tkinter/