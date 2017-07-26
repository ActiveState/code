## Tkinter buddies or shorcuts  
Originally published: 2017-04-07 11:42:26  
Last updated: 2017-04-07 11:45:19  
Author: Miguel Martínez López  
  
I provide two convenience functions to create shorcuts. *create_buddy* creates a buddy for the provided label.A buddy establish a connection between a label and a related widget. It provides a quick keyboard shorcut to focus its partner widget. (Buddy is a terminology used in PyQt).

*create_shortcut_to_button* creates a shorcut to invoke a button.

I bind to toplevel containing the widget. This way, when the dialog is closed all the bindings disappear.

All shorcuts are of this form: Alt + letter

Buddies and shorcuts enriches the user experience providing new ways to navigate and interact quickly with the application.