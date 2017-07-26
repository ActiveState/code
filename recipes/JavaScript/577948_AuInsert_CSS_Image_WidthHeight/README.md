## Auto Insert CSS Image Width/Height Macro:  
Originally published: 2011-11-16 15:23:03  
Last updated: 2011-11-16 15:23:03  
Author: Skye Giordano  
  
Based on the macro at http://community.activestate.com/forum/html-editing-img-tag-expansion-etc I hacked together this alternate version that will auto insert the width: and height: of an image background in a CSS rule turning this:

background: url(http://server.com/myImg.jpg) 0 0 no-repeat;

...into this:

background: url(http://server.com/myImg.jpg) 0 0 no-repeat;
height: 252px;
width: 200px;