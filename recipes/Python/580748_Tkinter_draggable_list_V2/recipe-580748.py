# version: 0.3
# Author: Miguel Martinez Lopez


try:
    from Tkinter import Frame
except ImportError:
    from tkinter import Frame

# Python 3 support
try:
    basestring
except NameError:
    basestring = str

class Item(Frame):
    def __init__(self, master, value, width, height, selection_handler=None, drag_handler = None, drop_handler=None, **kwargs):

        kwargs.setdefault("class_", "Item")
        Frame.__init__(self, master, **kwargs)
        
        self._x = None
        self._y = None
        
        self._width = width
        self._height = height

        self._tag = "item%s"%id(self)
        self._value = value

        self._selection_handler = selection_handler
        self._drag_handler = drag_handler
        self._drop_handler = drop_handler

    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y
        
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
        
    @property
    def value(self):
        return self._value
        
    def init(self, container, x, y):
        self._x = x
        self._y = y

        self.place(in_=container, x=x, y=y, width=self._width, height=self._height)

        self.bind_class(self._tag, "<ButtonPress-1>", self._on_selection)
        self.bind_class(self._tag, "<B1-Motion>", self._on_drag)
        self.bind_class(self._tag, "<ButtonRelease-1>", self._on_drop)

        self._add_bindtag(self)
        
        # Python3 compatibility: dict.values() return a view
        list_of_widgets = list(self.children.values())
        while len(list_of_widgets) != 0:
            widget = list_of_widgets.pop()
            list_of_widgets.extend(widget.children.values())
            
            self._add_bindtag(widget)
    
    def _add_bindtag(self, widget):
        bindtags = widget.bindtags()
        if self._tag not in bindtags:
            widget.bindtags((self._tag,) + bindtags)

    def _on_selection(self, event):
        self.tkraise()

        self._move_lastx = event.x_root
        self._move_lasty = event.y_root
        
        if self._selection_handler:
            self._selection_handler(self)

    def _on_drag(self, event):
        self.master.update_idletasks()
        
        cursor_x = self._x + event.x
        cursor_y = self._y + event.y

        self._x += event.x_root - self._move_lastx
        self._y += event.y_root - self._move_lasty

        self._move_lastx = event.x_root
        self._move_lasty = event.y_root

        self.place_configure(x=self._x, y=self._y)

        if self._drag_handler:
            self._drag_handler(cursor_x, cursor_y)
           
    def _on_drop(self, event):
        if self._drop_handler:
            self._drop_handler()
            
    def set_position(self, x,y):
        self._x = x
        self._y = y
        self.place_configure(x =x, y =y)
        
    def move(self, dx, dy):
        self._x += dx
        self._y += dy

        self.place_configure(x =self._x, y =self._y)

class DDList(Frame):
    def __init__(self, master, item_width, item_height, item_relief=None, item_background=None, item_borderwidth=None, offset_x=0, offset_y=0, gap=0, **kwargs):
        kwargs["width"] = item_width+offset_x*2
        kwargs["height"] = offset_y*2

        Frame.__init__(self, master, **kwargs)

        self._item_borderwidth = item_borderwidth
        self._item_relief = item_relief
        self._item_background = item_background
        self._item_width = item_width
        self._item_height = item_height
        
        self._offset_x = offset_x
        self._offset_y = offset_y
               
        self._left = offset_x
        self._top = offset_y
        self._right = self._offset_x + self._item_width
        self._bottom = self._offset_y

        self._gap = gap

        self._index_of_selected_item = None
        self._index_of_empty_container = None

        self._list_of_items = []
        self._position = {}

        self._new_y_coord_of_selected_item = None

    def create_item(self, value=None, **kwargs):
        
        if self._item_relief is not None:
            kwargs.setdefault("relief", self._item_relief)
        
        if self._item_borderwidth is not None:
            kwargs.setdefault("borderwidth", self._item_borderwidth)
            
        if self._item_background is not None:
            kwargs.setdefault("background", self._item_background)

        item = Item(self.master, value, self._item_width, self._item_height, self._on_item_selected, self._on_item_dragged, self._on_item_dropped, **kwargs)   
        return item

    def configure_items(self, **kwargs):
        for item in self._list_of_items:
            item.configure(**kwargs)

    def add_item(self, item, index=None):
        if index is None:
            index = len(self._list_of_items)
        else:
            if not -len(self._list_of_items) < index < len(self._list_of_items):
                raise ValueError("Item index out of range")

            for i in range(index, len(self._list_of_items)):
                _item = self._list_of_items[i]
                _item.move(0,  self._item_height + self._gap)
                
                self._position[_item] += 1
        
        x = self._offset_x
        y = self._offset_y + index * (self._item_height + self._gap)

        self._list_of_items.insert(index, item)
        self._position[item] = index

        item.init(self, x,y)

        if len(self._list_of_items) == 1:
            self._bottom += self._item_height
        else:
            self._bottom += self._item_height + self._gap
            
        self.configure(height=self._bottom + self._offset_y)

        return item

    def delete_item(self, index):
        
        if isinstance(index, Item):
            index = self._position[index]
        else:
            if not -len(self._list_of_items) < index < len(self._list_of_items):
                raise ValueError("Item index out of range")

        item = self._list_of_items.pop(index)
        value = item.value

        del self._position[item]

        item.destroy()
        
        for i in range(index, len(self._list_of_items)):
            _item = self._list_of_items[i]
            _item.move(0,  -(self._item_height+self._gap))
            self._position[_item] -= 1
        
        if len(self._list_of_items) == 0:
            self._bottom -= self._item_height
        else:
            self._bottom -= self._item_height + self._gap

        self.configure(height=self._bottom + self._offset_y)
        
        return value

    del_item = delete_item
    
    def pop(self):
        return self.delete_item(-1)
        
    def shift(self):
        return self.delete_item(0)
        
    def append(self, item):
        self.add_item(item)
        
    def unshift(self, item):
        self.add_item(0, item)
        
    def get_item(self, index):
        return self._list_of_items[index]

    def get_value(self, index):
        return self._list_of_items[index].value

    def _on_item_selected(self, item):        
        self._index_of_selected_item = self._position[item]
        self._index_of_empty_container = self._index_of_selected_item

    def _on_item_dragged(self, x, y):

        if self._left < x < self._right and self._top < y < self._bottom:

            quotient, remainder = divmod(y-self._offset_y, self._item_height + self._gap)

            if remainder < self._item_height:
            
                new_container = quotient

                if new_container != self._index_of_empty_container:
                    if new_container > self._index_of_empty_container:
                        for index in range(self._index_of_empty_container+1, new_container+1, 1):
                            item = self._get_item_of_virtual_list(index)                            

                            item.move(0,-(self._item_height+self._gap))
                    else:
                        for index in range(self._index_of_empty_container-1, new_container-1, -1):
                            item = self._get_item_of_virtual_list(index)

                            item.move(0,self._item_height+self._gap)

                    self._index_of_empty_container = new_container
                    
    def _get_item_of_virtual_list(self, index):
        if self._index_of_empty_container == index:
            raise Exception("No item in index: %s"%index)
        else:
            if self._index_of_empty_container != self._index_of_selected_item:
                if index > self._index_of_empty_container:
                    index -= 1

                if index >= self._index_of_selected_item:
                    index += 1
            item = self._list_of_items[index]
            return item

    def _on_item_dropped(self):
        
        item = self._list_of_items.pop(self._index_of_selected_item)
        self._list_of_items.insert(self._index_of_empty_container, item)
        
        x = self._offset_x
        y = self._offset_y + self._index_of_empty_container *(self._item_height + self._gap)
        
        item.set_position(x,y)
        
        for i in range(min(self._index_of_selected_item, self._index_of_empty_container),max(self._index_of_selected_item, self._index_of_empty_container)+1):
            item = self._list_of_items[i]
            self._position[item] = i
            
        self._index_of_empty_container = None
        self._index_of_selected_item = None

if __name__ == "__main__":
    try:
        from Tkinter import Tk, IntVar, Label, Entry, Button
        import tkMessageBox as messagebox
        from Tkconstants import *
    except ImportError:
        from tkinter import Tk, IntVar, Label, Entry, Button, messagebox
        from tkinter.constants import *

    root = Tk()
    root.title("DDList example")
    root.geometry("%dx%d%+d%+d"%(640, 550, 0, 0))

    sortable_list = DDList(root, 200, 100, offset_x=10, offset_y=10, gap =10, item_borderwidth=1, item_relief="groove")
    sortable_list.pack(expand=True, fill=BOTH)
    
    for i in range(4):
        item = sortable_list.create_item(value=i)
        label = Label(item, text="this is a label %s"%i)
        label.pack(anchor=W, padx= (4,0), pady= (4,0))

        sortable_list.add_item(item)

    frame = Frame(root)
    frame.pack(fill=X, pady=(0, 10))
    
    indexVar = IntVar()
    label = Label(frame, text="Entry index of item to delete:")
    label.pack(side=LEFT, padx=(10,6))
    entry_of_index = Entry(frame,textvariable= indexVar, width=3)
    
    def delete_item():
        try:
            index = indexVar.get()
        except ValueError:
            messagebox.showerror("Error", "Not a valid integer")
            return

        entry_of_index.delete(0, END)
        sortable_list.delete_item(index)
    entry_of_index.bind('<Return>', delete_item)

    entry_of_index.pack(side=LEFT)
    
    Button(frame, text="Delete", command=delete_item).pack(side=LEFT, padx=(3,0))

    root.mainloop()
