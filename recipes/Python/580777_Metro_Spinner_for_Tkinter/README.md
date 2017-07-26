## Metro Spinner for Tkinter  
Originally published: 2017-04-09 22:01:20  
Last updated: 2017-04-10 21:14:36  
Author: Miguel Martínez López  
  
I create a rotating image class *RotatingIcon* inspired and based on this code:

http://stackoverflow.com/questions/15736530/python-tkinter-rotate-image-animation

Features:
   - Methods to stop and start the animation
   - The animation automically stops when the window is not mapped, and the animation continues when the window is mapped again
   - Time setting to control the speed of the animation
   - All the formats accepted for PIL could be used. XBM format is automatically converted to Tk Bitmap. The advantage of Bitmats is the possibility to change the color of the foreground.

I added 6 different styles of spinners with different sizes.

I used fontawesome.io for the icon generation.

For more metro widgets see here:

https://code.activestate.com/recipes/580729-metro-ui-tkinter/
