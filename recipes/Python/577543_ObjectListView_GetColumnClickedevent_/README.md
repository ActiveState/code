###ObjectListView GetColumnClicked(event) # handler

Originally published: 2011-01-14 04:41:34
Last updated: 2011-01-14 04:41:35
Author: Dev Player

ObjectListView is a 3rd party wxPython 2.8+ module that adds a more object-friendly API to the wx.ListCtrl(). When clicking on an item in the list it's easy to process mouse click events or item selection events. However some OS platforms do not set all the event's attributes. Also the various HitTest() methods currently on various platforms are not implemented the same. So here is a little recipe to get the column number (first column equals zero) when left clicking and item in the ObjectListView with the mouse.