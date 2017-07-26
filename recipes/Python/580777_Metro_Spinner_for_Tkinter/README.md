## Metro Spinner for Tkinter

Originally published: 2017-04-09 22:01:20
Last updated: 2017-04-10 21:14:36
Author: Miguel Martínez López

I create a rotating image class *RotatingIcon* inspired and based on this code:\n\nhttp://stackoverflow.com/questions/15736530/python-tkinter-rotate-image-animation\n\nFeatures:\n   - Methods to stop and start the animation\n   - The animation automically stops when the window is not mapped, and the animation continues when the window is mapped again\n   - Time setting to control the speed of the animation\n   - All the formats accepted for PIL could be used. XBM format is automatically converted to Tk Bitmap. The advantage of Bitmats is the possibility to change the color of the foreground.\n\nI added 6 different styles of spinners with different sizes.\n\nI used fontawesome.io for the icon generation.\n\nFor more metro widgets see here:\n\nhttps://code.activestate.com/recipes/580729-metro-ui-tkinter/\n