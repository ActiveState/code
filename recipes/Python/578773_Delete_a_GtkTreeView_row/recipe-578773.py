#! /usr/bin/python

###########################################################
#
# Delete a Gtk.TreeView row
#
###########################################################

from gi.repository import Gtk
import os

class MyWindow(Gtk.Window):
    
    def __init__(self):

        Gtk.Window.__init__(self, title='My Window Title')
        self.connect('delete-event', Gtk.main_quit)        
        
        store = Gtk.ListStore(str, str)
        self.populate_store(store)
        
        self.treeview = Gtk.TreeView(model=store)

        renderer = Gtk.CellRendererText()
        
        column_name = Gtk.TreeViewColumn('Song Name', renderer, text=0)
        column_name.set_sort_column_id(0)        
        self.treeview.append_column(column_name)
        
        column_artist = Gtk.TreeViewColumn('Artist', renderer, text=1)
        column_artist.set_sort_column_id(1)
        self.treeview.append_column(column_artist)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)
        scrolled_window.set_min_content_height(200)
        
        button = Gtk.Button('Delete Selected Row')
        button.connect('clicked', self.on_button_clicked) 

        box = Gtk.Box()
        box.pack_start(scrolled_window, True, True, 1)
        box.pack_start(button, False, False, 1)

        self.add(box)
        self.show_all()

    def on_button_clicked(self, button):
     
  # Get the TreeView selected row(s)
        selection = self.treeview.get_selection()
        # get_selected_rows() returns a tuple
        # The first element is a ListStore
        # The second element is a list of tree paths
        # of all selected rows
        model, paths = selection.get_selected_rows()
        
        # Get the TreeIter instance for each path
        for path in paths:
   iter = model.get_iter(path)
   # Remove the ListStore row referenced by iter
   model.remove(iter)


    # Add data to ListStore
    def populate_store(self, store):
        
        store.append(['American Pie', 'Don McLean'])
        store.append(['Crossroads', 'Don McLean'])
        store.append(['Winterwood', 'Don McLean'])
        store.append(['Mountains of Mourne', 'Don McLean'])
        store.append(['Birthday song', 'Don McLean'])
        store.append(['Everyday', 'Don McLean'])
        store.append(['Crying', 'Don McLean'])
        store.append(['My Dear', 'Azra'])
        store.append(['Niska Bisera', 'Azra'])
        store.append(['Sticenik', 'Azra'])
        store.append(['Mon Ami', 'Azra'])
        store.append(['3N', 'Azra'])
        store.append(['Jane', 'Azra'])
        store.append(['Ghost of a Smile', 'The Pogues'])
        store.append(['Fairytale of New York', 'The Pogues'])
        store.append(['Fiesta', 'The Pogues'])
        store.append(['Summer in Siam', 'The Pogues'])
        
            
win = MyWindow()
Gtk.main()
