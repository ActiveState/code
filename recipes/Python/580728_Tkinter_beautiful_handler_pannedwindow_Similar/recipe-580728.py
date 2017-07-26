# Author: Miguel Martinez Lopez
#
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))


try:
    from Tkinter import Frame, PanedWindow as Tk_PanedWindow
    from ttk import Label
    from Tkconstants import HORIZONTAL, VERTICAL
except ImportError:
    from tkinter import Frame, PanedWindow as Tk_PanedWindow
    from tkinter.ttk import Label
    from tkinter.constants import HORIZONTAL, VERTICAL

class Handle(Frame):
    def __init__(self, panedwindow, sash_index, disallow_dragging=False, on_click=None, **kw):
        image = kw.pop("image", None)
        Frame.__init__(self, panedwindow, class_="Handle", **kw)

        self._sash_index = sash_index
        
        if image:
            self._event_area = Label(self, image=image)
            self._event_area.pack()            
        else:
            self._event_area = self
        
        self._center = int(self._event_area.winfo_reqwidth()/2), int(self._event_area.winfo_reqheight()/2)

        if disallow_dragging:
            if on_click:
                self._event_area.bind('<Button-1>', lambda event: on_click())
        else:
            self._event_area.bind('<Button-1>', self._initiate_motion)
            self._event_area.bind('<B1-Motion>', self._on_dragging)
            self._event_area.bind('<ButtonRelease-1>', self.master._on_release)
        
        
    def _initiate_motion(self, event) :
        self.master._active_sash = self._sash_index

        self._dx = event.x
        self._dy = event.y

    @property
    def sash_index(self):
        return self._sash_index

    def _on_dragging(self):
        raise NotImplementedError

class Vertical_Handle(Handle):
    def _on_dragging(self, event):
        y = event.y_root - self.master.winfo_rooty() - self._dy
        
        self.master.sash_place(self._sash_index, 1, y)

        self.master._update_position_all_handles()

class Horizontal_Handle(Handle):
    def _on_dragging(self, event):
        x = event.x_root - self.master.winfo_rootx() - self._dx

        self.master.sash_place(self._sash_index, x, 1)

        self.master._update_position_all_handles()
        

class PanedWindow(Tk_PanedWindow):
    
    def __init__(self, master, color="gray", size=60, sashpad=2, disallow_dragging=False, on_click=None, image=None, cursor=None, opaqueresize=True):
        Tk_PanedWindow.__init__(self, master, showhandle = False, orient=self.ORIENT, sashpad=sashpad, opaqueresize=opaqueresize)
    
        self._active_sash = None
        self._on_click = on_click
        self._image = image
        self._color = color
        self._cursor = cursor

        self._configure_callbacks = []
        
        if not opaqueresize:
            disallow_dragging = True

        self._disallow_dragging = disallow_dragging

        self._handle_list = []
        self._list_of_panes = []
        
        if self.ORIENT == VERTICAL:           
            self._width= size
            self._height = 2*sashpad
        else:            
            self._width = 2*sashpad
            self._height= size
        
        if opaqueresize:
            self.bind('<Button-1>', self._on_mark_sash)
            self.bind('<B1-Motion>', self._on_drag_sash)
            self.bind('<ButtonRelease-1>', self._on_release)
        
    def _on_release(self, event):
        handle_index = self._active_sash

        callback_id1 = self._list_of_panes[handle_index+1].bind("<Configure>", lambda event, handle_index=handle_index: self._on_configure_pane(handle_index), "+")
        callback_id2 = self._list_of_panes[handle_index].bind("<Configure>", lambda event, handle_index=handle_index: self._on_configure_pane(handle_index), "+")

        self._configure_callbacks[handle_index] = (callback_id1,callback_id2)

        self._active_sash = None

    def _on_drag_sash(self, event):
        coord_x = event.x
        coord_y = event.y

        Tk_PanedWindow.sash_place(self, self._active_sash, coord_x, coord_y)
        self._update_position_all_handles()

        return "break"

    def add(self, pane, **kwargs):
        Tk_PanedWindow.add(self, pane, **kwargs)

        self._list_of_panes.append(pane)
        quantity_of_panes = len(self._list_of_panes)

        if quantity_of_panes >= 2:
            handle_index = quantity_of_panes-2
            handle = self.HANDLE_CLASS(self, handle_index, bg=self._color, height=self._height, width=self._width, cursor = self._cursor, disallow_dragging=self._disallow_dragging, on_click=self._on_click, image=self._image)

            if self.ORIENT == VERTICAL:
                handle.place(relx=0.5, anchor="c")
            else:
                handle.place(rely=0.5, anchor="c")

            self._handle_list.append(handle)

            callback_id1 = pane.bind("<Configure>", lambda event, handle_index=handle_index: self._on_configure_pane(handle_index), "+")
            callback_id2 = self._list_of_panes[handle_index].bind("<Configure>", lambda event, handle_index=handle_index: self._on_configure_pane(handle_index), "+")
            self._configure_callbacks.append((callback_id1,callback_id2))

    def _on_mark_sash(self, event):
        identity = self.identify(event.x, event.y)

        if len(identity) ==2:
            self._active_sash= handle_index = identity[0]
            callback_id1,callback_id2 = self._configure_callbacks[handle_index]
            
            self._list_of_panes[handle_index+1].unbind(callback_id1)
            self._list_of_panes[handle_index].unbind(callback_id2)
        else:
            self._active_sash = None

class Vertical_PanedWindow(PanedWindow):
    ORIENT = VERTICAL
    HANDLE_CLASS = Vertical_Handle
        
    def _on_configure_pane(self, sash_index):
        x,y = Tk_PanedWindow.sash_coord(self, sash_index)
        self._handle_list[sash_index].place(y=y)
            
    def _update_position_all_handles(self):
        for sash_index, handle in enumerate(self._handle_list):
            x,y = Tk_PanedWindow.sash_coord(self, sash_index)
            handle.place(y=y)

class Horizontal_PanedWindow(PanedWindow):
    ORIENT = HORIZONTAL
    HANDLE_CLASS = Horizontal_Handle

    def _update_position_all_handles(self):
        for sash_index, handle in enumerate(self._handle_list):
            x,y = Tk_PanedWindow.sash_coord(self, sash_index)
            handle.place(x=x)

    def _on_configure_pane(self, sash_index):
        x,y = Tk_PanedWindow.sash_coord(self, sash_index)
        self._handle_list[sash_index].place(x=x)
        
if __name__ == "__main__":
    try:
        from Tkinter import Tk, PhotoImage
    except ImportError:
        from tkinter import Tk

    root = Tk()
    
    # Use for example this image for horizontal panedwindow
    # image = PhotoImage(data="R0lGODlhAwAYAPIAAEBAQGBgYICAgLu7u8zMzAAAAAAAAAAAACH5BAEAAAUALAAAAAADABgAAAMXCCFRI4OUSRVzUNJp24sbt3hZWHQYOCUAOw==")

    image = PhotoImage(data="R0lGODlhGAADAPIFAEBAQGBgYICAgLu7u8zMzAAAAAAAAAAAACH5BAEAAAUALAAAAAAYAAMAAAMaWBJQym61N2UZJTisb96fpxGD4JBmgZ4lKyQAOw==")

    panedwindow = Vertical_PanedWindow(root,  sashpad = 3, image=image)
    panedwindow.pack(fill="both", expand=True)
    
    
    for color in ("red", "blue","green"):
        frame = Frame(panedwindow, width=200, height=200, bg=color)
        panedwindow.add(frame, stretch="always")
    
    root.mainloop()
