# Version 1.1
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print("Email: ", "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))

from __future__ import print_function

try:
    from tkinter import *
except ImportError:
    from Tkinter import *
    

class SimultaneousPanels(object):
    TAG_PREFIX = 'SimultaneousPanels_'
    
    def __init__(self):
        self.collectionOfPanedWindows = {}

    def new_panedwindow(self,master, custom_tag= 'default', **kargs):
        widget = PanedWindow(master, **kargs)
        self.add_widget(widget,custom_tag)

        return widget

    def add_widget(self, widget, custom_tag):
        ID_of_the_panel_group = self.TAG_PREFIX + custom_tag
        
        widget.other_paned_windows = []

        if ID_of_the_panel_group in self.collectionOfPanedWindows:
            for paned_window in self.collectionOfPanedWindows[ID_of_the_panel_group]:
                widget.other_paned_windows.append(paned_window)
                paned_window.other_paned_windows.append(widget)

            self.collectionOfPanedWindows[ID_of_the_panel_group].append(widget)
        else:
            self.collectionOfPanedWindows[ID_of_the_panel_group] = [widget]

        widget.ID_of_the_panel_group = ID_of_the_panel_group
        
        widget.bindtags( (ID_of_the_panel_group,)+ widget.bindtags() )
        widget.bind_class(ID_of_the_panel_group, '<Button-1>', self.sash_mark)
        widget.bind_class(ID_of_the_panel_group, '<B1-Motion>', self.sash_dragto)

    def sash_mark(self,event):
        this_widget = event.widget

        identity = this_widget.identify(event.x, event.y)

        if len(identity) ==2:
            index = identity[0]
            this_widget.activedSash=index
        else:
            this_widget.activedSash = None

    def sash_dragto(self,event):
        this_widget = event.widget
        activedSash = this_widget.activedSash
        
        coord_x = event.x
        coord_y = event.y
        
        if activedSash != None:
            for paned_window in this_widget.other_paned_windows:
                paned_window.sash_place(activedSash, coord_x, coord_y)

            this_widget.sash_place(activedSash, coord_x, coord_y)

            return "break"
            
    def clear_connection(self):
        for list_of_panels in self.collectionOfPanedWindows.values():
            for panel in list_of_panels:
                del panel.other_paned_windows
                self.delete_bindtag_of_panel(panel)
        self.collectionOfPanedWindows = {}

    def delete_group(self, custom_tag):
        ID_of_the_panel_group = self.TAG_PREFIX + custom_tag
        for widget in self.collectionOfPanedWindows[ID_of_the_panel_group]:
            del widget.other_paned_windows
            self.delete_bindtag_of_panel(widget)

        del self.collectionOfPanedWindows[ID_of_the_panel_group]

    def remove_panel_from_group(self, widget):
        for panel in self.collectionOfPanedWindows[widget.ID_of_the_panel_group]:
            panel.other_paned_windows.remove(widget)
        self.delete_bindtag_of_panel(widget)
        del widget.other_paned_windows

    def delete_bindtag_of_panel(self, widget):
        new_bindtags = list(widget.bindtags())
        new_bindtags.remove(widget.ID_of_the_panel_group)
        widget.bindtags(tuple(new_bindtags))

    # Functions for debugging
    
    def __debug_all_panes(self, panedwindow):
        list_of_widgets = [panedwindow]
        list_of_widgets.extend(panedwindow.other_paned_windows)
        
        for panedwindow in list_of_widgets:
            self.__debug_panes_in_panedwindow(panedwindow)
        
        print()

    def __debug_panes_in_panedwindow(self, panedwindow):
        for tcl_object in panedwindow.panes():
            pane = panedwindow.nametowidget( str( tcl_object ) )
            if panedwindow["orient"] == HORIZONTAL:
                print( pane.winfo_width(), end=" ")
            else:
                print( pane.winfo_height(), end=" ")
        print()
            

def test():

    root = Tk()
    connectedPanels = SimultaneousPanels()
    
    Button(root, text="Click here to destroy connection between panels", command = connectedPanels.clear_connection).pack()
    
    for i in range(3):
        emptySpace = Frame(root, height=10)
        emptySpace.pack()
        
        m = connectedPanels.new_panedwindow(root, bd=1, orient=VERTICAL,sashwidth=2,sashrelief=RIDGE)
        m.pack()

        for j in range(3):
            panel= Label(m, text="panel number %s" %j)
            m.add(panel)

    root.mainloop()

if __name__ == '__main__':
    test()
