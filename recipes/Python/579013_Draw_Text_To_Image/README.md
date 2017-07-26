## Draw Text To Image  
Originally published: 2015-01-25 09:05:15  
Last updated: 2015-07-13 18:04:30  
Author: FB36   
  
PIL does not allow resizing default bitmap font.\nThis code resizes it by itself.\n\nThe disadvantage is slow speed but the advantage is it becomes possible to set color of each pixel of text foreground and background.\n\nAs an example I set foreground to reverse colors and background to grayscale.