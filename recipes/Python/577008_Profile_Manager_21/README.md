## Profile Manager 2.1  
Originally published: 2010-01-15 18:11:28  
Last updated: 2010-01-15 18:11:28  
Author: Stephen Chappell  
  
This is a demonstration of the "cmd.Cmd" class in Python. The recipe demonstrates limited model-view-controller design. The "Profile_Manager" class acts as the model, the "Interface" class is the view, and the basic "cmd.Cmd" class takes the role of controller. It is the "Interface" that handles the boundary between the application's user and the logic of the program. On the other hand, the "Profile_Manager" sits in the place between the interface and the file system (the database holding the data). It is the part that takes care of all the implemented program logic.