## Tkinter treeview like a table or multicolumn listbox  
Originally published: 2017-01-11 18:59:15  
Last updated: 2017-05-02 22:27:48  
Author: Miguel Martínez López  
  
This trick provides use my other recipe:

https://code.activestate.com/recipes/580794-simple-multicolumn-listbox-for-tkinter/

This recipes defines a *Tk_Table:* A table that extends the multicolumn listbox adding row numbers, making the cells editable and adding autoscrollbars.

*Tk_Table*

It has the same options than *Multicolumn_Listbox*, and some extra parameters to configure the new functionality.

Setting the editable keyword to True, makes the widget editable.

If you want stripped rows, pass the stripped_rows with a tuple (or list) of two colors.

If you want row numbers, then pass to *row_numbers* parameter a True value.

These are the extra options for this class:

- entry_background
- entry_foreground
- entry_validatecommand
- entry_selectbackground
- entry_selectborderwidth
- entry_selectforeground
- scrollbar_background
- scrollbar_troughcolor
- rowlabel_anchor
- rowlabel_minwidth
- rowlabel_hoverbackground
- frame_relief
- frame_borderwidth
- frame_background
- row_numbers