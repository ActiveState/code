import gtk
from time import sleep

class splashScreen():     
    def __init__(self):
        #DONT connect 'destroy' event here!
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Your app name')
        self.window.set_position(gtk.WIN_POS_CENTER)
        main_vbox = gtk.VBox(False, 1) 
        self.window.add(main_vbox)
        hbox = gtk.HBox(False, 0)
        self.lbl = gtk.Label("This shouldn't take too long... :)")
        self.lbl.set_alignment(0, 0.5)
        main_vbox.pack_start(self.lbl, True, True)
        self.window.show_all()

        
class yourApp():
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Your app name')
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect('destroy',	gtk.main_quit)
        main_vbox = gtk.VBox(False, 1) 
        self.window.add(main_vbox)
        hbox = gtk.HBox(False, 0)
        self.lbl = gtk.Label('All done! :)')
        self.lbl.set_alignment(0, 0.5)
        main_vbox.pack_start(self.lbl, True, True)
        self.window.show_all()      
        
        
if __name__ == "__main__":
    splScr = splashScreen()
    #If you don't do this, the splash screen will show, but wont render it's contents
    while gtk.events_pending():
        gtk.main_iteration()
    #Here you can do all that nasty things that take some time.
    sleep(3) 
    app = yourApp()
    #We don't need splScr anymore.
    splScr.window.destroy() 
    gtk.main()
