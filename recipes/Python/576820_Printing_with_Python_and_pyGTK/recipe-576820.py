#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# 
# written by Mark Muzenhardt <mark.muzenhardt@googlemail.com>
# published under BSD-License
 
import pygtk
pygtk.require('2.0')
import gtk
 
 
class DrawingAreaExample:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Drawing Area Example")
        window.connect("destroy", lambda w: gtk.main_quit())
        self.area = gtk.DrawingArea()
        self.area.set_size_request(400, 300)
        window.add(self.area)
 
        self.area.connect("expose-event", self.area_expose_cb)
        self.area.show()
        window.show()
        self.do_print()
 
    def area_expose_cb(self, area, event):
        self.style = self.area.get_style()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.draw_text()
        return True
 
    def do_print(self):
        print_op = gtk.PrintOperation()
        print_op.set_n_pages(1)
        print_op.connect("draw_page", self.print_text)
        res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, None)
 
    def draw_text(self):
        self.pangolayout = self.area.create_pango_layout("")
        self.format_text()
        self.area.window.draw_layout(self.gc, 10, 10, self.pangolayout)
        return
 
    def print_text(self, operation=None, context=None, page_nr=None):
        self.pangolayout = context.create_pango_layout()
        self.format_text()
        cairo_context = context.get_cairo_context()
        cairo_context.show_layout(self.pangolayout)
        return
 
    def format_text(self):
        self.pangolayout.set_text(unicode("""
Dies ist ein Text-Test. Er funktioniert gut und zeigt, dass auch PyGTK
das drucken kann, was man auf eine DrawingArea geschrieben hat.
Anwendungen dafür gibt es genug! 
""", "latin-1"))
 
 
def main():
    gtk.main()
    return 0
 
if __name__ == "__main__":
    DrawingAreaExample()
    main()
