try:
    from Tkinter import Label, Frame, Toplevel, Entry
    from Tkconstants import *
    from ttk import Separator
except ImportError:
    from tkinter import Label, Frame, Toplevel, Entry
    from tkinter.constants import *
    from tkinter.ttk import Separator
    
try:
  basestring
except NameError:
  basestring = str

class Listbox(Frame):
    def __init__(self, master, options, width=20, bordercolor="#cccccc", foreground="black", background="white", activebackground="#2780E3", activeforeground="white",padx=15, pady=7, command=None):
        Frame.__init__(self, master, background=background, highlightbackground=bordercolor, highlightcolor=bordercolor, highlightthickness=1, bd= 0)

        self._foreground = foreground
        self._background = background
        self._activebackground = activebackground
        self._activeforeground = activeforeground

        self._items = []
        
        index = 0
        for option in options:
            
            if option is None:
                Separator(self, orient=HORIZONTAL).pack(fill=X)
                continue
                
            if isinstance(option, basestring):
                test = option
                value = option
            else:
                text, value = option
            
            label_item = Label(self, width=width, text=text, background=background, foreground="black",  anchor=W, padx=padx, pady=pady)
            label_item.pack(fill=X)
            
            label_item.index = index
            label_item.value = value

            label_item.bind("<Enter>", self._on_enter_label_item)
            label_item.bind("<Leave>", self._on_leave_label_item)
            label_item.bind("<1>", lambda event, index=index:self._on_click_item(event.widget, index))
            self._items.append(label_item)
            
            index += 1
        
        self._actived_item = None
        self._command = command

        self.bind("<Up>", self._on_up)
        self.bind("<Down>", self._on_down)
        self.bind("<Return>", self._on_return)

    def _on_return(self, event):
        if self._command is not None:
             if self._actived_item is not None:
                 self._command(self._actived_item.value)

    def _activate_colors(self, label_item):
        label_item.configure(background=self._activebackground, foreground=self._activeforeground)
    
    def _deactivate_colors(self, label_item):
        label_item.configure(background=self._background, foreground=self._foreground)

    def _on_enter_label_item(self, event):
        label_item = event.widget
        self._activate_colors(label_item)
        
        self._actived_item = label_item

    def _on_leave_label_item(self, event):
        label_item = event.widget
        self._deactivate_colors(label_item)

    def _on_click_item(self, label_item, index):
        if self._actived_item != label_item:
            self._deactivate_colors(self._actived_item)
            self._activate_colors(label_item)
            self._actived_item = label_item
        
        self.focus_set()
        if self._command is not None:
            self._command(label_item.value)

    def _on_up(self, event):
        if self._actived_item is None:
            label_item = self._items[0]
            self._actived_item = label_item
            self._activate_colors(label_item)

        else:
            index = self._actived_item.index
            if index == 0: return
            index -= 1

            self._deactivate_colors(self._actived_item)
            
            self._actived_item = self._items[index]
            self._activate_colors(self._actived_item)

    def _on_down(self, event):
        if self._actived_item is None:
            label_item = self._items[0]
            self._actived_item = label_item
            self._activate_colors(label_item)

        else:
            index = self._actived_item.index
            if index == len(self._items) - 1: return
            
            index += 1
            
            self._deactivate_colors(self._actived_item)
            self._actived_item = self._items[index]
            self._activate_colors(self._actived_item)

if __name__ == "__main__":
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk
        
    root = Tk()

    def command(value):
        print("selected value: %s"%value)

    listbox = Listbox(root, options=(("Spain", "es"), None, ("USA", "us"), ("France","fr"), ("Britain", "br")), command=command)
    listbox.pack()

    listbox.focus()

    root.mainloop()
