## unset engine in gtkrc; unset widget style in gtk  
Originally published: 2009-07-13 06:51:51  
Last updated: 2009-07-13 06:51:51  
Author: Dima Tisnek  
  
Example shows how to unset gtk engine'd look for a particular widget.\n\ngtk.Widget.modify_xx allows you to override simple properties, like backgrounds (unless theme uses an engine) and text color (sometimes (?))\ngtkrc allows you to override most properties for all or selected widgets, like sizes, faces, and so on.\nsome parts of widget appearance are set through engine stanzas in gtkrc, these can be unset too, if you know how...\n\nhere it is!