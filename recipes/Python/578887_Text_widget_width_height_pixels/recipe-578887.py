try:
    from Tkinter import Frame, Text, Tk
    from Tkconstants import YES, BOTH
except ImportError:
    from tkinter import Frame, Text, Tk
    from tkinter.constants import YES, BOTH

class Text2(Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, master, width=self.width, height=self.height)
        self.text_widget = Text(self, **kwargs)
        self.text_widget.pack(expand=YES, fill=BOTH)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)

root = Tk()

# Now width and height are in pixels. They are not now the number of columns and the number of lines respectively
Text2(root, width=90,height=120).pack()


root.mainloop()
