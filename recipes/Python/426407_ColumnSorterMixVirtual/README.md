## ColumnSorterMixin with a Virtual wx.ListCtrl  
Originally published: 2005-06-22 14:01:53  
Last updated: 2006-08-02 13:07:53  
Author: Egor Zindy  
  
This recipe shows a way of using ColumnSorterMixin with virtual lists (wx.ListCtrl defined with the wx.LC_VIRTUAL flag). The sample code pretty much follows the wx.listctrl demo (provided with wxPython). The interesting bit is the TestVirtualList class and the musicdata dictionary (altogether lines 42 to 257). Remainder is provided to run the TestVirtualList class (or others from the wxdemo) standalone.

The idea is to combine an itemDataMap dictionary with an index table which defines the order in which the dictionary items are displayed. The actual display is handled by the virtual list using only the OnGetItemText, OnGetItemImage and OnGetItemAttr methods.

First of all, the 3 methods OnGetItemText OnGetItemImage and OnGetItemAttr must be declared. Following the ListCtrl demo and in addition to the self.itemDataMap dictionary, a self.itemIndexMap table defines the items order.

ColumnSorterMixin uses the SortItems, GetListrCtrl and GetSortImages  methods which are redefined here.
GetListCtrl now returns self (to keep the mixin happy). GetSortImages is pretty much the same as in the ListCtrl demo, only it uses the art provider (needs better looking arrows, maybe). SortItems handles the sorting. It gets the column clicked from the mixin _col variable and the sorting order (ascending or descending) from the _colSortFlag table.