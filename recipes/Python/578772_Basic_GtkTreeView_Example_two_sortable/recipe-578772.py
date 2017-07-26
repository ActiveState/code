#! /usr/bin/python

###########################################################
#
# Basic Gtk.TreeView Example with two sortable columns
#
###########################################################


# use  the new PyGObject binding
from gi.repository import Gtk
import os

class MyWindow(Gtk.Window):
    
    def __init__(self):

        Gtk.Window.__init__(self, title='My Window Title')
        self.connect('delete-event', Gtk.main_quit)        
        
        # Gtk.ListStore will hold data for the TreeView
        # Only the first two columns will be displayed
        # The third one is for sorting file sizes as numbers
        store = Gtk.ListStore(str, str, long)
        # Get the data - see below
        self.populate_store(store)
        
        treeview = Gtk.TreeView(model=store)

        # The first TreeView column displays the data from
        # the first ListStore column (text=0), which contains
        # file names
        renderer_1 = Gtk.CellRendererText()        
        column_1 = Gtk.TreeViewColumn('File Name', renderer_1, text=0)
        # Calling set_sort_column_id makes the treeViewColumn sortable
        # by clicking on its header. The column is sorted by
        # the ListStore column index passed to it 
        # (in this case 0 - the first ListStore column) 
        column_1.set_sort_column_id(0)        
        treeview.append_column(column_1)
        
        # xalign=1 right-aligns the file sizes in the second column
        renderer_2 = Gtk.CellRendererText(xalign=1)
        # text=1 pulls the data from the second ListStore column
        # which contains filesizes in bytes formatted as strings
        # with thousand separators
        column_2 = Gtk.TreeViewColumn('Size in bytes', renderer_2, text=1)
        # Mak the Treeview column sortable by the third ListStore column
        # which contains the actual file sizes
        column_2.set_sort_column_id(2)
        treeview.append_column(column_2)
        
        # Use ScrolledWindow to make the TreeView scrollable
        # Otherwise the TreeView would expand to show all items
        # Only allow vertical scrollbar
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(treeview)
        scrolled_window.set_min_content_height(200)
        
        self.add(scrolled_window)
        self.show_all()

    def populate_store(self, store):
        
        directory = '/home/anon/Documents'
        for filename in os.listdir(directory):
            size = os.path.getsize(os.path.join(directory, filename))
            # the second element is displayed in the second TreeView column
            # but that column is sorted by the third element
            # so the file sizes are sorted as numbers, not as strings
            store.append([filename, '{0:,}'.format(size), size])       
            
# The main part:
win = MyWindow()
Gtk.main()
