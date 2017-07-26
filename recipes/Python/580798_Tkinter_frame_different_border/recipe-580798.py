# Author: Miguel Martinez Lopez

try:
    from Tkinter import Tk, Frame
except ImportError:
    from tkinter import Tk, Frame

class Bordered_Frame(Frame):
    def __init__(self, master, bordercolor=None, borderleft=0, bordertop=0, borderright=0, borderbottom=0, interiorwidget=Frame, **kwargs):
        Frame.__init__(self, master, background=bordercolor, bd=0, highlightthickness=0)

        self.interior = interiorwidget(self, **kwargs)
        self.interior.pack(padx=(borderleft, borderright), pady=(bordertop, borderbottom))
        
        
if __name__ == "__main__":
    try:
        from Tkinter import Tk, Label
    except ImportError:
        from tkinter import Tk, Label
    
    root = Tk()
    root.geometry("300x400")
    root.configure(background="white")

    f = Bordered_Frame(root, text="This is a text", background="white", bordercolor="blue", padx=3, borderleft=7, interiorwidget=Label)
    f.pack(pady=10)
    
    f = Bordered_Frame(root, background="white", bordercolor="green", borderleft=7, bordertop=2, borderright=2, borderbottom=2)
    f.pack(pady=10)

    Label(f.interior, text="This is another example", background="white").pack(padx=4, pady=2)

    root.mainloop()
