#!/usr/bin/python
import threading
import gtk
import random
import time

gtk.gdk.threads_init()

NUM_THREADS = 10

class PyApp(gtk.Window):
    def __init__(self, threads=None):
        super(PyApp, self).__init__()
        
        self.connect("destroy", self.quit)
        self.set_title("pyGTK Threads Example")
        
        vbox = gtk.VBox(False, 4)
        
        self.threads = []
        for i in range(NUM_THREADS + 1):
            pb = gtk.ProgressBar()
            vbox.pack_start(pb, False, False, 0)
            self.threads.append(ProgressThread(pb, random.uniform(0.01, 0.10)))
        
        self.add(vbox)
        self.show_all()
        
    def quit(self, obj):
        for t in self.threads:
            t.stop()
        
        gtk.main_quit()
        
class ProgressThread(threading.Thread):
    def __init__(self, progressbar, step_value):
        threading.Thread.__init__ (self)
        
        self.pb = progressbar
        self.step = step_value
        
        self.stopthread = threading.Event()

    def run(self):
        while not self.stopthread.isSet():
            cur_frac = self.pb.get_fraction()
            new_frac = cur_frac + self.step
            if new_frac > 1.0:
                new_frac = 1.0
            
            gtk.gdk.threads_enter()
            self.pb.set_fraction(new_frac)
            gtk.gdk.threads_leave()
            
            if self.pb.get_fraction() == 1.0:
                break
            
            time.sleep(0.1)
        
    def stop(self):
        self.stopthread.set()
        
if __name__ == "__main__":
    pyapp = PyApp()
    
    for t in pyapp.threads:
        t.start()
    
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
