## Using wxPython with Twisted Python 
Originally published: 2003-02-21 02:38:30 
Last updated: 2003-02-21 02:38:30 
Author: Uwe C. Schroeder 
 
When using wxPython with Twisted in the way described in the Twisted docs wxPython will be stuck on menus and modal dialogs. This is due to the fact that wxPython uses private eventloops for menus and modal dialogs. You can't run Twisted cleanly in a thread (meaning without modification) and though using wxPython in a thread is possible, it's often not a viable option. Best would be to write a threaded wxreactor for Twisted which is a major project due to the internal nature of wx - using whatever GUI toolkit is available on the target platform.\nThis recipe is simple and works nicely on platforms using the select reactor (linux and windows).