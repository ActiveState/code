#! /usr/bin/python

###########################################################
#
# List MySql databases in a Gtk.TreeView
#
###########################################################

from gi.repository import Gtk
import MySQLdb
import os

class MyWindow(Gtk.Window):
    
    def __init__(self):

        Gtk.Window.__init__(self, title='My Window Title')
        self.connect('delete-event', Gtk.main_quit)        
        
        store = Gtk.ListStore(str, str, str, str)
        self.populate_store(store)
        
        self.treeview = Gtk.TreeView(model=store)

        renderer = Gtk.CellRendererText()
        
        column_catalog = Gtk.TreeViewColumn('Catalog Name', renderer, text=0)
        column_catalog.set_sort_column_id(0)        
        self.treeview.append_column(column_catalog)
        
        column_dbname = Gtk.TreeViewColumn('Database Name', renderer, text=1)
        column_dbname.set_sort_column_id(1)
        self.treeview.append_column(column_dbname)
        
        column_charset = Gtk.TreeViewColumn('Character Set', renderer, text=2)
        column_charset.set_sort_column_id(2)
        self.treeview.append_column(column_charset)
        
        column_collation = Gtk.TreeViewColumn('Collation', renderer, text=3)
        column_collation.set_sort_column_id(3)
        self.treeview.append_column(column_collation)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)
        scrolled_window.set_min_content_height(200)

        self.add(scrolled_window)
        self.show_all()

    # Add data to ListStore
    def populate_store(self, store):
        
        try:
            connection = None
            connection = MySQLdb.connect('localhost', 'annon', 'pass')
            cursor = connection.cursor()
            cursor.execute("Select * From `INFORMATION_SCHEMA`.`SCHEMATA`")
            rows = cursor.fetchall()
        
            for row in rows:
                store.append([row[0], row[1], row[2], row[3]])
                
        except MySQLdb.Error, e:
            store.append([str(e.args[0]), e.args[1], '', ''])
            
        finally:
            if connection != None:
                connection.close()
        
            
win = MyWindow()
Gtk.main()
