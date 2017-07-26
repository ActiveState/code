# Version: 2.3
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))


import platform

try:
    from Tkinter import Frame, BOTH ,N,E,S, W, CENTER, Entry, Canvas, Label
    from tkFont import Font, nametofont
    from ttk import Treeview, Scrollbar, Style
except ImportError:
    from tkinter import Frame, BOTH ,N,E,S, W, CENTER, Entry, Canvas, Label
    from tkinter.font import Font, nametofont
    from tkinter.ttk import Treeview, Scrollbar, Style

# Python 3 compatibility
try:
  basestring
except NameError:
  basestring = str

class Row(object):
    def __init__(self, table, index):
        self._multicolumn_listbox = table
        self._index = index

    def data(self):
        return self._multicolumn_listbox.row_data(self._index)

    def delete(self):
        self._multicolumn_listbox.delete_row(self._index)

    def update(self, data):
        self._multicolumn_listbox.update_row(self._index, data)

    def select(self):
        self._multicolumn_listbox.select_row(self._index)

    def deselect(self):
        self._multicolumn_listbox.deselect_row(self._index)
    
    def __str__(self):
        return str(self.data())
        
    def __len__(self):
        return self._multicolumn_listbox.number_of_columns
    
class Column(object):
    def __init__(self, table, index):
        self._multicolumn_listbox = table
        self._index = index
    
    def data(self):
        return self._multicolumn_listbox.column_data(self._index)

    def delete(self):
        self._multicolumn_listbox.delete_column(self._index)

    def update(self, data):
        self._multicolumn_listbox.update_column(self._index, data)

    def __str__(self):
        return str(self.data())
        
    def __len__(self):
        return self._multicolumn_listbox.number_of_rows
    
class Multicolumn_Listbox(object):
    _style_index = 0

    class List_Of_Rows(object):
        def __init__(self, multicolumn_listbox):
            self._multicolumn_listbox = multicolumn_listbox

        def data(self, index):
            return self._multicolumn_listbox.row_data(index)
            
        def get(self, index):
            return Row(self._multicolumn_listbox, index)

        def insert(self, data, index=None):
            self._multicolumn_listbox.insert_row(data, index)

        def delete(self, index):
            self._multicolumn_listbox.delete_row(index)

        def update(self, index, data):
            self._multicolumn_listbox.update_row(index, data)

        def select(self, index):
            self._multicolumn_listbox.select_row(index)

        def deselect(self, index):
            self._multicolumn_listbox.deselect_row(index)

        def set_selection(self, indices):
            self._multicolumn_listbox.set_selection(indices)

        def __getitem__(self, index): 
            return self.get(index)

        def __setitem__(self, index, value): 
            return self._multicolumn_listbox.update_row(index, value)

        def __delitem__(self, index): 
            self._multicolumn_listbox.delete_row(index)

        def __len__(self): 
            return self._multicolumn_listbox.number_of_rows

    class List_Of_Columns(object):
        def __init__(self, multicolumn_listbox):
            self._multicolumn_listbox = multicolumn_listbox
        
        def data(self, index):
            return self._multicolumn_listbox.get_column(index)

        def get(self, index):
            return Column(self._multicolumn_listbox, index)

        def delete(self, index):
            self._multicolumn_listbox.delete_column(index)

        def update(self, index, data):
            self._multicolumn_listbox.update_column(index, data)

        def __getitem__(self, index): 
            return self.get(index)

        def __setitem__(self, index, value): 
            return self._multicolumn_listbox.update_column(index, value)

        def __delitem__(self, index): 
            self._multicolumn_listbox.delete_column(index)

        def __len__(self): 
            return self._multicolumn_listbox.number_of_columns

    def __init__(self, master, columns, data=None, command=None, sort=True, select_mode=None, heading_anchor = CENTER, cell_anchor=W, style=None, height=None, padding=None, adjust_heading_to_content=False, stripped_rows=None, selection_background=None, selection_foreground=None, field_background=None, heading_font= None, heading_background=None, heading_foreground=None, cell_pady=2, cell_background=None, cell_foreground=None, cell_font=None, headers=True):

        self._stripped_rows = stripped_rows

        self._columns = columns
        
        self._number_of_rows = 0
        self._number_of_columns = len(columns)
        
        self.row = self.List_Of_Rows(self)
        self.column = self.List_Of_Columns(self)
        
        s = Style()

        if style is None:
            style_name = "Multicolumn_Listbox%s.Treeview"%self._style_index
            self._style_index += 1
        else:
            style_name = style
        
        style_map = {}
        if selection_background is not None:
            style_map["background"] = [('selected', selection_background)]
            
        if selection_foreground is not None:
            style_map["foeground"] = [('selected', selection_foreground)]

        if style_map:
            s.map(style_name, **style_map)

        style_config = {}
        if cell_background is not None:
            style_config["background"] = cell_background

        if cell_foreground is not None:
            style_config["foreground"] = cell_foreground

        if cell_font is None:
            font_name = s.lookup(style_name, "font")
            cell_font = nametofont(font_name)
        else:
            if not isinstance(cell_font, Font):
                if isinstance(cell_font, basestring):
                    cell_font = nametofont(cell_font)
                else:
                    if len(font) == 1:
                        cell_font = Font(family=cell_font[0])
                    elif len(font) == 2:
                        cell_font = Font(family=cell_font[0], size=cell_font[1])
                        
                    elif len(font) == 3:
                        cell_font = Font(family=cell_font[0], size=cell_font[1], weight=cell_font[2])
                    else:
                        raise ValueError("Not possible more than 3 values for font")
        
            style_config["font"] = cell_font
        
        self._cell_font = cell_font

        self._rowheight = cell_font.metrics("linespace")+cell_pady
        style_config["rowheight"]=self._rowheight

        if field_background is not None:
            style_config["fieldbackground"] = field_background

        s.configure(style_name, **style_config)

        heading_style_config = {}
        if heading_font is not None:
            heading_style_config["font"] = heading_font
        if heading_background is not None:
            heading_style_config["background"] = heading_background
        if heading_foreground is not None:
            heading_style_config["foreground"] = heading_foreground

        heading_style_name = style_name + ".Heading"
        s.configure(heading_style_name, **heading_style_config)

        treeview_kwargs = {"style": style_name}

        if height is not None:
            treeview_kwargs["height"] = height
            
        if padding is not None:
            treeview_kwargs["padding"] = padding
            
        if headers:
            treeview_kwargs["show"] = "headings"
        else:
            treeview_kwargs["show"] = ""
        
        if select_mode is not None:
            treeview_kwargs["selectmode"] = select_mode

        self.interior = Treeview(master, columns=columns, **treeview_kwargs)
        
        if command is not None:
            self._command = command
            self.interior.bind("<<TreeviewSelect>>", self._on_select)

        for i in range(0, self._number_of_columns):

            if sort:
                self.interior.heading(i, text=columns[i], anchor=heading_anchor, command=lambda col=i: self.sort_by(col, descending=False))
            else:
                self.interior.heading(i, text=columns[i], anchor=heading_anchor)
                
            if adjust_heading_to_content:
                self.interior.column(i, width=Font().measure(columns[i]))

            self.interior.column(i, anchor=cell_anchor)
            
        if data is not None:
            for row in data:
                self.insert_row(row)

    @property
    def row_height(self):
        return self._rowheight
        
    @property
    def font(self):
        return self._cell_font

    def configure_column(self, index, width=None, minwidth=None, anchor=None, stretch=None):
        kwargs = {}
        for config_name in ("width", "anchor", "stretch", "minwidth"):
            config_value = locals()[config_name]
            if config_value is not None:
                kwargs[config_name] = config_value
            
        self.interior.column('#%s'%(index+1), **kwargs)

    def row_data(self, index):
        try:
            item_ID = self.interior.get_children()[index]
        except IndexError:
            raise ValueError("Row index out of range: %d"%index)        

        return self.item_ID_to_row_data(item_ID)

    def update_row(self, index, data):
        try:
            item_ID = self.interior.get_children()[index]
        except IndexError:
            raise ValueError("Row index out of range: %d"%index)
            
        if len(data) == len(self._columns):
            self.interior.item(item_ID, values=data)
        else:
            raise ValueError("The multicolumn listbox has only %d columns"%self._number_of_columns)

    def delete_row(self, index):
        list_of_items = self.interior.get_children()

        try:
            item_ID = list_of_items[index]
        except IndexError:
            raise ValueError("Row index out of range: %d"%index)

        self.interior.delete(item_ID)
        self._number_of_rows -= 1
        
        if self._stripped_rows:
            for i in range(index, self._number_of_rows):
                self.interior.tag_configure(list_of_items[i+1], background=self._stripped_rows[i%2])
            
    def insert_row(self, data, index=None):
        if len(data) != self._number_of_columns:
            raise ValueError("The multicolumn listbox has only %d columns"%self._number_of_columns)
        
        if index is None:
            index = self._number_of_rows-1

        item_ID = self.interior.insert('', index, values=data)        
        self.interior.item(item_ID, tags=item_ID)

        self._number_of_rows += 1        

        if self._stripped_rows:            
            list_of_items = self.interior.get_children()

            self.interior.tag_configure(item_ID, background=self._stripped_rows[index%2])

            for i in range(index+1, self._number_of_rows):
                self.interior.tag_configure(list_of_items[i], background=self._stripped_rows[i%2])

    def column_data(self, index):
        return [self.interior.set(child_ID, index) for child_ID in self.interior.get_children('')]

    def update_column(self, index, data):
        for i, item_ID in enumerate(self.interior.get_children()): 
            data_row = self.item_ID_to_row_data(item_ID)
            data_row[index] = data[i]

            self.interior.item(item_ID, values=data_row)

        return data

    def clear(self):
        # Another possibility:
        #  self.interior.delete(*self.interior.get_children())

        for row in self.interior.get_children():
            self.interior.delete(row)
            
        self._number_of_rows = 0
            
    def update(self, data):
        self.clear()

        for row in data:
            self.insert_row(row)
            
    def focus(self, index=None):
        if index is None:
            return self.interior.item(self.interior.focus())
        else:
            item = self.interior.get_children()[index]
            self.interior.focus(item)

    def state(self, state=None):
        if stateSpec is None:
            return self.interior.state()
        else:
            self.interior.state(state)

    @property
    def number_of_rows(self):
        return self._number_of_rows
        
    @property
    def number_of_columns(self):
        return self._number_of_columns
        
    def toogle_selection(self, index):
        list_of_items = self.interior.get_children()
        
        try:
            item_ID = list_of_items[index]
        except IndexError:
            raise ValueError("Row index out of range: %d"%index)

        self.interior.selection_toggle(item_ID)     

    def select_row(self, index):
        list_of_items = self.interior.get_children()
        
        try:
            item_ID = list_of_items[index]
        except IndexError:
            raise ValueError("Row index out of range: %d"%index)

        self.interior.selection_add(item_ID)

    def deselect_row(self, index):
        list_of_items = self.interior.get_children()
        
        try:
            item_ID = list_of_items[index]
        except IndexError:
            raise ValueError("Row index out of range: %d"%index)

        self.interior.selection_remove(item_ID)
        
    def deselect_all(self):
        self.interior.selection_remove(self.interior.selection())

    def set_selection(self, indices):
        list_of_items = self.interior.get_children()

        self.interior.selection_set(" ".join(list_of_items[row_index] for row_index in indices))

    @property
    def selected_rows(self):
        data = []
        for item_ID in self.interior.selection():
            data_row = self.item_ID_to_row_data(item_ID)
            data.append(data_row)
        
        return data

    @property
    def indices_of_selected_rows(self):
        list_of_indices = []
        for index, item_ID in enumerate(self.interior.get_children()):
            if item_ID in self.interior.selection():
                list_of_indices.append(index)

        return list_of_indices
        
    def delete_all_selected_rows(self):
        selected_items = self.interior.selection()
        for item_ID in selected_items:
            self.interior.delete(item_ID)
        
        number_of_deleted_rows = len(selected_items)
        self._number_of_rows -= number_of_deleted_rows

        return number_of_deleted_rows

    def _on_select(self, event):
        for item_ID in event.widget.selection():
            data_row = self.item_ID_to_row_data(item_ID)
            self._command(data_row)

    def item_ID_to_row_data(self, item_ID):
        item = self.interior.item(item_ID)
        return item["values"]
    
    @property
    def table_data(self):
        data = []

        for item_ID in self.interior.get_children():
            data_row = self.item_ID_to_row_data(item_ID)
            data.append(data_row)

        return data
    
    @table_data.setter
    def table_data(self, data):
        self.update(data)
    
    def cell_data(self, row, column):
        """Get the value of a table cell"""
        try:
            item = self.interior.get_children()[row]
        except IndexError:
            raise ValueError("Row index out of range: %d"%row)
            
        return self.interior.set(item, column)
            
    def update_cell(self, row, column, value):
        """Set the value of a table cell"""

        item_ID = self.interior.get_children()[row]
        
        data = self.item_ID_to_row_data(item_ID)
        
        data[column] = value
        self.interior.item(item_ID, values=data)
    
    def __getitem__(self, index):
        if isinstance(index, tuple):
            row, column = index
            return self.cell_data(row, column)
        else:
            raise Exception("Row and column indices are required")
        
    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            row, column = index
            self.update_cell(row, column, value)
        else:
            raise Exception("Row and column indices are required")

    def bind(self, event, handler):
        self.interior.bind(event, handler)

    def sort_by(self, col, descending):
        """
        sort tree contents when a column header is clicked
        """
        # grab values to sort
        data = [(self.interior.set(child_ID, col), child_ID) for child_ID in self.interior.get_children('')]
        
        # if the data to be sorted is numeric change to float
        try:
            data = [(float(number), child_ID) for number, child_ID in data]
        except ValueError:
            pass

        # now sort the data in place
        data.sort(reverse=descending)
        for idx, item in enumerate(data):
            self.interior.move(item[1], '', idx)

        # switch the heading so that it will sort in the opposite direction
        self.interior.heading(col, command=lambda col=col: self.sort_by(col, not descending))
        
        if self._stripped_rows:
            list_of_items = self.interior.get_children('')
            for i in range(len(list_of_items)):
                self.interior.tag_configure(list_of_items[i], background=self._stripped_rows[i%2])

    def destroy(self):
        self.interior.destroy()
        
    def item_ID(self, index):
        return self.interior.get_children()[index]

################################################
# The next code is only for Tk_Table class
#
#

OS = platform.system()

def bind_function_onMouseWheel(scrolled_widget, orient, binding_widget=None, callback=None, factor = 1, unit="units"):
    if not scrolled_widget:
        binding_widget = scrolled_widget

    view_command = getattr(scrolled_widget, orient+'view')
    
    if OS == 'Linux':
        if callback:
            def onMouseWheel(event):
                if event.num == 4:
                    view_command("scroll",(-1)*factor, unit)
                elif event.num == 5:
                    view_command("scroll",factor, unit) 
                
                callback()
        else:
            def onMouseWheel(event):
                if event.num == 4:
                    view_command("scroll",(-1)*factor, unit)
                elif event.num == 5:
                    view_command("scroll",factor, unit) 

    elif OS == 'Windows':
        if callback:
            def onMouseWheel(event):        
                view_command("scroll",(-1)*int((event.delta/120)*factor), unit)
                callback()
        else:
            def onMouseWheel(event):        
                view_command("scroll",(-1)*int((event.delta/120)*factor), unit)
    
    elif OS == 'Darwin':
        if callback:
            def onMouseWheel(event):        
                view_command("scroll",event.delta, unit)
                callback()
        else:
            def onMouseWheel(event):        
                view_command("scroll",event.delta, unit)

    if OS == "Linux" :
        binding_widget.bind('<4>', onMouseWheel, add='+')
        binding_widget.bind('<5>', onMouseWheel, add='+')
    else:
        # Windows and MacOS
        binding_widget.bind("<MouseWheel>", onMouseWheel,  add='+')

def unbind_function_onMouseWheel(binding_widget):
    if OS == "Linux" :    
        binding_widget.unbind('<4>')
        binding_widget.unbind('<5>')
    else:
        binding_widget.unbind('<MouseWheel>')

class Row_Header(Canvas):
    def __init__(self, master, font, row_height, row_minwidth, hover_background=None, background=None, anchor=None, onclick=None):
        Canvas.__init__(self, master, bd=0, highlightthickness=0, yscrollincrement=row_height, width=0)
        
        if background is not None:
            self.configure(background=background)

        self._frame_of_row_numbers = Frame(self, bd=0)

        self.create_window(0, 0, window=self._frame_of_row_numbers, anchor=N+W)
        self._width_of_row_numbers = 0

        self._labelrow_kwargs = labelrow_kwargs= {}

        labelrow_kwargs["font"] = font
        
        if anchor is not None:
            labelrow_kwargs["anchor"] = anchor

        self._row_minwidth= row_minwidth
        self._row_height = row_height
        self._hover_background = hover_background
        self._onclick = onclick
        
        self._number_of_labels = 0

    def pop(self, n_labels=1):
        if self._number_of_labels == 0:
            return

        list_of_slaves = self._frame_of_row_numbers.pack_slaves()
        
        for i in range(n_labels):
            list_of_slaves.pop().destroy()
        
        if list_of_slaves:
            width_of_row_numbers= max(list_of_slaves[-1].winfo_reqwidth(), self._row_minwidth)
            
            if width_of_row_numbers < self._width_of_row_numbers:
                self._width_of_row_numbers = width_of_row_numbers
                
                for slave in self._frame_of_row_numbers.pack_slaves():
                    slave.configure(width=width_of_row_numbers)

        self.config(width=self._frame_of_row_numbers.winfo_reqwidth())
        self.config(scrollregion=(0, 0, self._frame_of_row_numbers.winfo_reqwidth(), len(list_of_slaves)*self._row_height))

        self._number_of_labels -= n_labels

    def delete_labels(self):
        if self._number_of_labels == 0:
            return

        for slave in self._frame_of_row_numbers.pack_slaves():
            slave.destroy()
        
        self._number_of_labels = 0

    def new_label(self):
        # Creating a new row header
        
        self._number_of_labels += 1

        frame_button = Frame(self._frame_of_row_numbers, height=self._row_height)
        frame_button.pack()
        frame_button.pack_propagate(False)
        
        row_label = Label(frame_button, text =self._number_of_labels, **self._labelrow_kwargs)
        row_label.bind("<1>", lambda event, index=self._number_of_labels-1: self._on_click_label(index))
        
        if self._hover_background:
            row_label.bind("<Enter>", lambda event, row_label=row_label: row_label.configure(background=self._hover_background))
            row_label.bind("<Leave>", lambda event, row_label=row_label: row_label.configure(background=self.cget("background")))

        row_label.pack(expand=True, fill=BOTH)
        
        width_of_row_numbers= max(row_label.winfo_reqwidth(), self._row_minwidth)
        
        if width_of_row_numbers > self._width_of_row_numbers:
            self._width_of_row_numbers = width_of_row_numbers
            
            for slave in self._frame_of_row_numbers.pack_slaves():
                slave.configure(width=width_of_row_numbers)
        else:
            frame_button.configure(width=width_of_row_numbers)

        frame_button.update_idletasks()

        self.config(width=self._frame_of_row_numbers.winfo_reqwidth())
        self.config(scrollregion=(0, 0, self._frame_of_row_numbers.winfo_reqwidth(), self._number_of_labels*self._row_height))

    def _on_click_label(self, index):            
        if self._onclick:
            self._onclick(index)

class Tk_Table(Frame, object):
    def __init__(self, master, columns, data=None, command=None, editable=True, sort=True, select_mode=None, autoscroll=True, vscrollbar=True, hscrollbar=False, heading_anchor = CENTER, cell_anchor=W, style=None, scrollbar_background=None, scrollbar_troughcolor=None, height=None, padding=None, adjust_heading_to_content=False, stripped_rows=None, selection_background=None, selection_foreground=None, cell_background=None, cell_foreground=None, cell_font=None, field_background=None, heading_font= None, heading_background=None, heading_foreground=None, cell_pady=2, column_header=True, row_numbers=True, entry_background="#d6d6d6", entry_foreground=None, entry_validatecommand=None, entry_selectbackground="#1BA1E2", entry_selectborderwidth=None, entry_selectforeground=None, entry_font = "TkDefaultFont", rowlabel_anchor=E, rowlabel_minwidth=0, rowlabel_hoverbackground="#FFFFFF",frame_relief=None, frame_borderwidth=None, frame_background=None):

        frame_kwargs = {}
        
        if frame_relief is not None:
            frame_kwargs["relief"] = frame_relief
            
        if frame_borderwidth is not None:
            frame_kwargs["borderwidth"] = frame_borderwidth

        if frame_background is not None:
            frame_kwargs["background"] = frame_background

        Frame.__init__(self, master, class_="Multicolumn_Listbox", **frame_kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._multicolumn_listbox = Multicolumn_Listbox(self, columns, data=data, command=command, sort=sort, select_mode=select_mode, heading_anchor = heading_anchor, cell_anchor=cell_anchor, style=style, height=height, padding=padding, adjust_heading_to_content=adjust_heading_to_content, stripped_rows=stripped_rows, selection_background=selection_background, selection_foreground=selection_foreground, cell_background=cell_background, cell_foreground=cell_foreground, cell_font=cell_font, field_background=field_background, heading_font=heading_font, heading_background=heading_background, heading_foreground=heading_foreground, cell_pady=cell_pady, headers=column_header)
        self._multicolumn_listbox.interior.grid(row=0, column=1, sticky= N+E+W+S)
        
        self._mousewheel_detection = True

        if row_numbers:
            self._row_numbers = Row_Header(self, font=self._multicolumn_listbox.font, row_height=self._multicolumn_listbox.row_height, row_minwidth=rowlabel_minwidth, hover_background = rowlabel_hoverbackground, anchor=rowlabel_anchor, onclick=self._on_click_row_label)
            self._row_numbers.grid(row=0, column=0, sticky= N+S+E)

            self._multicolumn_listbox.interior.bind("<Map>", self._place_vertically_row_numbers)
        else:
            self._row_numbers = None

        if editable:
            self._selected_cell = None
            self._entry_popup = None

            self._multicolumn_listbox.interior.bind("<1>", self._edit_cell)
            
            def configure(event):
                """
                if self._entry_popup:
                    self._entry_popup.destroy()
                return
                """

                self._multicolumn_listbox.interior.update_idletasks()
                self._update_position_of_entry()

            self._multicolumn_listbox.interior.bind("<Configure>", configure)

            self._entry_kwargs = entry_kwargs = {}
            if entry_background is not None:
                entry_kwargs["background"] = entry_background

            if entry_foreground is not None:
                entry_kwargs["foreground"] = entry_foreground
                
            if entry_validatecommand is not None:
                entry_kwargs["validatecommand"] = entry_validatecommand
                
            if entry_selectbackground is not None:
                entry_kwargs["selectbackground"] = entry_selectbackground
                
            if entry_selectforeground is not None:
                entry_kwargs["selectforeground"] = entry_selectforeground
                
            if entry_font is not None:
                entry_kwargs["font"] = entry_font

        if command is not None:
            self._command = command
            self._multicolumn_listbox.interior.bind("<<TreeviewSelect>>", self._on_select)
            
        scrollbar_kwargs = {}
        if scrollbar_background is not None:
            scrollbar_kwargs["background"] = scrollbar_background
            
        if scrollbar_troughcolor is not None:
            scrollbar_kwargs["throughcolor"] = scrollbar_troughcolor

        if vscrollbar:
            if editable:
                if row_numbers:
                    def yview_command(*args):
                        
                        self._multicolumn_listbox.interior.yview(*args)
                        self._row_numbers.yview(*args)

                        self._update_position_of_entry()
                else:
                    def yview_command(*args):
                        self._multicolumn_listbox.interior.yview(*args)
                        self._update_position_of_entry()
            else:
                if row_numbers:
                    def yview_command(*args):
                        self._multicolumn_listbox.interior.yview(*args)
                        self._row_numbers.yview(*args)
                else:
                    yview_command = self._multicolumn_listbox.interior.yview

            self._vbar=Scrollbar(self,takefocus=0, command=yview_command, **scrollbar_kwargs)
            self._vbar.grid(row=0, column=2, sticky= N+S)

            def yscrollcommand(first,last):
                first, last = float(first), float(last)
                if first <= 0 and last >= 1:
                    if self._mousewheel_detection:
                        if autoscroll:
                            self._vbar.grid_remove()

                        if row_numbers:
                            unbind_function_onMouseWheel(self._multicolumn_listbox.interior)
                        self._mousewheel_detection = False
                else:
                    if not self._mousewheel_detection:
                        if autoscroll:
                            self._vbar.grid()

                        if row_numbers:
                            bind_function_onMouseWheel(self._row_numbers, "y", binding_widget=self._multicolumn_listbox.interior, unit="pages")
                        self._mousewheel_detection = True

                self._vbar.set(first, last)
                if editable:
                    self._update_position_of_entry()

            self._multicolumn_listbox.interior.config(yscrollcommand=yscrollcommand)

        if hscrollbar:
            if editable:
                def xview_command(*args):
                    self._multicolumn_listbox.interior.xview(*args)
                    self._update_position_of_entry()
            else:
                xview_command = self._multicolumn_listbox.interior.xview

            self._hbar=Scrollbar(self,takefocus=0, command=xview_command, **scrollbar_kwargs)
            self._hbar.grid(row=1, column=1, sticky= E+W)
            
            if autoscroll:
                if editable:
                    def xscrollcommand(f,l, self=self):
                        make_autoscroll(self._hbar, f, l)
                        self._update_position_of_entry()
                else:
                    def xscrollcommand(f,l, hbar=self._hbar):
                        make_autoscroll(hbar, f, l)

                self._multicolumn_listbox.interior.config(xscrollcommand=xscrollcommand)
            else:
                self._multicolumn_listbox.interior.config(xscrollcommand=self._hbar.set)

    def _place_vertically_row_numbers(self, event):
        self._multicolumn_listbox.interior.unbind("<Map>")

        item_ID = self._multicolumn_listbox.interior.insert('', 0, values=[""]*self._multicolumn_listbox.number_of_columns)
        self._multicolumn_listbox.interior.update()
        x,y,w,h = self._multicolumn_listbox.interior.bbox(item_ID)
        self._multicolumn_listbox.interior.delete(item_ID)

        self._row_numbers.grid_configure(pady=(y,0))

    def _edit_cell(self, event):
        '''Executed, when a row is clicked. Opens an entry popup above the cell, so it is possible
        to select text '''

        # close previous popups
        if self._entry_popup:
            self._destroy_entry()

        # what row and column was clicked on
        item_ID = self._multicolumn_listbox.interior.identify_row(event.y)
        if not item_ID: return

        column = self._multicolumn_listbox.interior.identify_column(event.x)

        if column == "": return
        
        # get column position info
        x,y,width,height = self._multicolumn_listbox.interior.bbox(item_ID, column)
       
        # place Entry popup properly
        column_number = int(column[1:])-1
        cell_data = self._multicolumn_listbox.item_ID_to_row_data(item_ID)[column_number]


        self._entry_popup = Entry(self._multicolumn_listbox.interior, exportselection=True, borderwidth=0,  **self._entry_kwargs)
        self._entry_popup.place(x=x, y=y, width=width, height=height)
        
        self._entry_popup.insert(0, cell_data)
        self._entry_popup.focus_force()

        self._entry_popup.bind("<Control-a>", lambda event: self._select_all_entry_data)
        self._entry_popup.bind("<Escape>", lambda event: self._destroy_entry())
        self._entry_popup.bind("<FocusOut>", lambda event: self._destroy_entry())

        bind_function_onMouseWheel(self._multicolumn_listbox.interior, "y", binding_widget=self._entry_popup, callback=self._update_position_of_entry, unit="pages")
        
        if self._row_numbers:
            bind_function_onMouseWheel(self._row_numbers, "y", binding_widget=self._entry_popup, unit="pages")
        
        self._entry_popup.bind("<Return>", self._on_update_cell)
        
        self._selected_cell = item_ID, column, column_number

    def _on_click_row_label(self, index):
        if self._selected_cell and self._multicolumn_listbox.item_ID(index) == self._selected_cell[0]:
            self._destroy_entry()

        self._multicolumn_listbox.toogle_selection(index)

    def _select_all_entry_data(self):
        ''' Set selection on the whole text '''
        self._entry_popup.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'

    def _destroy_entry(self):
        self._entry_popup.destroy()

        self._entry_popup = None
        self._selected_cell = None

    def _on_update_cell(self, event):
        item_ID, column, column_number = self._selected_cell

        data = self._entry_popup.get()

        row_data = self._multicolumn_listbox.item_ID_to_row_data(item_ID)
        row_data[column_number] = data        
        self._multicolumn_listbox.interior.item(item_ID, values=row_data)
        
        self._destroy_entry()
        
    def _update_position_of_entry(self):
        if self._selected_cell:
            bbox = self._multicolumn_listbox.interior.bbox(self._selected_cell[0], self._selected_cell[1])
            if bbox == "":
                self._entry_popup.place_forget()
            else:
                x,y,width,height = bbox
                self._entry_popup.place(x=x, y=y, width=width, height=height)

    def configure_column(self, index, width=None, minwidth=None, anchor=None, stretch=None):
        self._multicolumn_listbox.configure_column(self, index, width=None, minwidth=None, anchor=None, stretch=None)

    def row_data(self, index):
        return self._multicolumn_listbox.row_data(index)

    def update_row(self, index, data):
        self._multicolumn_listbox.update_row(index,data)

    def delete_row(self, index):
        self._multicolumn_listbox.delete_row(index)
        if self._row_numbers:
            self._row_numbers.pop()

    def insert_row(self, data, index=None):
        self._multicolumn_listbox.insert_row(data, index)
        if self._row_numbers:
            self._row_numbers.new_label()

    def column_data(self, index):
        return self._multicolumn_listbox.column_data(index)

    def update_column(self, index, data):
        self._multicolumn_listbox.update_column(index, data)

    def clear(self):
        self._multicolumn_listbox.clear()
        
        if self._row_numbers:
            self._row_numbers.delete_labels()

    def update(self, data):
        current_number_of_rows = self._multicolumn_listbox.number_of_rows
        self._multicolumn_listbox.update(data)
        
        if self._row_numbers:
            number_of_rows = len(data)
            if current_number_of_rows < number_of_rows:
                for i in range(number_of_rows - current_number_of_rows):
                    self._row_numbers.new_label()
            else:
                n_labels = current_number_of_rows - number_of_rows
                self._row_numbers.pop(n_labels =n_labels)

    def focus(self, index=None):
        self._multicolumn_listbox.focus(index)

    def state(self, state=None):
        self._multicolumn_listbox.state(state)

    @property
    def number_of_rows(self):
        return self._multicolumn_listbox.number_of_rows

    @property
    def number_of_columns(self):
        return self._multicolumn_listbox.number_of_columns

    def toogle_selection(self, index):
        self._multicolumn_listbox.toogle_selection(index)

    def select_row(self, index):
        self._multicolumn_listbox.select_row(index)

    def deselect_row(self, index):
        self._multicolumn_listbox.deselect_row(index)

    def deselect_all(self):
        self._multicolumn_listbox.deselect_all()

    def set_selection(self, indices):
        self._multicolumn_listbox.set_selection(indices)

    @property
    def selected_rows(self):
        return self._multicolumn_listbox.selected_rows

    @property
    def indices_of_selected_rows(self):
        return self._multicolumn_listbox.indices_of_selected_rows

    def delete_all_selected_rows(self):
        number_of_deleted_rows = self._multicolumn_listbox.delete_all_selected_rows()

        if self._row_numbers:
            self._row_numbers.pop(n_labels=number_of_deleted_rows)

    @property
    def table_data(self):
        return self._multicolumn_listbox.table_data

    @table_data.setter
    def table_data(self, data):
        self.update(data)

    def cell_data(self, row, column):
        return self._multicolumn_listbox.cell_data(row, column)

    def update_cell(self, row, column, value):
        self._multicolumn_listbox.update_cell(row, column, value)

    def __getitem__(self, index):
        return self._multicolumn_listbox[index]
        
    def __setitem__(self, index, value):
        self._multicolumn_listbox[index] = value

    def bind(self, event, handler):
        self._multicolumn_listbox.bind(event, handler)

    def sort_by(self, col, descending):
        self._multicolumn_listbox.sort_by(col, descending)

if __name__ == '__main__':
    try:
        from Tkinter import Tk
        import tkMessageBox as messagebox
    except ImportError:
        from tkinter import Tk
        from tkinter import messagebox

    root = Tk()
    
    def on_select(data):
        print("called command when row is selected")
        print(data)
        print("\n")
        
    def show_info(msg):
        messagebox.showinfo("Table Data", msg)

    mcListbox = Multicolumn_Listbox(root, ["column one","column two", "column three"], command=on_select, cell_anchor="center")
    mcListbox.interior.pack()
    
    mcListbox.insert_row([1,2,3])
    show_info("mcListbox.insert_row([1,2,3])")
    
    mcListbox.row.insert([4,5,7])
    show_info("mcListbox.row.insert([4,5,7])")

    mcListbox.update_row(0, [7,8,9])
    show_info("mcListbox.update_row(0, [4,5,6])")
    
    mcListbox.update([[1,2,3], [4,5,6]])
    show_info("mcListbox.update([[1,2,3], [4,5,6]])")
    
    mcListbox.select_row(0)
    show_info("mcListbox.select_row(0)")

    print("mcListbox.selected_rows")
    print(mcListbox.selected_rows)
    print("\n")
    
    print("mcListbox.table_data")
    print(mcListbox.table_data)
    print("\n")

    print("mcListbox.row[0]")
    print(mcListbox.row[0])
    print("\n")
    
    print("mcListbox.row_data(0)")
    print(mcListbox.row_data(0))
    print("\n")
    
    print("mcListbox.column[1]")
    print(mcListbox.column[1])
    print("\n")
    
    print("mcListbox[0,1]")
    print(mcListbox[0,1])
    print("\n")

    mcListbox.column[1] = ["item1", "item2"]

    mcListbox.update_column(2, [8,9])
    show_info("mcListbox.update_column(2, [8,9])")
    
    mcListbox.clear()
    show_info("mcListbox.clear()")
    
    mcListbox.table_data = [[1,2,3], [4,5,6], [7,8,9]]
    show_info("mcListbox.table_data = [[1,2,3], [4,5,6], [7,8,9]]")

    mcListbox.delete_row(1)
    show_info("mcListbox.delete_row(1)")
    
    row = mcListbox.row[0].update([2,4,5])
    show_info("mcListbox.row[0].update([2,4,5])")

    mcListbox.destroy()

    # The next table is editable: Click on the table to edit the cell
    table = Tk_Table(root, ["column one","column two", "column three"], row_numbers=True, stripped_rows = ("white","#f2f2f2"), select_mode="none")
    table.pack(expand=True, fill=BOTH)
    
    table.table_data = [[0, 1, 2],
 [3, 4, 5],
 [6, 7, 8],
 [9, 10, 11],
 [12, 13, 14],
 [15, 16, 17],
 [18, 19, 20],
 [21, 22, 23],
 [24, 25, 26],
 [27, 28, 29]]
    
    table.insert_row([1,2,3])

    show_info("We created an editable and zebra style table. Click on a cell to edit.")

    root.mainloop()
