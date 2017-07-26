###Pagination widget in Tkinter

Originally published: 2016-11-20 11:54:55
Last updated: 2017-05-01 20:34:49
Author: Miguel Martínez López

I added here a pagination widget in tkinter with different styles.\n\nWhen this option *"hide_controls_at_edge"* is true, the widget hides *"next"*, *"previous"*, *"last"* and *"first"* buttons when they are not necessary. For example when pagination is at the first page then the buttons *"previous"* and *"first"* are not strictly necessary. Analogously when pagination is at the last page, the buttons *"last"* and *"next"* are not necessary because its not possible to go more forward.\n\n\nThe user can customize the text of *"next"*, *"previous"*, *"last"* and *"first"* buttons. When some of these options is None, then the corresponding button is not showed: *prev_button*. *next_button*, *first_button*, *last_button*\n\nThe *"command"* option is a callback called every time a page is selected.