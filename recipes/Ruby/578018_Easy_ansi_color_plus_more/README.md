## Easy ansi color plus more. 
Originally published: 2012-01-18 06:57:50 
Last updated: 2014-04-16 15:36:04 
Author: Mike 'Fuzzy' Partin 
 
This quick class extends the base String class to add the ability to chain escape codes onto your output. For instance: puts 'String'.bold.underline.blink.red for something truly hideous. Aside from the colors (all are supported, but I haven't put in support for background colors as of the time of this post), cursor placement (ymmv based on the term type), screen clearing, bold, underline, blink reverse, conceal are all handled as well.