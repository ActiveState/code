# Author: Miguel Martinez Lopez

try:
    import Tkinter as tk
    from Tkconstants import *    
except ImportError:
    import tkinter as tk
    from tkinter.constants import *

import base64

# python 2 and 3 compatibility
try:
  basestring
except NameError:
  basestring = str

def center_toplevel(toplevel):
    x = (toplevel.winfo_screenwidth() - toplevel.winfo_reqwidth())/2
    y = (toplevel.winfo_screenheight() - toplevel.winfo_height())/2

    toplevel.geometry("+%d+%d" % (x, y))

class Draggable_Window(tk.Toplevel):

    def __init__(self, master=None, disable_dragging =False, release_command = None):
        tk.Toplevel.__init__(self, master)

        if disable_dragging == False:
            self.bind('<Button-1>', self.initiate_motion)
            self.bind('<ButtonRelease-1>', self.release_dragging)

        self.release_command = release_command

    def initiate_motion(self, event):
        # This is another possibility:
        #   OriX, OriY = self.window_position()
        #   self.deltaX = event.x_root - OriX
        #   self.deltaY = event.y_root - OriY
        #
        self.deltaX = event.x_root - self.winfo_x()
        self.deltaY = event.y_root - self.winfo_y()

        self.bind('<Motion>', self.drag_window)

    def drag_window(self, event):
        new_x = event.x_root - self.deltaX
        new_y = event.y_root - self.deltaY

        if new_x < 0 :
            new_x = 0

        if new_y < 0 :
            new_y = 0

        self.wm_geometry("+%s+%s" % (new_x, new_y))

    def release_dragging(self, event):
        self.unbind('<Motion>')

        if self.release_command != None :
            self.release_command()

    def disable_dragging(self) :
        self.unbind('<Button-1>')
        self.unbind('<ButtonRelease-1>')
        self.unbind('<Motion>')

    def enable_dragging(self):
        self.bind('<Button-1>', self.initiate_motion)
        self.bind('<ButtonRelease-1>', self.release_dragging)

class Control_Button(tk.Label):
    def __init__(self, master, active_background=None, active_foreground=None, command=None, **kwargs):
        tk.Label.__init__(self, master, **kwargs)
        
        self._active_background = active_background
        self._active_foreground = active_foreground
        self._background = self.cget("background")
        self._foreground = self.cget("foreground")
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
            
        if command is not None:
            self.bind("<1>", lambda event: command())
            
    def _on_enter(self, event):
        self.configure(background=self._active_background, foreground=self._active_foreground)

    def _on_leave(self, event):
        self.configure(background=self._background, foreground=self._foreground)

class Metro_Dialog(Draggable_Window):
    WINDOW_ICON = "I2RlZmluZSBpbWFnZV93aWR0aCAxOQojZGVmaW5lIGltYWdlX2hlaWdodCAxOQpzdGF0aWMgY2hhciBpbWFnZV9iaXRzW10gPSB7CjB4MDAsMHgwMCwweDAwLDB4MDAsMHgwMCwweDAyLDB4MDAsMHhmYywweDAzLDB4NzgsMHhmZiwweDAzLDB4N2YsMHhmZiwweDAzLAoweDdmLDB4ZmYsMHgwMywweDdmLDB4ZmYsMHgwMywweDdmLDB4ZmYsMHgwMywweDdmLDB4ZmYsMHgwMywweDdmLDB4ZmYsMHgwMywKMHgwMCwweDAwLDB4MDAsMHg3ZiwweGZmLDB4MDMsMHg3ZiwweGZmLDB4MDMsMHg3ZiwweGZmLDB4MDMsMHg3ZiwweGZmLDB4MDMsCjB4N2YsMHhmZiwweDAzLDB4N2YsMHhmZiwweDAzLDB4NDAsMHhmZiwweDAzLDB4MDAsMHhlMCwweDAzCn07"
    CLOSE_ICON = "I2RlZmluZSB4Ml93aWR0aCA0NQojZGVmaW5lIHgyX2hlaWdodCAyMApzdGF0aWMgY2hhciB4Ml9iaXRzW10gPSB7CiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgxOCwgMHgwNiwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgzMCwgMHgwMywgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHhFMCwgMHgwMSwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHhDMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHhFMCwgMHgwMSwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgzMCwgMHgwMywgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgxOCwgMHgwNiwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgfTsK"
    MAXIMIZE_ICON = "I2RlZmluZSBtYXhpbWl6ZV93aWR0aCAyMAojZGVmaW5lIG1heGltaXplX2hlaWdodCAyMApzdGF0aWMgY2hhciBtYXhpbWl6ZV9iaXRzW10gPSB7CiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHhFMCwgMHg3RiwgMHgwMCwgMHhFMCwgMHg3RiwgMHgwMCwgCiAgMHgyMCwgMHg0MCwgMHgwMCwgMHgyMCwgMHg0MCwgMHgwMCwgMHgyMCwgMHg0MCwgMHgwMCwgMHgyMCwgMHg0MCwgMHgwMCwgCiAgMHgyMCwgMHg0MCwgMHgwMCwgMHhFMCwgMHg3RiwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgfTsK"
    MINIMIZE_ICON = "I2RlZmluZSBtaW5pbWl6ZV93aWR0aCAyMAojZGVmaW5lIG1pbmltaXplX2hlaWdodCAyMApzdGF0aWMgY2hhciBtaW5pbWl6ZV9iaXRzW10gPSB7CiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHhDMCwgMHgzRiwgMHgwMCwgMHhDMCwgMHgzRiwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgfTsK"
    RESTORE_ICON = "I2RlZmluZSByZXN0b3JlX3dpZHRoIDIwCiNkZWZpbmUgcmVzdG9yZV9oZWlnaHQgMjAKc3RhdGljIGNoYXIgcmVzdG9yZV9iaXRzW10gPSB7CiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHg4MCwgMHg3RiwgMHgwMCwgMHgwMCwgMHg0MCwgMHgwMCwgMHhFMCwgMHg1RiwgMHgwMCwgCiAgMHhFMCwgMHg1RiwgMHgwMCwgMHgyMCwgMHg1OCwgMHgwMCwgMHgyMCwgMHg1MCwgMHgwMCwgMHgyMCwgMHg1MCwgMHgwMCwgCiAgMHgyMCwgMHg1MCwgMHgwMCwgMHgyMCwgMHgxMCwgMHgwMCwgMHhFMCwgMHgxRiwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgMHgwMCwgCiAgfTsK"

    HEADER_BACKGROUND = "brown"
    HEADER_FOREGROUND = "white"
    ICON_FOREGROUND = "white"
    BUTTON_ACTIVEBACKGROUND = "#CDE6F7"
    BUTTON_ACTIVEFOREGROUND = "#2A8DD4"
    BUTTON_BACKGROUND = "white"
    BUTTON_FOREGROUND = "#777777"
    BODY_BACKGROUND = "white"
    BORDERWIDTH = 2

    def __init__(self, master, title, width=None, height=None, header_background=None, header_foreground=None, icon_foreground=None, button_activebackground=None, button_activeforeground=None, button_background=None, button_foreground=None ,body_background=None, borderwidth=None, maximize_button=True, minimize_button=True, close_button=True, icon=None, center_on_screen=False):
        if header_background is None:
            header_background = self.HEADER_BACKGROUND
        
        if header_foreground is None:
            header_foreground = self.HEADER_FOREGROUND
            
        if icon_foreground is None:
            icon_foreground = self.ICON_FOREGROUND
            
        if button_activebackground is None:
           button_activebackground = self.BUTTON_ACTIVEBACKGROUND
        
        if button_activeforeground is None:
            button_activeforeground = self.BUTTON_ACTIVEFOREGROUND
        
        if button_background is None:
            button_background = self.BUTTON_BACKGROUND
        
        if button_foreground is None:
            button_foreground = self.BUTTON_FOREGROUND
        
        if body_background is None:
            body_background = self.BODY_BACKGROUND
            
        if borderwidth is None:
            borderwidth = self.BORDERWIDTH

        Draggable_Window.__init__(self, master)

        self.wm_attributes('-topmost', True)
        self.overrideredirect(True)
        
        outer_frame = tk.Frame(self, highlightbackground=header_background, highlightcolor=header_background, highlightthickness=borderwidth)
        outer_frame.pack(expand=True, fill=BOTH)

        self._header = tk.Frame(outer_frame, background=header_background, padx=6, pady=6)
        self._header.pack(fill=X)

        if icon is None:
            if isinstance(Metro_Dialog.WINDOW_ICON, basestring):
                data = base64.b64decode(Metro_Dialog.WINDOW_ICON)
                Metro_Dialog.WINDOW_ICON = tk.BitmapImage(data=data)
                
            icon = Metro_Dialog.WINDOW_ICON

        if isinstance(icon, tk.BitmapImage):
            icon.configure(foreground=icon_foreground)

        if close_button:
            if isinstance(Metro_Dialog.CLOSE_ICON, basestring):
                data = base64.b64decode(Metro_Dialog.CLOSE_ICON)
                Metro_Dialog.CLOSE_ICON = tk.BitmapImage(data=data, foreground=button_foreground)
    
            self._close_button = Control_Button(self._header, foreground=button_foreground, background=button_background, active_background=button_activebackground, image=Metro_Dialog.CLOSE_ICON, command=self.close)
            self._close_button.pack(side=RIGHT, padx=(1,0))

        if maximize_button:
            if isinstance(Metro_Dialog.MAXIMIZE_ICON, basestring):
                data = base64.b64decode(Metro_Dialog.MAXIMIZE_ICON)
                Metro_Dialog.MAXIMIZE_ICON = tk.BitmapImage(data=data, foreground=button_foreground)
            
            self._maximize_button = Control_Button(self._header, foreground=button_foreground, background=button_background, active_background=button_activebackground, image=Metro_Dialog.MAXIMIZE_ICON, command=self.maximize)
            self._maximize_button.pack(side=RIGHT, padx=(1,0))

        if minimize_button:
            if isinstance(Metro_Dialog.MINIMIZE_ICON, basestring):
                data = base64.b64decode(Metro_Dialog.MINIMIZE_ICON)
                Metro_Dialog.MINIMIZE_ICON = tk.BitmapImage(data=data, foreground=button_foreground)

            self._minimize_button = Control_Button(self._header, foreground=button_foreground, background=button_background, active_background=button_activebackground, active_foreground=button_activeforeground, image=Metro_Dialog.MINIMIZE_ICON, command=self.minimize)
            self._minimize_button.pack(side=RIGHT, padx=(1,0))

        self._borderwidth = borderwidth

        self._icon_label = tk.Label(self._header, image=icon, background=header_background)
        self._icon_label.pack(side=LEFT)

        self._title = title
        self._title_label = tk.Label(self._header, text=title, foreground=header_foreground, background=header_background)
        self._title_label.pack(side=LEFT, padx=6)
        
        self.body = tk.Frame(outer_frame, padx=4, pady=4, background = body_background)
        self.body.pack(expand=True, fill=BOTH)

        self._width = width
        self._height = height
        
        self._is_maximized = True

        if center_on_screen:
            self.center_on_screen()

    def close(self):
        self.destroy()

    def maximize(self):
        if self._is_maximized: return

        self.body.pack(expand=True, fill=BOTH)
        self.geometry("%dx%d"%(self._width, self._height))
        
        self._is_maximized = True

    def minimize(self):
        if not self._is_maximized: return

        if self._width is None:
            self._width = self.winfo_width()
            
        if self._height is None:
            self._height = self.winfo_height()

        width = self._width
        height = self._header.winfo_reqheight() + 2*self._borderwidth

        self.body.pack_forget()
        self.geometry("%dx%d"%(width,height))
        
        self._is_maximized = False

    def set_position(self, x, y):
        self.geometry("+%d+%d" % (x, y))

    def center_on_screen(self):
        center_toplevel(self)

if __name__ == "__main__":
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root = Tk()
    dialog = Metro_Dialog(root, title="This is my title", center_on_screen=True)
    tk.Label(dialog.body, background="white", text="this is a label").pack()

    root.mainloop()
