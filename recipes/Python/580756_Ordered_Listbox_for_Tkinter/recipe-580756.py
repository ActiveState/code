# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))


try:
    from Tkinter import Frame, Listbox
    from ttk import Scrollbar
    from Tkconstants import *
except ImportError:
    from tkinter import Frame, Listbox
    from tkinter.ttk import Scrollbar
    from tkinter.constants import *


def make_autoscroll(sbar, first, last):
    """Hide and show scrollbar as needed."""
    first, last = float(first), float(last)
    if first <= 0 and last >= 1:
        sbar.grid_remove()
    else:
        sbar.grid()
    sbar.set(first, last)

def bisect(list_of_items, item, ascending_order=True, ignore_case=False):    
    lo = 0
    hi = len(list_of_items)

    # I repeat a little bit myself here because I want to be more efficient.
    if ascending_order:
        if ignore_case:
            item = item.lower()
            while lo < hi:
                mid = (lo+hi)//2

                if item < list_of_items[mid].lower(): hi = mid
                else: lo = mid+1
        else:
            while lo < hi:
                mid = (lo+hi)//2

                if item < list_of_items[mid]: hi = mid
                else: lo = mid+1
    else:
        if ignore_case:
            item = item.lower()
            while lo < hi:
                mid = (lo+hi)//2

                if item > list_of_items[mid].lower(): hi = mid
                else: lo = mid+1
        else:
            while lo < hi:
                mid = (lo+hi)//2

                if item > list_of_items[mid]: hi = mid
                else: lo = mid+1
    return lo


class Ordered_Listbox(Frame):
    def __init__(self, master, data=None, ascending_order = True, ignore_case=False, autoscroll=False, vscrollbar=True, hscrollbar=False, scrollbar_background=None, scrollbar_troughcolor=None, **kwargs):
        Frame.__init__(self, master)

        self._ignore_case = ignore_case
        self._ascending_order = ascending_order

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self._listbox = Listbox(self, *kwargs)        
        self._listbox.grid(row=0, column=0, sticky= N+E+W+S)

        scrollbar_kwargs = {}
        if scrollbar_background is not None:
            scrollbar_kwargs["background"] = scrollbar_background
            
        if scrollbar_troughcolor is not None:
            scrollbar_kwargs["throughcolor"] = scrollbar_troughcolor

        if vscrollbar:
            self._vbar=Scrollbar(self,takefocus=0, command=self._listbox.yview, **scrollbar_kwargs)
            self._vbar.grid(row=0, column=1, sticky= N+S)
            
            if autoscroll:
                self._listbox.config(yscrollcommand=lambda f, l: make_autoscroll(self._vbar, f, l))
            else:
                self._listbox.config(yscrollcommand=self._vbar.set)

        if hscrollbar:
            self._hbar=Scrollbar(self,takefocus=0, command=self._listbox.xview, **scrollbar_kwargs)
            self._hbar.grid(row=0, column=1, sticky= E+W)
            
            if autoscroll:
                self._listbox.config(xscrollcommand=lambda f, l: make_autoscroll(self._hbar, f, l))
            else:
                self._listbox.config(xscrollcommand=self._hbar.set)

        if data is not None:
            for item in data:
                self.add_item(item)

    def add_item(self, item):
        list_of_items = self._listbox.get(0, END)

        index = bisect(list_of_items, item, ignore_case=self._ignore_case, ascending_order=self._ascending_order)
        self._listbox.insert(index, item)

    def delete_item(self, item):
        list_of_items = self._listbox.get(0, END)
        index = bisect(list_of_items, item, ignore_case=self._ignore_case, ascending_order=self._ascending_order)
        self._listbox.delete(index-1)
        
    def selected_items(self):
        list_of_items = []

        for index in self._listbox.curselection():
            list_of_items.append(self._listbox.get(index))
            
        return list_of_items
        
    def selected_item(self):
        return self._listbox.curselection()[0]

    def deselect_all(self):
        self._listbox.selection_clear(0, END)
        
    def select(self, item):
        index = self.index(item)
        
        if index is None:
            return
        
        self._listbox.selection_set(index)

    def deselect(self, item):
        index = self.index(item)
        
        if index is None:
            return
        
        self._listbox.selection_clear(index)

    def index(self, item):
        list_of_items = self._listbox.get(0, END)

        try:
            index = list_of_items.index(item)
        except ValueError:
            return None

        return index

    def bind(self, event, handler):
        self._listbox.bind(event, handler)
    
    def clear(self):
        self._listbox.delete(1,END)

    def __iter__(self):
        return self.items
    
    @property
    def items(self):
        return self._listbox.get(0, END)


if __name__ == "__main__":
    try:
        from Tkinter import Tk, Label
    except ImportError:
        from tkinter import Tk, Label
        
    root = Tk()
    list_of_cities = ["New York", "London", "mADrid", "Tokyo", "caRaCas", "Ottawa", "PraGUE", "Cairo", "Moscow", "Quito", "LuxEMbourg", "Mexico City"]

    for ascending_order in (True, False):
        for ignore_case in (True, False):
            Label(root, text="ascending_order= %s, ignore_case= %s"%(ascending_order, ignore_case)).pack()
            ordered_listbox = Ordered_Listbox(root, data=list_of_cities, ascending_order=ascending_order, ignore_case=ignore_case)
            ordered_listbox.pack(pady=(0,6))
    

    ordered_listbox.add_item("Rome")
    ordered_listbox.add_item("Paris")

    ordered_listbox.select("Rome")
    ordered_listbox.pack()

    root.mainloop()
