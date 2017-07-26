"""
    Button Widget to be used with Tkinter, that allows
    you to make a button that changes fg color when
    the mouse is over it.
"""
import Tkinter

class ColorButton(Tkinter.Widget):
    """
    Slightly different Button widget, with an option added: OnColor:
    This will change the fg of the Button to that color when the mouse
    is over it. Default OnColor is 'red'"""
    
    def __init__(self, master, OnColor = 'red', cnf = {}, **kw):
        Tkinter.Widget.__init__(self, master, 'button', cnf, kw)
        if not 'fg' in kw:
            kw['fg'] = 'black'
        self.bind("<Enter>", lambda Event:self.Enter(OnColor))
        self.bind("<Leave>", lambda Event:self.Leave(kw['fg']))

    def Enter(self, Color):
        """Internal Function"""
        
        self['fg'] = Color

    def Leave(self, Color):
        """Internal Function"""
        
        self['fg'] = Color
