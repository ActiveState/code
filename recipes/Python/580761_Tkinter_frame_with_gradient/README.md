## Tkinter frame with gradient  
Originally published: 2017-03-11 02:22:08  
Last updated: 2017-03-11 03:43:56  
Author: Miguel Martínez López  
  
Frame with linear gradient using PIL. 

It's also possible to make the same trick using tkinter PhotoImage.

http://stackoverflow.com/questions/10417524/why-is-photoimage-put-slow

But PIL is more efficient:

https://groups.google.com/forum/#!topic/comp.lang.python/nQ6YO-dTz10

Possible values for **orient** are: *VERTICAL*, *HORIZONTAL*. If **orient** is "vertical", then width is mandatory. If **orient** is "horizontal", then height is mandatory. If **steps** is *None*, then the gradient is composed of adjacent lines.

One possible practical application of gradient frames are tool bars. Gradient guives a visual clue of when an area starts and when an area finish. 