# Author: Miguel Martinez Lopez
# Version: 0.4

try:
    import Tkinter as tk
    import ttk

    from Tkinter import StringVar
    import tkFont

    from ttk import Style
    from Tkconstants import *
except ImportError:
    import tkinter as tk
    import tkinter.ttk as ttk

    from tkinter import StringVar
    import tkinter.font as tkFont
    from tkinter.ttk import Style
    from tkinter.constants import *
    
import base64

import weakref

# Support for Python 3
try:
    xrange
except NameError:
    xrange = range

try:
  basestring
except NameError:
  basestring = str


class NotValidID(Exception):
    """Not a valid ID widget"""

_registered_widgets =  weakref.WeakValueDictionary()

def get_widget_by_ID(ID):
    if ID in _registered_widgets:
        return _registered_widgets[ID]
    else:
        raise NotValidID
    
def get_background_of_widget(widget):
    try:
        # We assume first tk widget
        background = widget.cget("background")
    except:
        # Otherwise this is a ttk widget
        style = widget.cget("style")

        if style == "":
            # if there is not style configuration option, default style is the same than widget class
            style = widget.winfo_class()

        background = Style().lookup(style, 'background')
    
    return background

def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))
    

class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.contains_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.contains_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.contains_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.contains_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state


class MetroWidget(object):
    """Inherits background from parent and adds ID to widget"""
    def __init__(self, widget_class, master, ID, kwargs, inherit_background=True):
        if inherit_background:
            if "background" in kwargs:
                if kwargs["background"] is None:
                    kwargs["background"] = get_background_of_widget(master)
                    self.inherited_background = True
                else:
                    self.inherited_background = False
            elif "bg" in kwargs:
                if kwargs["bg"] is None:
                    kwargs["bg"] = get_background_of_widget(master)
                    self.inherited_background = True
                else:
                    self.inherited_background = False
            else:
                kwargs["background"] = get_background_of_widget(master)
                self.inherited_background = True

        widget_class.__init__(self, master, **kwargs)
        
        if ID is not None:
            global _registered_widgets
            if ID in _registered_widgets:
                raise Exception("ID already taken: %s"%ID)

            _registered_widgets[ID] = self

        self._ID = ID
        
    def ID(self):
        return self._ID

class Combobox(ttk.Combobox, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, ttk.Combobox, master, ID, kwargs, False)

class PanedWindow(tk.PanedWindow, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.PanedWindow, master, ID, kwargs)

class Entry(tk.Entry, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.Entry, master, ID, kwargs, False)

class Button(tk.Button, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.Button, master, ID, kwargs, False)

class Frame(tk.Frame, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.Frame, master, ID, kwargs)

class LabelFrame(tk.LabelFrame, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.LabelFrame, master, ID, kwargs)

class Label(tk.Label, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.Label, master, ID, kwargs)

class Radiobutton(tk.Radiobutton, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.Radiobutton, master, ID, kwargs)

class Checkbutton(tk.Checkbutton, MetroWidget):
    def __init__(self, master, ID=None, **kwargs):
        MetroWidget.__init__(self, tk.Checkbutton, master, ID, kwargs)


class Metro_ButtonLabel(Label):
    def __init__(self, master, text, background, ID=None, foreground="white", opacity=0.8, font=None, command=None, padx=7, pady=7):
        Label.__init__(self, master, ID=ID, text=text, background=background, foreground=foreground, padx=padx, pady=pady)
        if font:
            self.configure(font=font)

        opacity = float(opacity)

        if background.startswith("#"):
            r,g,b = hex2rgb(background)
        else:
            # Color name
            r,g,b = master.winfo_rgb(background)

        r = int(opacity*r)
        g = int(opacity*g)
        b = int(opacity*b)

        if r <= 255 and g <= 255 and b <=255:
            self._activebackground = '#%02x%02x%02x' % (r,g,b)
        else:
            self._activebackground = '#%04x%04x%04x' % (r,g,b)

        self._background = background
        
        self.bind("<Enter>", self._state_active)
        self.bind("<Leave>", self._state_normal)
        
        self._command = command

        if command is not None:
            self.bind("<ButtonRelease-1>", command)

    def _state_normal(self, event):
        self.configure(background=self._background)

    def _state_active(self, event):
        self.configure(background=self._activebackground)

    def invoke(self):
        if self._command is not None:
            self._command()

class Metro_Button(Button):
    def __init__(self, master, text, background, ID=None, foreground="white", opacity=0.8, font=None, command=None, padx=7, pady=7):
        opacity = float(opacity)

        if background.startswith("#"):
            r,g,b = hex2rgb(background)
        else:
            # Color name
            r,g,b = master.winfo_rgb(background)

        r = int(opacity*r)
        g = int(opacity*g)
        b = int(opacity*b)

        if r <= 255 and g <= 255 and b <=255:
            activebackground = '#%02x%02x%02x' % (r,g,b)
        else:
            activebackground = '#%04x%04x%04x' % (r,g,b)


        Button.__init__(self, master, ID=ID, text=text, activebackground=activebackground, background=background, activeforeground=foreground, foreground=foreground, relief=FLAT, padx=padx, pady=pady, borderwidth=0, highlightthickness=0)
        if font:
            self.configure(font=font)

        if command:
            self.configure(command=command)

class Metro_Entry(Frame):
    BORDER_COLOR = "#999999"
    ACTIVE_BORDERCOLOR = "#787878"

    BACKGROUND = "white"

    DISABLED_BACKGROUND = "#EBEBE4"
    DISABLED_FOREGROUND = "#545454"
    
    BORDER_WIDTH = 1

    def __init__(self, master, width=None, placeholder=None, placeholder_font=None, placeholder_color="grey", highlightthickness= 1, state=NORMAL, font=None, ID=None):

        Frame.__init__(self, master, ID=ID, bd=0, background=Metro_Entry.BACKGROUND, highlightbackground=Metro_Entry.BORDER_COLOR, highlightcolor=Metro_Entry.BORDER_COLOR, highlightthickness=Metro_Entry.BORDER_WIDTH)
        
        self._entry = Entry(self, background=Metro_Entry.BACKGROUND, disabledbackground=Metro_Entry.DISABLED_BACKGROUND , disabledforeground=Metro_Entry.DISABLED_FOREGROUND, highlightthickness=0, bd=0)
        self._entry.pack(expand=True, fill=BOTH, padx=5, pady=5)

        if placeholder:
            add_placeholder_to(self._entry, placeholder, color=placeholder_color, font=placeholder_font)

        if font:
            self._entry.configure(font=font)

        if width:
            self._entry.configure(width=width)

        self._highlightthickness = highlightthickness

        self._entry.bind("<Escape>", lambda event: self._entry.nametowidget(".").focus())

        self._entry.bind('<FocusIn>', self._on_focusin, add="+")
        self._entry.bind('<FocusOut>', self._on_focusout, add="+")
        
        self.delete = self._entry.delete
        self.get = self._entry.get
        self.icursor = self._entry.icursor
        self.insert = self._entry.insert
        self.insert = self._entry.insert
        self.scan_dragto = self._entry.scan_dragto
        self.scan_dragto = self._entry.scan_dragto
        self.scan_mark = self._entry.scan_mark
        self.select_adjust = self._entry.select_adjust
        self.select_clear = self._entry.select_clear
        self.select_from = self._entry.select_from
        self.select_present = self._entry.select_present
        self.select_range = self._entry.select_range
        self.select_to = self._entry.select_to
        self.selection_adjust = self._entry.selection_adjust
        self.selection_clear = self._entry.selection_clear
        self.selection_from = self._entry.selection_from
        self.selection_present = self._entry.selection_present
        self.selection_range = self._entry.selection_range
        self.selection_range = self._entry.selection_range
        self.selection_to = self._entry.selection_to
        self.xview = self._entry.xview
        self.xview_moveto = self._entry.xview_moveto
        self.xview_scroll = self._entry.xview_scroll

    def _on_focusin(self, event):
        if self._highlightthickness == 0:
            self.configure(highlightbackground=Metro_Entry.BORDER_COLOR, highlightcolor=Metro_Entry.BORDER_COLOR, highlightthickness=Metro_Entry.BORDER_WIDTH)
        else:
            self.configure(highlightbackground=Metro_Entry.ACTIVE_BORDERCOLOR, highlightcolor=Metro_Entry.ACTIVE_BORDERCOLOR, highlightthickness=self._highlightthickness)

    def _on_focusout(self, event):
        self.configure(highlightbackground=Metro_Entry.BORDER_COLOR, highlightcolor=Metro_Entry.BORDER_COLOR, highlightthickness=Metro_Entry.BORDER_WIDTH)

    def get_state(self):
        return sel._entry.cget("state")

    def set_state(self, state):
        if state == NORMAL:
             self.configure(background="white")
        else: 
            self.configure(background=Metro_Entry.DISABLED_BACKGROUND)

        self._entry.configure(state=state)

    def get_font(self):
        return sel._entry.cget("font")

    def set_font(self, font):
        self._entry.configure(font=font)

    def bind_entry(self, event, handler):
        self._entry.bind(event, handler)

class Search_Box(Frame):
    def __init__(self, master, button_text="Search", button_ipadx=16, button_background="#009688", button_foreground="white", button_font=None, opacity=0.8, placeholder=None, placeholder_font=None, placeholder_color="grey", entry_highlightthickness=1, entry_width=30, entry_font=None, command=None, ID=None):
        Frame.__init__(self, master, ID=ID)
        
        self._command = command

        self.entry = Metro_Entry(self, width=entry_width, placeholder=placeholder, placeholder_font=placeholder_font, placeholder_color=placeholder_color, highlightthickness=entry_highlightthickness)
        self.entry.pack(side=LEFT, fill=BOTH)

        if entry_font:
            self.entry.configure(font=entry_font)
            
        self.button = Metro_Button(self, text=button_text, background=button_background, foreground=button_foreground, font=button_font, command=self._execute_command, padx=button_ipadx)
        self.button.pack(side=LEFT, fill=Y)

        if command is not None:
            self.entry.bind_entry("<Return>", lambda event: self.button.invoke())

    def get_text(self):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            if entry.placeholder_state.contains_placeholder:
                return ""
            else:
                return entry.get()
        else:
            return entry.get()
        
    def set_text(self, text):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            entry.placeholder_state.contains_placeholder = False

        entry.delete(0, END)
        entry.insert(0, text)
        
    def clear(self):
        self.entry_var.set("")
        
    def focus(self):
        self.entry.focus()

    def _execute_command(self):
        text = self.get_text()
        self._command(text)


class Base_Container(object):
    @property
    def background(self):
        return self.cget("background")

    def set_background(self, background, cascade=True):
        self.configure(background=background)

        if not cascade:
            return

        list_of_widgets = list(form_widget.children.values())
        
        while True:
            try:
                widget = list_of_widgets.pop()
            except IndexError:
                break

            list_of_widgets.extend(list(widget.children.values()))
            
            if hasattr(widget, "inherited") and not widget.inherited:
                continue
            
            try:
                widget.configure(background=background)
            except:
                pass

class Container(Frame, Base_Container):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("class_", "Container")
        Frame.__init__(self, master, **kwargs)

class Label_Container(LabelFrame, Base_Container):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("class_", "Label_Container")
        LabelFrame.__init__(self, master, **kwargs)

class Link_Button(Label):
    def __init__(self, master, text, background=None, font=None, familiy=None, size=None, underline=True, visited_fg = "#551A8B", normal_fg = "#0000EE", visited=False, action=None, ID=None):
        self._visited_fg = visited_fg
        self._normal_fg = normal_fg
        
        if visited:
            fg = self._visited_fg
        else:
            fg = self._normal_fg

        if font is None:
            default_font = tkFont.nametofont("TkDefaultFont")
            family = default_font.cget("family")

            if size is None:
                size = default_font.cget("size")

            font = tkFont.Font(family=family, size=size, underline=underline)

        Label.__init__(self, master, ID=ID, background=background, text=text, fg=fg, cursor="hand2", font=font)

        self._visited = visited
        self._action = action

        self.bind("<Button-1>", self._on_click)

    @property
    def visited(self):
        return self._visited
        
    @visited.setter
    def visited(self, is_visited):
        if is_visited:
            self.configure(fg=self._visited_fg)
            self._visited = True
        else:
            self.configure(fg=self._normal_fg)
            self._visited = False

    def _on_click(self, event):
        if not self._visited:
            self.configure(fg=self._visited_fg)

        self._visited = True

        if self._action:
            self._action()

    def ID(self):
        return self._ID

class QuoteFrame(Frame):
    CONTENT_BACKGROUND = "#eeeeee"
    CONTENT_PADDING = 10
    LEFT_BORDER_COLOR = "#555555"
    LEFT_BORDER_WIDTH = 6

    def __init__(self,master=None, text=None, ID=None):
        Frame.__init__(self, master, ID=ID, background = self.CONTENT_BACKGROUND)
        Frame(self, background=self.LEFT_BORDER_COLOR, width=self.LEFT_BORDER_WIDTH).pack(side=LEFT, fill=Y)
    
        self.body = Container(self, background = self.CONTENT_BACKGROUND, padx=self.CONTENT_PADDING, pady=self.CONTENT_PADDING)
        self.body.pack(expand=True, fill=BOTH)
        
        if text is not None:
            Label(self.body, text=text).pack(anchor=W)

class Metro_LabelFrame(Frame):
    HEADER_BACKGROUND = "#1ba1e2"
    HEADER_FOREGROUND = "white"
    CONTENT_BACKGROUND = "#e8f1f4"
    INNER_PADDING = 8
    
    FONT_HEADER = "TkDefaultFont"
    #("Segoe UI", "Open Sans", "sans-serif", "serif")

    def __init__(self, master, title, ID=None):
        Frame.__init__(self, master, ID=ID)
        
        header = tk.Frame(self, background=self.HEADER_BACKGROUND, padx=self.INNER_PADDING, pady= self.INNER_PADDING)
        header.pack(fill=X)
        
        self._title = title
        self._title_label = tk.Label(header, text=title, foreground=self.HEADER_FOREGROUND, background=self.HEADER_BACKGROUND, font=self.FONT_HEADER)
        self._title_label.pack(anchor=W)
        
        self.body = Container(self, padx=self.INNER_PADDING, pady= self.INNER_PADDING, background = self.CONTENT_BACKGROUND)
        self.body.pack(expand=True, fill=BOTH)
        
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self._title_label.configure(text=title)


class Metro_Panel(Frame):
    def __init__(self, master, title, header_color, border_color, width=None, ID=None):
        Frame.__init__(self, master, ID=ID, highlightbackground=border_color, highlightcolor=border_color, highlightthickness=1, background="white")
        heading = tk.Frame(self, background=header_color)
        heading.pack(fill=X)
                
        title_label = tk.Label(heading, text=title, foreground="white", background=header_color)
        title_label.pack(padx=8, pady=1, anchor=W)
        
        if width is not None:
            heading.pack_propagate(False)
            heading.configure(width=width, height=title_label.winfo_reqheight()+2)
        
        self.body = Container(self, background="white", padx=10, pady=13)
        self.body.pack(expand=True, fill=BOTH)

class Primary_Panel(Metro_Panel):
    def __init__(self, master, title, width=None):
        Metro_Panel.__init__(self, master, title, "#2780e3", "#2780e3", width)

class Danger_Panel(Metro_Panel):
    def __init__(self, master, title, width=None):
        Metro_Panel.__init__(self, master, title, "#ff0039", "#f0005e", width)

class Success_Panel(Metro_Panel):
    def __init__(self, master, title, width=None):
        Metro_Panel.__init__(self, master, title, "#3fb618", "#4e9f15", width)

class Info_Panel(Metro_Panel):
    def __init__(self, master, title, width=None):
        Metro_Panel.__init__(self, master, title, "#9954bb", "#7643a8", width)

class Warning_Panel(Metro_Panel):
    def __init__(self, master, title, width=None):
        Metro_Panel.__init__(self, master, title, "#ff7518", "#ff4309", width)

class Metro_Checkbutton(tk.Checkbutton):
    image = { 
        16: 'I2RlZmluZSBpbWFnZV93aWR0aCAxNgojZGVmaW5lIGltYWdlX2hlaWdodCAxNgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4ZmYsMHhmZiwweDAxLDB4ODAsMHgwMSwweDgwLDB4MDEsMHg4MCwweDAxLDB4ODAsMHgwMSwweDgwLDB4MDEsMHg4MCwweDAxLAoweDgwLDB4MDEsMHg4MCwweDAxLDB4ODAsMHgwMSwweDgwLDB4MDEsMHg4MCwweDAxLDB4ODAsMHgwMSwweDgwLDB4MDEsMHg4MCwKMHhmZiwweGZmCn07',
        22: 'I2RlZmluZSBpbWFnZV93aWR0aCAyMgojZGVmaW5lIGltYWdlX2hlaWdodCAyMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4ZmYsMHhmZiwweDNmLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLAoweDAxLDB4MDAsMHgyMCwweDAxLDB4MDAsMHgyMCwweDAxLDB4MDAsMHgyMCwweDAxLDB4MDAsMHgyMCwweDAxLDB4MDAsMHgyMCwKMHgwMSwweDAwLDB4MjAsMHgwMSwweDAwLDB4MjAsMHgwMSwweDAwLDB4MjAsMHgwMSwweDAwLDB4MjAsMHgwMSwweDAwLDB4MjAsCjB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLAoweDAxLDB4MDAsMHgyMCwweDAxLDB4MDAsMHgyMAp9Ow==',
        24: 'I2RlZmluZSBpbWFnZV93aWR0aCAyNAojZGVmaW5lIGltYWdlX2hlaWdodCAyNApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4ZmYsMHhmZiwweGZmLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLAoweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwKMHgwMywweDAwLDB4YzAsMHgwMywweDAwLDB4YzAsMHgwMywweDAwLDB4YzAsMHgwMywweDAwLDB4YzAsMHgwMywweDAwLDB4YzAsCjB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLAoweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwweGZmLDB4ZmYsMHhmZgp9Ow==',
        32: 'I2RlZmluZSBpbWFnZV93aWR0aCAzMgojZGVmaW5lIGltYWdlX2hlaWdodCAzMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4MDMsMHgwMCwweDAwLAoweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwKMHgwMCwweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsCjB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLAoweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwKMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsCjB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwweDAzLAoweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwKMHgwMywweDAwLDB4MDAsMHhjMCwweGZmLDB4ZmYsMHhmZiwweGZmCn07',
        48: 'I2RlZmluZSBpbWFnZV93aWR0aCA0OAojZGVmaW5lIGltYWdlX2hlaWdodCA0OApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLAoweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwKMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsCjB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLAoweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwKMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsCjB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLAoweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwKMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsCjB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLAoweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwKMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsCjB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLAoweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwKMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsCjB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLAoweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwKMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsCjB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLAoweGZmLDB4ZmYsMHhmZgp9Ow=='
    }

    selectimage = {   
        16: 'I2RlZmluZSBpbWFnZV93aWR0aCAxNgojZGVmaW5lIGltYWdlX2hlaWdodCAxNgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4ZmYsMHhmZiwweDAxLDB4ODAsMHgwMSwweDgwLDB4MDEsMHg4MCwweDAxLDB4OTgsMHgwMSwweGJjLDB4MTksMHg5ZSwweDNkLAoweDhmLDB4ZjksMHg4NywweGYxLDB4ODMsMHhlMSwweDgxLDB4YzEsMHg4MCwweDAxLDB4ODAsMHgwMSwweDgwLDB4MDEsMHg4MCwKMHhmZiwweGZmCn07',
        22: 'I2RlZmluZSBpbWFnZV93aWR0aCAyMgojZGVmaW5lIGltYWdlX2hlaWdodCAyMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4ZmYsMHhmZiwweDNmLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLAoweDAxLDB4MDAsMHgyMCwweDAxLDB4MDAsMHgyMywweDAxLDB4ODAsMHgyNywweDAxLDB4YzAsMHgyZiwweDMxLDB4ZTAsMHgyNywKMHg3OSwweGYwLDB4MjMsMHhmOSwweGY4LDB4MjEsMHhmMSwweGZkLDB4MjAsMHhlMSwweDdmLDB4MjAsMHhjMSwweDNmLDB4MjAsCjB4ODEsMHgxZiwweDIwLDB4MDEsMHgwZiwweDIwLDB4MDEsMHgwNiwweDIwLDB4MDEsMHgwMCwweDIwLDB4MDEsMHgwMCwweDIwLAoweDAxLDB4MDAsMHgyMCwweDAxLDB4MDAsMHgyMAp9Ow==',
        24: 'I2RlZmluZSBpbWFnZV93aWR0aCAyNAojZGVmaW5lIGltYWdlX2hlaWdodCAyNApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4ZmYsMHhmZiwweGZmLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLDB4MDMsMHgwMCwweGMwLAoweDAzLDB4MDAsMHhjMiwweDAzLDB4MDAsMHhjNywweDAzLDB4ODAsMHhjZiwweDQzLDB4ODAsMHhjZiwweGUzLDB4YzAsMHhjNywKMHhmMywweGUxLDB4YzMsMHhmMywweGYxLDB4YzEsMHhlMywweGZiLDB4YzEsMHhlMywweGZmLDB4YzAsMHhjMywweDdmLDB4YzAsCjB4ODMsMHgzZiwweGMwLDB4MDMsMHgxZiwweGMwLDB4MDMsMHgwZSwweGMwLDB4MDMsMHgwNCwweGMwLDB4MDMsMHgwMCwweGMwLAoweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwweDAzLDB4MDAsMHhjMCwweGZmLDB4ZmYsMHhmZgp9Ow==',
        32: 'I2RlZmluZSBpbWFnZV93aWR0aCAzMgojZGVmaW5lIGltYWdlX2hlaWdodCAzMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4MDMsMHgwMCwweDAwLAoweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwKMHgwMCwweGMwLDB4MDMsMHgwMCwweDgwLDB4YzAsMHgwMywweDAwLDB4YzAsMHhjMywweDAzLDB4MDAsMHhlMCwweGM3LDB4MDMsCjB4MDAsMHhmMCwweGNmLDB4ODMsMHgwMCwweGY4LDB4Y2YsMHhjMywweDAzLDB4ZmMsMHhjNywweGUzLDB4MDcsMHhmZSwweGMzLAoweGYzLDB4MGYsMHhmZiwweGMxLDB4ZjMsMHg5ZiwweGZmLDB4YzAsMHhlMywweGZmLDB4N2YsMHhjMCwweGMzLDB4ZmYsMHgzZiwKMHhjMCwweDgzLDB4ZmYsMHgxZiwweGMwLDB4MDMsMHhmZiwweDBmLDB4YzAsMHgwMywweGZlLDB4MDcsMHhjMCwweDAzLDB4ZmMsCjB4MDMsMHhjMCwweDAzLDB4ZjgsMHgwMSwweGMwLDB4MDMsMHhmMCwweDAwLDB4YzAsMHgwMywweDIwLDB4MDAsMHhjMCwweDAzLAoweDAwLDB4MDAsMHhjMCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MDMsMHgwMCwweDAwLDB4YzAsMHgwMywweDAwLDB4MDAsMHhjMCwKMHgwMywweDAwLDB4MDAsMHhjMCwweGZmLDB4ZmYsMHhmZiwweGZmCn07',
        48: 'I2RlZmluZSBpbWFnZV93aWR0aCA0OAojZGVmaW5lIGltYWdlX2hlaWdodCA0OApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLAoweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwKMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsCjB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLAoweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwKMHgwMCwweDE4LDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDNjLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDdlLDB4ZTAsCjB4MDcsMHgwMCwweDAwLDB4MDAsMHhmZiwweGUwLDB4MDcsMHgwMCwweDAwLDB4ODAsMHhmZiwweGUxLDB4MDcsMHgwMCwweDAwLAoweGMwLDB4ZmYsMHhlMywweDA3LDB4MTgsMHgwMCwweGUwLDB4ZmYsMHhlMSwweDA3LDB4M2MsMHgwMCwweGYwLDB4ZmYsMHhlMCwKMHgwNywweDdlLDB4MDAsMHhmOCwweDdmLDB4ZTAsMHgwNywweGZmLDB4MDAsMHhmYywweDNmLDB4ZTAsMHg4NywweGZmLDB4MDEsCjB4ZmUsMHgxZiwweGUwLDB4YzcsMHhmZiwweDAzLDB4ZmYsMHgwZiwweGUwLDB4ODcsMHhmZiwweDg3LDB4ZmYsMHgwNywweGUwLAoweDA3LDB4ZmYsMHhjZiwweGZmLDB4MDMsMHhlMCwweDA3LDB4ZmUsMHhmZiwweGZmLDB4MDEsMHhlMCwweDA3LDB4ZmMsMHhmZiwKMHhmZiwweDAwLDB4ZTAsMHgwNywweGY4LDB4ZmYsMHg3ZiwweDAwLDB4ZTAsMHgwNywweGYwLDB4ZmYsMHgzZiwweDAwLDB4ZTAsCjB4MDcsMHhlMCwweGZmLDB4MWYsMHgwMCwweGUwLDB4MDcsMHhjMCwweGZmLDB4MGYsMHgwMCwweGUwLDB4MDcsMHg4MCwweGZmLAoweDA3LDB4MDAsMHhlMCwweDA3LDB4MDAsMHhmZiwweDAzLDB4MDAsMHhlMCwweDA3LDB4MDAsMHhmZSwweDAxLDB4MDAsMHhlMCwKMHgwNywweDAwLDB4ZmMsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4NzgsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MzAsCjB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLAoweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwweDAwLDB4MDAsMHhlMCwweDA3LDB4MDAsMHgwMCwKMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsMHgwNywweDAwLDB4MDAsMHgwMCwweDAwLDB4ZTAsCjB4MDcsMHgwMCwweDAwLDB4MDAsMHgwMCwweGUwLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLDB4ZmYsMHhmZiwweGZmLAoweGZmLDB4ZmYsMHhmZgp9Ow=='
    }

    def __init__(self, master, size=22, **kw):
        image = Metro_Checkbutton.image[size]
        
        if isinstance(image, basestring):
            Metro_Checkbutton.image[size] = image = tk.BitmapImage(data=base64.b64decode(image))

        selectimage = Metro_Checkbutton.selectimage[size]
        
        if isinstance(selectimage, basestring):
            Metro_Checkbutton.selectimage[size] = selectimage = tk.BitmapImage(data=base64.b64decode(selectimage))

        background = get_background_of_widget(master)
        tk.Checkbutton.__init__(self, master, indicatoron=0, background=background, activebackground="white", selectimage=selectimage, image=image, highlightthickness=0, **kw)

class Metro_Radiobutton(tk.Radiobutton):
    image = {
        16: 'I2RlZmluZSBpbWFnZV93aWR0aCAxNgojZGVmaW5lIGltYWdlX2hlaWdodCAxNgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4ZTAsMHgwNywweGY4LDB4MWYsMHgzYywweDNjLDB4MGUsMHg3MCwweDA2LDB4NjAsMHgwNywweGUwLDB4MDMsMHhjMCwweDAzLAoweGMwLDB4MDMsMHhjMCwweDAzLDB4YzAsMHgwNywweGUwLDB4MDYsMHg2MCwweDBlLDB4NzAsMHgzYywweDNjLDB4ZjgsMHgxZiwKMHhlMCwweDA3Cn07',
        22: 'I2RlZmluZSBpbWFnZV93aWR0aCAyMgojZGVmaW5lIGltYWdlX2hlaWdodCAyMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgzZiwweDAwLDB4ZTAsMHhmZiwweDAxLDB4ZjAsMHhmZiwweDAzLDB4ZjgsMHhjMCwweDA3LDB4M2MsMHgwMCwweDBmLAoweDFlLDB4MDAsMHgxZSwweDBlLDB4MDAsMHgxYywweDBlLDB4MDAsMHgxYywweDA3LDB4MDAsMHgzOCwweDA3LDB4MDAsMHgzOCwKMHgwNywweDAwLDB4MzgsMHgwNywweDAwLDB4MzgsMHgwNywweDAwLDB4MzgsMHgwNywweDAwLDB4MzgsMHgwZiwweDAwLDB4MWMsCjB4MGUsMHgwMCwweDFjLDB4MWUsMHgwMCwweDFlLDB4M2MsMHgwMCwweDBmLDB4ZjgsMHhjMCwweDA3LDB4ZjAsMHhmZiwweDAzLAoweGUwLDB4ZmYsMHgwMSwweDAwLDB4M2YsMHgwMAp9Ow==',
        24: 'I2RlZmluZSBpbWFnZV93aWR0aCAyNAojZGVmaW5lIGltYWdlX2hlaWdodCAyNApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHg3ZSwweDAwLDB4YzAsMHhmZiwweDAzLDB4ZTAsMHhmZiwweDA3LDB4ZjAsMHg4MSwweDBmLDB4NzgsMHgwMCwweDFlLAoweDNjLDB4MDAsMHgzYywweDFlLDB4MDAsMHg3OCwweDBlLDB4MDAsMHg3MCwweDBmLDB4MDAsMHhmMCwweDA3LDB4MDAsMHhlMCwKMHgwNywweDAwLDB4ZTAsMHgwNywweDAwLDB4ZTAsMHgwNywweDAwLDB4ZTAsMHgwNywweDAwLDB4ZTAsMHgwNywweDAwLDB4ZTAsCjB4MGYsMHgwMCwweDcwLDB4MGUsMHgwMCwweDcwLDB4MWUsMHgwMCwweDc4LDB4M2MsMHgwMCwweDNjLDB4NzgsMHgwMCwweDFlLAoweGY4LDB4ODEsMHgwZiwweGUwLDB4ZmYsMHgwNywweGMwLDB4ZmYsMHgwMywweDAwLDB4ZmYsMHgwMAp9Ow==',
        32: 'I2RlZmluZSBpbWFnZV93aWR0aCAzMgojZGVmaW5lIGltYWdlX2hlaWdodCAzMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweGYwLDB4MGYsMHgwMCwweDAwLDB4ZmUsMHg3ZiwweDAwLDB4ODAsMHhmZiwweGZmLAoweDAxLDB4YzAsMHhmZiwweGZmLDB4MDMsMHhlMCwweDFmLDB4ZjgsMHgwNywweGYwLDB4MDMsMHhjMCwweDBmLDB4ZjgsMHgwMSwKMHg4MCwweDFmLDB4ZmMsMHgwMCwweDAwLDB4M2YsMHg3YywweDAwLDB4MDAsMHgzZSwweDNlLDB4MDAsMHgwMCwweDdjLDB4MWUsCjB4MDAsMHgwMCwweDc4LDB4MWUsMHgwMCwweDAwLDB4NzgsMHgwZiwweDAwLDB4MDAsMHhmOCwweDBmLDB4MDAsMHgwMCwweGYwLAoweDBmLDB4MDAsMHgwMCwweGYwLDB4MGYsMHgwMCwweDAwLDB4ZjAsMHgwZiwweDAwLDB4MDAsMHhmMCwweDBmLDB4MDAsMHgwMCwKMHhmMCwweDBmLDB4MDAsMHgwMCwweGYwLDB4MGYsMHgwMCwweDAwLDB4ZjgsMHgxZSwweDAwLDB4MDAsMHg3OCwweDFlLDB4MDAsCjB4MDAsMHg3OCwweDNlLDB4MDAsMHgwMCwweDdjLDB4N2MsMHgwMCwweDAwLDB4M2UsMHhmYywweDAwLDB4MDAsMHgzZiwweGY4LAoweDAxLDB4ODAsMHgxZiwweGYwLDB4MDMsMHhjMCwweDBmLDB4ZTAsMHgwZiwweGYwLDB4MDcsMHhjMCwweGZmLDB4ZmYsMHgwMywKMHg4MCwweGZmLDB4ZmYsMHgwMSwweDAwLDB4ZmUsMHg3ZiwweDAwCn07',
        48: 'I2RlZmluZSBpbWFnZV93aWR0aCA0OAojZGVmaW5lIGltYWdlX2hlaWdodCA0OApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweGY4LDB4MWYsMHgwMCwweDAwLDB4MDAsMHg4MCwweGZmLAoweGZmLDB4MDEsMHgwMCwweDAwLDB4ZTAsMHhmZiwweGZmLDB4MDcsMHgwMCwweDAwLDB4ZjgsMHhmZiwweGZmLDB4MWYsMHgwMCwKMHgwMCwweGZjLDB4ZmYsMHhmZiwweDNmLDB4MDAsMHgwMCwweGZlLDB4ZmYsMHhmZiwweDdmLDB4MDAsMHgwMCwweGZmLDB4MGYsCjB4ZjAsMHhmZiwweDAwLDB4ODAsMHhmZiwweDAxLDB4ODAsMHhmZiwweDAxLDB4YzAsMHg3ZiwweDAwLDB4MDAsMHhmZSwweDAzLAoweGUwLDB4MWYsMHgwMCwweDAwLDB4ZjgsMHgwNywweGYwLDB4MGYsMHgwMCwweDAwLDB4ZjAsMHgwZiwweGY4LDB4MDcsMHgwMCwKMHgwMCwweGUwLDB4MWYsMHhmOCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MWYsMHhmYywweDAxLDB4MDAsMHgwMCwweDgwLDB4M2YsCjB4ZmMsMHgwMSwweDAwLDB4MDAsMHg4MCwweDNmLDB4ZmUsMHgwMCwweDAwLDB4MDAsMHgwMCwweDdmLDB4ZmUsMHgwMCwweDAwLAoweDAwLDB4MDAsMHg3ZiwweDdlLDB4MDAsMHgwMCwweDAwLDB4MDAsMHg3ZSwweDdlLDB4MDAsMHgwMCwweDAwLDB4MDAsMHg3ZSwKMHg3ZiwweDAwLDB4MDAsMHgwMCwweDAwLDB4ZmUsMHgzZiwweDAwLDB4MDAsMHgwMCwweDAwLDB4ZmMsMHgzZiwweDAwLDB4MDAsCjB4MDAsMHgwMCwweGZjLDB4M2YsMHgwMCwweDAwLDB4MDAsMHgwMCwweGZjLDB4M2YsMHgwMCwweDAwLDB4MDAsMHgwMCwweGZjLAoweDNmLDB4MDAsMHgwMCwweDAwLDB4MDAsMHhmYywweDNmLDB4MDAsMHgwMCwweDAwLDB4MDAsMHhmYywweDNmLDB4MDAsMHgwMCwKMHgwMCwweDAwLDB4ZmMsMHgzZiwweDAwLDB4MDAsMHgwMCwweDAwLDB4ZmMsMHg3ZiwweDAwLDB4MDAsMHgwMCwweDAwLDB4ZmUsCjB4N2UsMHgwMCwweDAwLDB4MDAsMHgwMCwweDdlLDB4N2UsMHgwMCwweDAwLDB4MDAsMHgwMCwweDdlLDB4ZmUsMHgwMCwweDAwLAoweDAwLDB4MDAsMHg3ZiwweGZlLDB4MDAsMHgwMCwweDAwLDB4MDAsMHg3ZiwweGZjLDB4MDEsMHgwMCwweDAwLDB4ODAsMHgzZiwKMHhmYywweDAxLDB4MDAsMHgwMCwweDgwLDB4M2YsMHhmOCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MWYsMHhmOCwweDA3LDB4MDAsCjB4MDAsMHhlMCwweDFmLDB4ZjAsMHgwZiwweDAwLDB4MDAsMHhmMCwweDBmLDB4ZTAsMHgxZiwweDAwLDB4MDAsMHhmOCwweDA3LAoweGMwLDB4N2YsMHgwMCwweDAwLDB4ZmUsMHgwMywweDgwLDB4ZmYsMHgwMSwweDgwLDB4ZmYsMHgwMSwweDAwLDB4ZmYsMHgwZiwKMHhmMCwweGZmLDB4MDAsMHgwMCwweGZlLDB4ZmYsMHhmZiwweDdmLDB4MDAsMHgwMCwweGZjLDB4ZmYsMHhmZiwweDNmLDB4MDAsCjB4MDAsMHhmOCwweGZmLDB4ZmYsMHgxZiwweDAwLDB4MDAsMHhlMCwweGZmLDB4ZmYsMHgwNywweDAwLDB4MDAsMHg4MCwweGZmLAoweGZmLDB4MDEsMHgwMAp9Ow=='
    }

    selectimage = {
        16: 'I2RlZmluZSBpbWFnZV93aWR0aCAxNgojZGVmaW5lIGltYWdlX2hlaWdodCAxNgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4ZTAsMHgwNywweGY4LDB4MWYsMHgzYywweDNjLDB4MGUsMHg3MCwweDA2LDB4NjAsMHhjNywweGUzLDB4ZTMsMHhjNywweGUzLAoweGM3LDB4ZTMsMHhjNywweGUzLDB4YzcsMHhjNywweGUzLDB4MDYsMHg2MCwweDBlLDB4NzAsMHgzYywweDNjLDB4ZjgsMHgxZiwKMHhlMCwweDA3Cn07',
        22: 'I2RlZmluZSBpbWFnZV93aWR0aCAyMgojZGVmaW5lIGltYWdlX2hlaWdodCAyMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgzZiwweDAwLDB4ZTAsMHhmZiwweDAxLDB4ZjAsMHhmZiwweDAzLDB4ZjgsMHhjMCwweDA3LDB4M2MsMHgwMCwweDBmLAoweDFlLDB4MDAsMHgxZSwweDBlLDB4MDAsMHgxYywweDBlLDB4MWUsMHgxYywweDA3LDB4M2YsMHgzOCwweDg3LDB4N2YsMHgzOCwKMHg4NywweDdmLDB4MzgsMHg4NywweDdmLDB4MzgsMHg4NywweDdmLDB4MzgsMHgwNywweDNmLDB4MzgsMHgwZiwweDFlLDB4MWMsCjB4MGUsMHgwMCwweDFjLDB4MWUsMHgwMCwweDFlLDB4M2MsMHgwMCwweDBmLDB4ZjgsMHhjMCwweDA3LDB4ZjAsMHhmZiwweDAzLAoweGUwLDB4ZmYsMHgwMSwweDAwLDB4M2YsMHgwMAp9Ow==',
        24: 'I2RlZmluZSBpbWFnZV93aWR0aCAyNAojZGVmaW5lIGltYWdlX2hlaWdodCAyNApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHg3ZSwweDAwLDB4YzAsMHhmZiwweDAzLDB4ZTAsMHhmZiwweDA3LDB4ZjAsMHg4MSwweDBmLDB4NzgsMHgwMCwweDFlLAoweDNjLDB4MDAsMHgzYywweDFlLDB4MDAsMHg3OCwweDBlLDB4MDAsMHg3MCwweDBmLDB4M2UsMHhmMCwweDA3LDB4N2YsMHhlMCwKMHg4NywweGZmLDB4ZTAsMHg4NywweGZmLDB4ZTAsMHg4NywweGZmLDB4ZTAsMHg4NywweGZmLDB4ZTAsMHg4NywweGZmLDB4ZTAsCjB4MGYsMHg3ZiwweDcwLDB4MGUsMHgzZSwweDcwLDB4MWUsMHgwMCwweDc4LDB4M2MsMHgwMCwweDNjLDB4NzgsMHgwMCwweDFlLAoweGY4LDB4ODEsMHgwZiwweGUwLDB4ZmYsMHgwNywweGMwLDB4ZmYsMHgwMywweDAwLDB4ZmYsMHgwMAp9Ow==',
        32: 'I2RlZmluZSBpbWFnZV93aWR0aCAzMgojZGVmaW5lIGltYWdlX2hlaWdodCAzMgpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweGYwLDB4MGYsMHgwMCwweDAwLDB4ZmUsMHg3ZiwweDAwLDB4ODAsMHhmZiwweGZmLAoweDAxLDB4YzAsMHhmZiwweGZmLDB4MDMsMHhlMCwweDFmLDB4ZjgsMHgwNywweGYwLDB4MDMsMHhjMCwweDBmLDB4ZjgsMHgwMSwKMHg4MCwweDFmLDB4ZmMsMHgwMCwweDAwLDB4M2YsMHg3YywweDAwLDB4MDAsMHgzZSwweDNlLDB4MDAsMHgwMCwweDdjLDB4MWUsCjB4YzAsMHgwMywweDc4LDB4MWUsMHhmMCwweDBmLDB4NzgsMHgwZiwweGY4LDB4MWYsMHhmOCwweDBmLDB4ZjgsMHgxZiwweGYwLAoweDBmLDB4ZmMsMHgzZiwweGYwLDB4MGYsMHhmYywweDNmLDB4ZjAsMHgwZiwweGZjLDB4M2YsMHhmMCwweDBmLDB4ZmMsMHgzZiwKMHhmMCwweDBmLDB4ZmMsMHgxZiwweGYwLDB4MGYsMHhmOCwweDFmLDB4ZjgsMHgxZSwweGYwLDB4MGYsMHg3OCwweDFlLDB4YzAsCjB4MDMsMHg3OCwweDNlLDB4MDAsMHgwMCwweDdjLDB4N2MsMHgwMCwweDAwLDB4M2UsMHhmYywweDAwLDB4MDAsMHgzZiwweGY4LAoweDAxLDB4ODAsMHgxZiwweGYwLDB4MDMsMHhjMCwweDBmLDB4ZTAsMHgwZiwweGYwLDB4MDcsMHhjMCwweGZmLDB4ZmYsMHgwMywKMHg4MCwweGZmLDB4ZmYsMHgwMSwweDAwLDB4ZmUsMHg3ZiwweDAwCn07',
        48: 'I2RlZmluZSBpbWFnZV93aWR0aCA0OAojZGVmaW5lIGltYWdlX2hlaWdodCA0OApzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweGY4LDB4MWYsMHgwMCwweDAwLDB4MDAsMHg4MCwweGZmLAoweGZmLDB4MDEsMHgwMCwweDAwLDB4ZTAsMHhmZiwweGZmLDB4MDcsMHgwMCwweDAwLDB4ZjgsMHhmZiwweGZmLDB4MWYsMHgwMCwKMHgwMCwweGZjLDB4ZmYsMHhmZiwweDNmLDB4MDAsMHgwMCwweGZlLDB4ZmYsMHhmZiwweDdmLDB4MDAsMHgwMCwweGZmLDB4MGYsCjB4ZjAsMHhmZiwweDAwLDB4ODAsMHhmZiwweDAxLDB4ODAsMHhmZiwweDAxLDB4YzAsMHg3ZiwweDAwLDB4MDAsMHhmZSwweDAzLAoweGUwLDB4MWYsMHgwMCwweDAwLDB4ZjgsMHgwNywweGYwLDB4MGYsMHgwMCwweDAwLDB4ZjAsMHgwZiwweGY4LDB4MDcsMHgwMCwKMHgwMCwweGUwLDB4MWYsMHhmOCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MWYsMHhmYywweDAxLDB4MDAsMHgwMCwweDgwLDB4M2YsCjB4ZmMsMHgwMSwweDAwLDB4MDAsMHg4MCwweDNmLDB4ZmUsMHgwMCwweGUwLDB4MDcsMHgwMCwweDdmLDB4ZmUsMHgwMCwweGY4LAoweDFmLDB4MDAsMHg3ZiwweDdlLDB4MDAsMHhmYywweDNmLDB4MDAsMHg3ZSwweDdlLDB4MDAsMHhmZSwweDdmLDB4MDAsMHg3ZSwKMHg3ZiwweDAwLDB4ZmYsMHhmZiwweDAwLDB4ZmUsMHgzZiwweDAwLDB4ZmYsMHhmZiwweDAwLDB4ZmMsMHgzZiwweDgwLDB4ZmYsCjB4ZmYsMHgwMSwweGZjLDB4M2YsMHg4MCwweGZmLDB4ZmYsMHgwMSwweGZjLDB4M2YsMHg4MCwweGZmLDB4ZmYsMHgwMSwweGZjLAoweDNmLDB4ODAsMHhmZiwweGZmLDB4MDEsMHhmYywweDNmLDB4ODAsMHhmZiwweGZmLDB4MDEsMHhmYywweDNmLDB4ODAsMHhmZiwKMHhmZiwweDAxLDB4ZmMsMHgzZiwweDAwLDB4ZmYsMHhmZiwweDAwLDB4ZmMsMHg3ZiwweDAwLDB4ZmYsMHhmZiwweDAwLDB4ZmUsCjB4N2UsMHgwMCwweGZlLDB4N2YsMHgwMCwweDdlLDB4N2UsMHgwMCwweGZjLDB4M2YsMHgwMCwweDdlLDB4ZmUsMHgwMCwweGY4LAoweDFmLDB4MDAsMHg3ZiwweGZlLDB4MDAsMHhlMCwweDA3LDB4MDAsMHg3ZiwweGZjLDB4MDEsMHgwMCwweDAwLDB4ODAsMHgzZiwKMHhmYywweDAxLDB4MDAsMHgwMCwweDgwLDB4M2YsMHhmOCwweDAzLDB4MDAsMHgwMCwweGMwLDB4MWYsMHhmOCwweDA3LDB4MDAsCjB4MDAsMHhlMCwweDFmLDB4ZjAsMHgwZiwweDAwLDB4MDAsMHhmMCwweDBmLDB4ZTAsMHgxZiwweDAwLDB4MDAsMHhmOCwweDA3LAoweGMwLDB4N2YsMHgwMCwweDAwLDB4ZmUsMHgwMywweDgwLDB4ZmYsMHgwMSwweDgwLDB4ZmYsMHgwMSwweDAwLDB4ZmYsMHgwZiwKMHhmMCwweGZmLDB4MDAsMHgwMCwweGZlLDB4ZmYsMHhmZiwweDdmLDB4MDAsMHgwMCwweGZjLDB4ZmYsMHhmZiwweDNmLDB4MDAsCjB4MDAsMHhmOCwweGZmLDB4ZmYsMHgxZiwweDAwLDB4MDAsMHhlMCwweGZmLDB4ZmYsMHgwNywweDAwLDB4MDAsMHg4MCwweGZmLAoweGZmLDB4MDEsMHgwMAp9Ow=='
    }

    def __init__(self, master, size=22, **kw):
        image = Metro_Radiobutton.image[size]
        
        if isinstance(image, basestring):
            Metro_Radiobutton.image[size] = image = tk.BitmapImage(data=base64.b64decode(image))

        selectimage = Metro_Radiobutton.selectimage[size]
        
        if isinstance(selectimage, basestring):
            Metro_Radiobutton.selectimage[size] = selectimage = tk.BitmapImage(data=base64.b64decode(selectimage))

        background = get_background_of_widget(master)
        tk.Radiobutton.__init__(self, master, indicatoron=0, background=background, selectcolor=background, activebackground=background, selectimage=selectimage, image=image, highlightthickness=0, borderwidth=0, **kw)

def initialize_font():
    if "Open Sans" in tkFont.families():
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Open Sans", size=11)
        
        default_font = tkFont.nametofont("TkTextFont")
        default_font.configure(family="Open Sans", size=11)

if __name__ == "__main__":
    
    try:
        from Tkinter import Tk
        from tkMessageBox import showinfo
    except ImportError:
        from tkinter import Tk
        from tkinter.messagebox import showinfo
        
    root = Tk()
    
    initialize_font()

    page = Container(root, bg="white", bd=1, relief=RIDGE, padx=10, pady=10)
    page.pack()

    row = Frame(page)
    row.pack()

    metro_labelframe = Metro_LabelFrame(row, title="This is the title")
    metro_labelframe.pack(side=LEFT, padx=6, pady=9)
    for i  in range(5):
        Label(metro_labelframe.body, text="This is line number %i"%i).pack(expand=True, fill=BOTH)

    metro_labelframe = Metro_LabelFrame(row, title="This is the title")
    metro_labelframe.pack(side=LEFT, padx=6, pady=9)
    
    Label(metro_labelframe.body, text="One line").pack(anchor=W)
    Label(metro_labelframe.body, text="Another line").pack(anchor=W)
    Label(metro_labelframe.body, text="more lines...").pack(anchor=W)
    quote = QuoteFrame(metro_labelframe.body, text="blah.. blah..blah..blah..blah..blah..")
    quote.pack()

    Label(metro_labelframe.body, text="more body here...").pack(anchor=W)
    
    def callback():
        import webbrowser
        webbrowser.open_new(r"http://www.google.com")

    link = Link_Button(row, text="Google Hyperlink", action=callback)
    link.pack(padx=10, pady=10)
    
    row = Frame(page)
    row.pack()

    metro_panel = Primary_Panel(row, "Primary Panel", width=250)
    metro_panel.pack(padx=10, pady=7, side=LEFT)
    Label(metro_panel.body, text="Panel content").pack(anchor=W)

    metro_panel = Info_Panel(row, "Info Panel", width=250)
    metro_panel.pack(padx=10, pady=7, side=LEFT)
    Label(metro_panel.body, text="Panel content").pack(anchor=W)

    metro_panel = Danger_Panel(row, "Danger Panel", width=300)
    metro_panel.pack(padx=10, pady=7, side=LEFT)
    Label(metro_panel.body, text="Panel content").pack(anchor=W)

    metro_panel = Success_Panel(row, "Success Panel", width=250)
    metro_panel.pack(padx=10, pady=7, side=LEFT)
    Label(metro_panel.body, text="Panel content").pack(anchor=W)

    metro_panel = Warning_Panel(row, "Warning Panel", width=250)
    metro_panel.pack(padx=10, pady=7)
    Label(metro_panel.body, text="Panel content").pack(anchor=W)
    
    row = Frame(page)
    row.pack(pady=4, fill=X)

    Label(row, text="Metro button:").pack(side=LEFT)
    Metro_Button(row, "Search", "#60a917").pack(side=LEFT, padx=4)
    Metro_Button(row, "Run", "red").pack(side=LEFT, padx=4)
    Metro_Button(row, "Login", "#8b5a2b").pack(side=LEFT, padx=4)
    
    row = Frame(page)
    row.pack(pady=4, fill=X)

    def command(text):
        showinfo("search command", "searching:%s"%text)

    searchbox = Search_Box(page, command=command, placeholder="Type and press enter", entry_highlightthickness=0)
    searchbox.pack(anchor=W)
    
    row = Frame(page)
    row.pack(pady=4, fill=X)

    Metro_Checkbutton(row).pack(side=LEFT)
    Label(row, text="option1").pack(padx=(2,0), side=LEFT)

    var = StringVar()

    row = Frame(page)
    row.pack(pady=4, fill=X)

    Metro_Radiobutton(row,variable=var, value="0").pack(side=LEFT)
    Label(row, text="option2").pack(padx=(2,0),side=LEFT)
    Metro_Radiobutton(row,variable=var, value="1").pack(side=LEFT, padx=(10,0))
    Label(row, text="option3").pack(padx=(2,0), side=LEFT)

    Label(page, text="This is an entry:").pack(anchor=W)
    Metro_Entry(page).pack(anchor=W)
    root.mainloop()
