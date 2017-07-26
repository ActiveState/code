## IronPython fade-in windowOriginally published: 2004-09-02 01:58:08 
Last updated: 2004-09-02 01:58:08 
Author: Brian Quinlan 
 
This recipe describes how to create a fade-in window using IronPython. Several applications use fade-in windows for temporary data e.g. new Outlook XP mail messages are shown through a fade-in/fade-out pop-up window.\n\nFading in can be best accomplished using the Form.Opacity property and a Timer. Pop-up windows should also set the "topmost" window style.