## tkMath, convert between pixels, inches, cm and mm  
Originally published: 2008-03-30 08:27:56  
Last updated: 2008-04-12 02:25:41  
Author: Ronald Longo  
  
If you're writing some Tkinter software and you're sizing something in inches or centimeters and tkinter only gives you feedback in pixel distances then you may need a way to get back to your prefered units of measure.  I recently found myself in this situation.  There's nothing fancy about the set of functions here, it's more about the little known winfo_fpixels() function.  Once you know about this everything else is a piece of cake.  These functions are simple, but convenient.