from tkinter import Tk, END, INSERT
from tkinter.ttk import Frame, Style
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import asksaveasfilename, askopenfilename

class Scratchpad:

    def __init__(self):
        self.window = Tk()
        self.window.title("Onager Scratchpad")
        self.create_frame()
        self.create_editing_window()
        self.window.bind('<F7>', self.save_file)
        self.window.bind('<F5>', self.open_file)

    def create_frame(self):
        frame_style = Style()
        frame_style.theme_use('alt')
        frame_style.configure("TFrame",
                              relief='raised')
        self.frame = Frame(self.window, style="frame_style.TFrame")
        self.frame.rowconfigure(1)
        self.frame.columnconfigure(1)
        self.frame.grid(row=0, column=0)

    def create_editing_window(self):
        self.editing_window = ScrolledText(self.frame)
        self.editing_window.configure(fg='gold',
                                      bg='blue',
                                      font='serif 12',
                                      padx='15',
                                      pady='15',
                                      wrap='word',
                                      borderwidth='10',
                                      relief='sunken',
                                      tabs='48',
                                      insertbackground='cyan')
        self.editing_window.grid(row=0, column=0)

    def save_file(self, event=None):
        name = asksaveasfilename()
        outfile = open(name, 'w')
        contents = self.editing_window.get(0.0, END)
        outfile.write(contents)
        outfile.close()

    def open_file(self, event=None):
        name = askopenfilename()
        infile = open(name, 'r')
        contents = infile.read()
        self.editing_window.insert(INSERT, contents)
        infile.close()

def main():
    onager = Scratchpad()
    onager.window.mainloop()

if __name__=='__main__':
    main()
