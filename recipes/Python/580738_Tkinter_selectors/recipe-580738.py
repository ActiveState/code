# Author: Miguel Martinez Lopez
#
# Please let me know if you find a bug
# Uncomment the next line to see my email
#   print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))

"""Tkinter Selectors
    Select widgets using selectors synchronously or asynchronously.

    This is the provided API:
        toplevel_titles(widget)
        window_titles(widget)
        full_name_of_widgets(root)
        find_toplevel_by_title(widget, title)
        find_widgets_by_name(root, name)
        find_widget_by_name(root, name)
        find_widgets_by_class(root, class_)
        find_widget_by_class(root, class_)
        find(root, selector, callback, async=True)
        find_all(root, selector, callback, async=True)
        config(root, selector, **kwargs)
        config_async(root, selector, **kwargs)
        config_all(root, selector, **kwargs)
        config_all_async(root, selector, **kwargs)
        tk_print(root, name=True, class_= True, indent="\t")
"""
# Python 2/3 compatibility
import sys

PY3 = sys.version_info[0] ==3

if PY3:
  basestring = str
  unicode = str

class SubSelector(unicode):
    def __add__(self, txt):
        return self.__class__(unicode(self)+txt)

class SubSelector_Name(SubSelector):
    """Subselector that match the widget name"""

class SubSelector_Class(SubSelector):
    """Subselector that match the widget class"""

class Tkinter_Selector(object):

    def __init__(self, selector_string):

        if len(selector_string) == 0:
            raise ValueError("selector can't be zero length")

        if selector_string[0] == ".":
            self._anchor_start = True
            last_char = "."
            selector_string = selector_string[1:]

        else:            
            self._anchor_start = False
            
            if selector_string[0] == "*":
                last_char = "*"
                selector_string = selector_string[1:]
            else:
                last_char = None


        if selector_string[-1] == "*" or selector_string[-1] == ".":
            raise ValueError("'%s' is not allowed at the end"%selector_string[-1])

        selector_obj = []
        
        sequence_of_selector_elements = []
        
        selector_element = None

        for position, char in enumerate(selector_string):
            if char == ".":
                if last_char == "." or last_char == "*":
                    raise ValueError("Not allowed '%s' at position %d"%(last_char, position))
                
                sequence_of_selector_elements.append(selector_element)

                selector_element = None
            elif char == "*":
                if last_char == "." or last_char == "*":
                    raise ValueError("Not allowed '%s' at position %d"%(last_char, position))
    
                sequence_of_selector_elements.append(selector_element)
                selector_element = None

                selector_obj.append(sequence_of_selector_elements)
                sequence_of_selector_elements = []
            else:
                if selector_element is None:
                    if char.isupper():
                        selector_element = SubSelector_Class(char)
                    else:
                        selector_element = SubSelector_Name(char)
                else:
                    selector_element += char
                
            last_char = char

        if selector_element is not None:
            sequence_of_selector_elements.append(selector_element)

        if len(sequence_of_selector_elements) != 0:
            selector_obj.append(sequence_of_selector_elements)

        
        self._selector_obj = selector_obj
        self._selector_string = selector_string

    def match(self, root, callback, async=True):
        queue = [(root, 0, 0)]

        if async:
            def async_match():
                self._match(queue, callback)

                if len(queue) != 0:
                    root.after(0, async_match)
            async_match()
        else:
            while len(queue) != 0:
                self._match(queue, callback)

    def _match(self, queue, callback):
        widget, index_1, index_2 = queue.pop(0)
        selector_element = self._selector_obj[index_1][index_2]

        if len(self._selector_obj) == index_1 + 1 and len(self._selector_obj[-1]) == index_2 + 1:
            for child in self._matched_children(widget, selector_element):
                try:
                    callback(child)
                except StopIteration:
                    del queue[:]
                    return
        else:
            if len(self._selector_obj[index_1]) == index_2 +1:
                new_index_1 = index_1 + 1
                new_index_2 = 0
            else:
                new_index_1 = index_1
                new_index_2 = index_2 + 1

            for child in self._matched_children(widget, selector_element):
                queue.insert(0, (child, new_index_1, new_index_2))

        if index_2 == 0 and not (self._anchor_start and index_1 == 0):
            for child in widget.children.values():
                queue.append((child, index_1, 0))
            
    def _matched_children(self, widget, selector_element):
        for child_name, child in widget.children.items():
            if isinstance(selector_element, SubSelector_Name):
                if child_name == selector_element:
                    yield child
            else:
                if child.winfo_class() == selector_element:
                    yield child
    @property
    def anchor_start(self):
        return self._anchor_start
    
    def __str__(self):
        return self._selector_string

def iterate(root):
    queue_of_widgets = root.children.values()

    while True:
            
        if len(queue_of_widgets) == 0:
            return
        else:
            yield queue_of_widgets.pop()
            queue.extend(widget.children.values())


def get_root(widget):
    if str(widget) == ".":
        root = widget
    else:
        root = widget.nametowidget(".")
    return root
            
def find_toplevel_by_title(widget, title):
    root = get_root(widget)

    if  isinstance(title, re._pattern_type):
        for child in root.children.values():
            if child.winfo_class() == "Toplevel" and title.search(child.wm_title()):
                return child
    else:
        for child in root.children.values():
            if child.winfo_class() == "Toplevel" and child.wm_title() == title:
                return child

def toplevel_titles(widget):
    root = get_root(widget)

    list_of_titles = []

    for child in root.children.values():
        if child.winfo_class() == "Toplevel":
            list_of_titles.append(child.wm_title())

    return list_of_titles

def window_titles(widget):
    root = get_root(widget)

    return [root.wm_title()] + list_toplevel_titles(root)

def find_widgets_by_name(root, name):
    list_of_found_widgets = []
    
    queue = root.children.items()

    while True:
        
        widget_name, widget = queue.pop()
        if widget_name == name:
            list_of_found_widgets.append(widget)
            
        if len(queue) == 0:
            return list_of_found_widgets
        else:
            queue.extend(widget.children.items())

def find_widget_by_name(root, name):
    queue = root.children.items()

    while True:
        
        widget_name, widget = queue.pop()
        if widget_name == name:
            return widget
            
        if len(queue) == 0:
            return
        else:
            queue.extend(widget.children.items())
    
def find_widgets_by_class(root, class_):
    list_of_found_widgets = []
    
    for widget in iterate(root):
        if widget.winfo_class() == class_:
            list_of_found_widgets.append(widget)
        
    return list_of_found_widgets

def find_widget_by_class(root, class_):
    for widget in iterate(root):
        if widget.winfo_class() == class_:
            return widget

def full_name_of_widgets(root):
    names = [str(root)]

    queue_of_widgets = root.children.values()

    while True:

        if len(queue_of_widgets) == 0:
            return names
        else:
            names.append(str(queue_of_widgets.pop()))
            queue_of_widgets.extend(widget.children.values())
 

def find_all(root, selector, callback, async=True):
    list_of_found_widgets = []
    
    if isinstance(selector, basestring):
        selector = Tkinter_Selector(selector)

    selector.match(root, callback, async)

def find(root, selector, callback, async=True):
    if isinstance(selector, basestring):
        selector = Tkinter_Selector(selector)

    def wrapper_callback(widget):
        callback(widget)
        raise StopIteration

    selector.match(root, wrapper_callback, async)

def config_extended(root, selector, async, config_kwargs):
    if isinstance(selector, basestring):
        selector = Tkinter_Selector(selector)
    
    def callback(widget, config_kwargs=config_kwargs):
        widget.configure(**config_kwargs)
        raise StopIteration

    selector.match(root, callback, async)

def config_all_extended(root, selector, async, config_kwargs):
    if isinstance(selector, basestring):
        selector = Tkinter_Selector(selector)
    
    selector.match(root, lambda widget, config_kwargs = config_kwargs: widget.configure(**config_kwargs), async)


def config(root, selector, **kwargs):
    config_extended(root, selector, False, kwargs)

def config_async(root, selector, **kwargs):
    config_extended(root, selector, True, kwargs)

def config_all(root, selector, **kwargs):
    config_all_extended(root, selector, False, kwargs)

def config_all_async(root, selector, **kwargs):
    config_all_extended(root, selector, True, kwargs)

def tk_print(root, name=True, class_= True, indent="\t"):
    """Print a tree of widget names and/or classes"""
    print(root)
    
    if name or class_:
        _print_widget_tree_from(root, name, class_, 1, indent)

def _print_widget_tree_from(root, print_names, print_classes, level, indent):
    for child_name, child in root.children.items():
        
        if print_names:
            if print_classes:
                output = "%s (%s)"%(child_name, child.winfo_class())
            else:
                output = child_name
        else:
            output = child.winfo_class()

        print(indent*level + output)
        _print_widget_tree_from(child, print_names, print_classes, level+1, indent)
    


if __name__ == "__main__":
    try:
        from Tkinter import Tk, Frame, Label, Button, LabelFrame
    except ImportError:
        from tkinter import Tk, Frame, Label, Button, LabelFrame
    
    root = Tk()
    
    container1 = LabelFrame(root, class_="Container1")
    container1.pack()
    
    left = Frame(container1, name="left")
    left.pack()
    
    Label(left, name="label0").pack()
    
    center = Frame(container1, name="center")
    center.pack()
    
    area1 = Frame(center, class_="Area1")
    area1.pack()
    
    area2 = Frame(center, class_="Area2")
    area2.pack()
    
    Button(area2, name="my_button").pack()
    Button(area2).pack()
    
    area3 = Frame(center, class_="Area3")
    area3.pack()
    
    area4 = Frame(center, class_="Area4")
    area4.pack()
    
    child_frame = Frame(area4, class_="Child_Frame")
    child_frame.pack()
    
    child_label = Label(area4)
    child_label.pack()
    
    right = Frame(container1, name="right")
    right.pack()
    
    container2 = Frame(root, class_="Container2")
    container2.pack()

    tk_print(root)

    def show(widget):
        print(widget)

    find_all(root, "Container1*Label", show, False)
    find(root, "Container1*label0", show)
    find_all(root, "center*Button", show)
    find_all(root, ".Container1.left.label0", show)
    
    config_all(root, "Container1*Label", text="this is a label")
    config(root, "Container1*label0", text="this is a label number 0")
    config_all(root, "Container1*Button", text="this is a button")
    config(root, "Container1", text="this is Container 1")

    root.mainloop()
