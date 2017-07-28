## Tkinter Datepicker (like the jQuery UI datepicker)  
Originally published: 2016-12-04 00:03:21  
Last updated: 2017-06-19 18:22:01  
Author: Miguel Martínez López  
  
It's based on ttkcalendar.py. But the internals are totally changed.I don't use for example the Treeview widget. I added more features also:
 - On mouse over, the day label changes the background
 - The selected day has an outstanding style
 - Added support for many hotkeys

These are the default bindings:

- *Click button 1 on entry:* Show calendar

- *Click button 1 outside entry and calendar:* Hide calendar

- *Escape:* Hide calendar

- *CTRL + PAGE UP:* Move to the previous month.

- *CTRL + PAGE DOWN:* Move to the next month.

- *CTRL + SHIFT + PAGE UP:* Move to the previous year.

- *CTRL + SHIFT + PAGE DOWN:* Move to the next year.

- *CTRL + LEFT:* Move to the previous day.

- *CTRL + RIGHT:* Move to the next day.

- *CTRL + UP:* Move to the previous week.

- *CTRL + DOWN:* Move to the next week.

- *CTRL + END:* Close the datepicker and erase the date.

- *CTRL + HOME:* Move to the current month.

- *CTRL + SPACE:* Show date on calendar
        
- *CTRL + Return:* Set current selection to entry