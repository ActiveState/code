# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print "Author's email: ", "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex")

try:
   import Tkinter as tk
   import ttk
except ImportError:
   import tkinter as tk
   from tkinter import ttk


class MouseWheel(object):
    def __init__(self, root, factor = 0.5):
        self.activeArea = None
        self.factor = factor

        import platform
        os = platform.system()

        if os == "Linux" :
            root.bind_all('<4>', self.onMouseWheel,  add='+')
            root.bind_all('<5>', self.onMouseWheel,  add='+')
        else:
            # Windows and MacOS
            root.bind_all("<MouseWheel>", self.onMouseWheel,  add='+')

    def onMouseWheel(self,event):
        if self.activeArea:
            self.activeArea.onMouseWheel(event.delta)

    def mouseWheel_bind(self, widget):
        self.activeArea = widget

    def mouseWheel_unbind(self):
        self.activeArea = None

    def add_scrolling(self, scrollingArea, xscrollbar=None, yscrollbar=None):
        scrollingArea.bind('<Enter>',lambda event: self.mouseWheel_bind(scrollingArea))
        scrollingArea.bind('<Leave>', lambda event: self.mouseWheel_unbind())

        if xscrollbar and not hasattr(xscrollbar, 'onMouseWheel'):
            setattr(xscrollbar, 'onMouseWheel', lambda delta: scrollingArea.xview("scroll",(-1)*int(delta/(120*self.factor)),"units" ) )

        if yscrollbar and not hasattr(yscrollbar, 'onMouseWheel'):
            setattr(yscrollbar, 'onMouseWheel', lambda delta: scrollingArea.yview("scroll",(-1)*int(delta/(120*self.factor)),"units" ) )

        active_scrollbar_on_mouse_wheel = yscrollbar or xscrollbar
        if active_scrollbar_on_mouse_wheel:
            setattr(scrollingArea, 'onMouseWheel', active_scrollbar_on_mouse_wheel.onMouseWheel)

        for scrollbar in (xscrollbar, yscrollbar):
            if scrollbar:
                scrollbar.bind('<Enter>', lambda event, scrollbar=scrollbar: self.mouseWheel_bind(scrollbar) )
                scrollbar.bind('<Leave>', lambda event: self.mouseWheel_unbind())


class simultaneousScrollbar(ttk.Scrollbar):
    def __init__(self, master, factor = 0.5, **kwargs):
        self.__scrollableWidgets = []

        if 'orient' in kwargs:
            if kwargs['orient']== tk.VERTICAL:
                self.__orientLabel = 'y'
            elif kwargs['orient']== tk.HORIZONTAL:
                self.__orientLabel = 'x'
            else:
                raise Exception("Bad 'orient' argument in scrollbar.")
        else:
            self.__orientLabel = 'y'

        kwargs['command'] = self.onScroll
        self.factor = factor

        ttk.Scrollbar.__init__(self, master, **kwargs)



    def add_ScrollableArea(self, *scrollableWidgets):
        for widget in scrollableWidgets:
            self.__scrollableWidgets.append(widget)
            widget[self.__orientLabel+'scrollcommand']=self.set

    def onScroll(self, *args):
        for widget in self.__scrollableWidgets:
            getattr(widget, self.__orientLabel+'view')(*args)

    def onMouseWheel(self, delta):
        for widget in self.__scrollableWidgets:
            getattr(widget, self.__orientLabel+'view')("scroll",(-1)*int(delta/(120*self.factor)),"units" )

def test():
    root = tk.Tk()

    scrollbar = simultaneousScrollbar(root, orient=tk.HORIZONTAL)
    scrollbar.pack(side=tk.TOP, fill=tk.X)

    emptySpace = tk.Frame(root, height=18)
    emptySpace.pack()

    tk.Label(root, text='First scrolled frame:').pack(anchor=tk.W)
    canvas1 = tk.Canvas(root, width=300, height=100)
    canvas1.pack(anchor=tk.NW)

    frame1= tk.Frame(canvas1)
    frame1.pack()

    for i in range(20):
        tk.Label(frame1, text="Label "+str(i)).pack(side=tk.LEFT)

    canvas1.create_window(0, 0, window=frame1, anchor='nw')

    canvas1.update_idletasks()

    canvas1['scrollregion'] = (0,0,frame1.winfo_reqwidth(), frame1.winfo_reqheight())

    tk.Label(root, text='Second scrolled frame:').pack(anchor=tk.W)
    canvas2 = tk.Canvas(root,width=300, height=100)
    canvas2.pack(anchor=tk.NW)

    frame2= tk.Frame(canvas2)
    frame2.pack()

    for i in range(20):
        tk.Label(frame2, text="Label "+str(i)).pack(side=tk.LEFT)

    canvas2.create_window(0, 0, window=frame2, anchor='nw')

    canvas2.update_idletasks()
    canvas2['scrollregion'] = (0,0,frame2.winfo_reqwidth(), frame2.winfo_reqheight())

    scrollbar.add_ScrollableArea(canvas1,canvas2)

    MouseWheel(root).add_scrolling(canvas1, xscrollbar=scrollbar)
    MouseWheel(root).add_scrolling(canvas2, xscrollbar=scrollbar)

    root.mainloop()

if __name__== '__main__':
    test()
