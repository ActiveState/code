# Version: 0.2
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print("Author's email: ", "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))

# Based on these codes:
#   https://github.com/alejandroautalan/pygubu/blob/master/pygubu/widgets/tkscrolledframe.py
#   http://wiki.tcl.tk/9223 


try:
    from Tkinter import Frame
    from ttk import Scrollbar
    
    from Tkconstants import *
except ImportError:
    from tkinter import Frame
    from tkinter.ttk import Scrollbar
    
    from tkinter.constants import *

import platform

OS = platform.system()

class Mousewheel_Support(object):    

    # implemetation of singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, root, horizontal_factor = 2, vertical_factor=2):
        
        self._active_area = None
        
        if isinstance(horizontal_factor, int):
            self.horizontal_factor = horizontal_factor
        else:
            raise Exception("Vertical factor must be an integer.")

        if isinstance(vertical_factor, int):
            self.vertical_factor = vertical_factor
        else:
            raise Exception("Horizontal factor must be an integer.")

        if OS == "Linux" :
            root.bind_all('<4>', self._on_mousewheel,  add='+')
            root.bind_all('<5>', self._on_mousewheel,  add='+')
        else:
            # Windows and MacOS
            root.bind_all("<MouseWheel>", self._on_mousewheel,  add='+')

    def _on_mousewheel(self,event):
        if self._active_area:
            self._active_area.onMouseWheel(event)

    def _mousewheel_bind(self, widget):
        self._active_area = widget

    def _mousewheel_unbind(self):
        self._active_area = None

    def add_support_to(self, widget=None, xscrollbar=None, yscrollbar=None, what="units", horizontal_factor=None, vertical_factor=None):
        if xscrollbar is None and yscrollbar is None:
            return

        if xscrollbar is not None:
            horizontal_factor = horizontal_factor or self.horizontal_factor

            xscrollbar.onMouseWheel = self._make_mouse_wheel_handler(widget,'x', self.horizontal_factor, what)
            xscrollbar.bind('<Enter>', lambda event, scrollbar=xscrollbar: self._mousewheel_bind(scrollbar) )
            xscrollbar.bind('<Leave>', lambda event: self._mousewheel_unbind())

        if yscrollbar is not None:
            vertical_factor = vertical_factor or self.vertical_factor

            yscrollbar.onMouseWheel = self._make_mouse_wheel_handler(widget,'y', self.vertical_factor, what)
            yscrollbar.bind('<Enter>', lambda event, scrollbar=yscrollbar: self._mousewheel_bind(scrollbar) )
            yscrollbar.bind('<Leave>', lambda event: self._mousewheel_unbind())

        main_scrollbar = yscrollbar if yscrollbar is not None else xscrollbar
        
        if widget is not None:
            if isinstance(widget, list) or isinstance(widget, tuple):
                list_of_widgets = widget
                for widget in list_of_widgets:
                    widget.bind('<Enter>',lambda event: self._mousewheel_bind(widget))
                    widget.bind('<Leave>', lambda event: self._mousewheel_unbind())

                    widget.onMouseWheel = main_scrollbar.onMouseWheel
            else:
                widget.bind('<Enter>',lambda event: self._mousewheel_bind(widget))
                widget.bind('<Leave>', lambda event: self._mousewheel_unbind())

                widget.onMouseWheel = main_scrollbar.onMouseWheel

    @staticmethod
    def _make_mouse_wheel_handler(widget, orient, factor = 1, what="units"):
        view_command = getattr(widget, orient+'view')
        
        if OS == 'Linux':
            def onMouseWheel(event):
                if event.num == 4:
                    view_command("scroll",(-1)*factor, what)
                elif event.num == 5:
                    view_command("scroll",factor, what) 
                
        elif OS == 'Windows':
            def onMouseWheel(event):        
                view_command("scroll",(-1)*int((event.delta/120)*factor), what) 
        
        elif OS == 'Darwin':
            def onMouseWheel(event):        
                view_command("scroll",event.delta, what)
        
        return onMouseWheel

class Scrolling_Area(Frame, object):

    def __init__(self, master, width=None, height=None, mousewheel_speed = 2, scroll_horizontally=True, xscrollbar=None, scroll_vertically=True, yscrollbar=None, outer_background=None, inner_frame=Frame, **kw):
        super(Scrolling_Area, self).__init__(master, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._clipper = Frame(self, background=outer_background, width=width, height=height)
        self._clipper.grid(row=0, column=0, sticky=N+E+W+S)
        
        self._width = width
        self._height = height

        self.innerframe = inner_frame(self._clipper, padx=0, pady=0, highlightthickness=0)
        self.innerframe.place(in_=self._clipper, x=0, y=0)

        if scroll_vertically:
            if yscrollbar is not None:
                self.yscrollbar = yscrollbar
            else:
                self.yscrollbar = Scrollbar(self, orient=VERTICAL)
                self.yscrollbar.grid(row=0, column=1,sticky=N+S)
                
            self.yscrollbar.set(0.0, 1.0)
            self.yscrollbar.config(command=self.yview)
        else:
            self.yscrollbar = None
            
        self._scroll_vertically = scroll_vertically

        if scroll_horizontally:
            if xscrollbar is not None:
                self.xscrollbar = xscrollbar
            else:
                self.xscrollbar = Scrollbar(self, orient=HORIZONTAL)
                self.xscrollbar.grid(row=1, column=0, sticky=E+W)
            
            self.xscrollbar.set(0.0, 1.0)
            self.xscrollbar.config(command=self.xview)
        else:
            self.xscrollbar = None
            
        self._scroll_horizontally = scroll_horizontally

        self._jfraction=0.05
        self._startX = 0
        self._startY = 0       

        # Whenever the clipping window or scrolled frame change size,
        # update the scrollbars.
        self.innerframe.bind('<Configure>', self._on_configure)
        self._clipper.bind('<Configure>',  self._on_configure)
        
        self.innerframe.xview = self.xview
        self.innerframe.yview = self.yview

        Mousewheel_Support(self).add_support_to(self.innerframe, xscrollbar=self.xscrollbar, yscrollbar=self.yscrollbar)

    def update_viewport(self):
        # compute new height and width
        self.update()
        frameHeight = float(self.innerframe.winfo_reqheight())
        frameWidth = float(self.innerframe.winfo_reqwidth())
        
        if self._width is not None:
            width = min(self._width, frameWidth)
        else:
            width = self._frameWidth

        if self._height is not None:
            height = min(self._height, frameHeight)
        else:
            height = self._frameHeight
        
        self._clipper.configure(width=width, height=height)

    def _on_configure(self, event):
        self._frameHeight = float(self.innerframe.winfo_reqheight())
        self._frameWidth = float(self.innerframe.winfo_reqwidth())

        # resize the visible part
        if self._scroll_horizontally:
            self.xview("scroll", 0, "unit")
            
        if self._scroll_vertically:
            self.yview("scroll", 0, "unit")       

    def xview(self, mode = None, value = None, units = None):
        value = float(value)

        clipperWidth = self._clipper.winfo_width()
        frameWidth = self._frameWidth 
        
        _startX = self._startX

        if mode is None:
            return self.xscrollbar.get()
        elif mode == 'moveto':
            # absolute movement
            self._startX = int(value * frameWidth)
        else: 
            # mode == 'scroll'
            # relative movement
            if units == 'units':
                jump = int(clipperWidth * self._jfraction)
            else:
                jump = clipperWidth
            self._startX = self._startX + value * jump

        if frameWidth <= clipperWidth:
            # The scrolled frame is smaller than the clipping window.

            self._startX = 0
            hi = 1.0
            #use expand by default
            relwidth = 1
        else:
            # The scrolled frame is larger than the clipping window.
            #use expand by default
            if self._startX + clipperWidth > frameWidth:
                self._startX = frameWidth - clipperWidth
                hi = 1.0
            else:
                if self._startX < 0:
                    self._startX = 0
                hi = (self._startX + clipperWidth) / frameWidth
            relwidth = ''

        if self._startX != _startX:
            # Position frame relative to clipper.
            self.innerframe.place(x = -self._startX, relwidth = relwidth)
        
        lo = self._startX / frameWidth
        self.xscrollbar.set(lo, hi)

    def yview(self, mode = None, value = None, units = None):
        value = float(value)
        clipperHeight = self._clipper.winfo_height()
        frameHeight = self._frameHeight
        
        _startY = self._startY

        if mode is None:
            return self.yscrollbar.get()
        elif mode == 'moveto':
            self._startY = value * frameHeight
        else: # mode == 'scroll'
            if units == 'units':
                jump = int(clipperHeight * self._jfraction)
            else:
                jump = clipperHeight
            self._startY = self._startY + value * jump

        if frameHeight <= clipperHeight:
            # The scrolled frame is smaller than the clipping window.

            self._startY = 0
            hi = 1.0
            # use expand by default
            relheight = 1
        else:
            # The scrolled frame is larger than the clipping window.
            # use expand by default 
            if self._startY + clipperHeight > frameHeight:
                self._startY = frameHeight - clipperHeight
                hi = 1.0
            else:
                if self._startY < 0:
                    self._startY = 0
                hi = (self._startY + clipperHeight) / frameHeight
            relheight = ''

        if self._startY != _startY:
            # Position frame relative to clipper.
            self.innerframe.place(y = -self._startY, relheight = relheight)

        lo = self._startY / frameHeight
        self.yscrollbar.set(lo, hi)

if __name__== '__main__':
    try:
        from Tkinter import Tk, Frame, Label
    except ImportError:
        from tkinter import Tk, Label, Frame
    
    root = Tk()
    root.geometry("200x300")
    
    scrolling_area = Scrolling_Area(root)
    scrolling_area.pack(expand=1, fill="both")
    
    for i in range(20):
        rowFrame = Frame(scrolling_area.innerframe)
        rowFrame.pack()
        for j in range(8):
            Label(rowFrame, text="Label %s, %s" % (str(i), str(j))).pack(side="left")


    root.mainloop()
