#! /usr/bin/python

###########################################################
#
# Use Gtk.TreeView to browse MySql databases
#
###########################################################

from gi.repository import Gtk
import MySQLdb
import os

class MyWindow(Gtk.Window):
    
    def __init__(self):

        Gtk.Window.__init__(self, title='My Window Title')
        self.connect('delete-event', Gtk.main_quit)        
        
        self.connection = None
        self.connect_to_database()
        store = Gtk.TreeStore(str, str, str, str)
        self.populate_store(store)
        
        self.treeview = Gtk.TreeView(model=store)

        renderer = Gtk.CellRendererText()
        column_catalog = Gtk.TreeViewColumn('Name', renderer, text=0)
        self.treeview.append_column(column_catalog)
        
        self.treeview.connect('test-expand-row', self.add_child_items, store)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.treeview)
        scrolled_window.set_min_content_height(200)

        self.add(scrolled_window)
        self.show_all()
    
    def connect_to_database(self):
        try:
            self.connection = MySQLdb.connect('localhost', 'anon', 'pass')
        except MySQLdb.Error, e:
            print e.args[1]
    
    # Add databases to TreeStore
    def populate_store(self, store):
        
        root_iter = store.append(None, ['localhost', 'server', '', ''])
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("Select * From `INFORMATION_SCHEMA`.`SCHEMATA`")
            rows = cursor.fetchall()
        
            for row in rows:
                db_iter = store.append(root_iter, [row[1], 'database', '', ''])
                store.append(db_iter, ['dummy', '', '', ''])
        except MySQLdb.Error, e:
            store.append(root_iter, [e.args[1], '', '', ''])    
    
    def add_child_items(self, treeview, iter, path, store):
        
        if iter == None:
            return
        
        if store.iter_n_children(iter) == 1:
            
            node_iter = store.iter_nth_child(iter, 0)

            if store.get(node_iter, 0)[0] == 'dummy':
                store.remove(node_iter)

                if store.get(iter, 1)[0] == 'database':
                
                    cursor = self.connection.cursor()
                    db_name = store.get(iter, 0)[0]
                    
                    tables_iter = store.append(iter, ['tables', '', '', ''])
                    
                    sql = "Select `TABLE_NAME` From `INFORMATION_SCHEMA`.`TABLES`" \
                    "Where `TABLE_SCHEMA` = '{0}' " \
                    "And `TABLE_TYPE` = 'BASE TABLE'".format(db_name)
                    print sql
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        table_iter = store.append(tables_iter, [row[0], 'table', db_name, ''])
                        store.append(table_iter, ['dummy', '', '', ''])
                        
                    views_iter = store.append(iter, ['views', '', '', ''])
                    
                    sql = "Select `TABLE_NAME` From `INFORMATION_SCHEMA`.`TABLES`" \
                    "Where `TABLE_SCHEMA` = '{0}'" \
                    "And `TABLE_TYPE` Like '%VIEW%'".format(db_name)
                    print sql
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        view_iter = store.append(views_iter, [row[0], 'table', db_name, ''])
                        store.append(view_iter, ['dummy', '', '', ''])
                        
                if store.get(iter, 1)[0] == 'table':
                    
                    columns_iter = store.append(iter, ['columns', '', '', ''])
                    
                    db_name = store.get(iter, 2)[0]
                    table_name = store.get(iter, 0)[0]
                    
                    sql = "Select `COLUMN_NAME` From `INFORMATION_SCHEMA`.`COLUMNS` " \
                    "Where `TABLE_SCHEMA` = '{0}' " \
                    "And `TABLE_NAME` = '{1}'" \
                    "Order By `ORDINAL_POSITION`".format(db_name, table_name)
                    
                    cursor = self.connection.cursor()
                    cursor.execute(sql)
                       
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        store.append(columns_iter, [row[0], 'column', '', ''])
                    
            
            
win = MyWindow()
Gtk.main()
