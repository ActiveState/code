from tkinter.ttk import Notebook

class Autoresized_Notebook(Notebook):
  def __init__(self, master=None, **kw):

    Notebook.__init__(self, master, **kw)
    self.bind("<<NotebookTabChanged>>", self._on_tab_changed)

  def _on_tab_changed(self,event):
    event.widget.update_idletasks()

    tab = event.widget.nametowidget(event.widget.select())
    event.widget.configure(height=tab.winfo_reqheight())

if __name__== "__main__":
    from tkinter import Frame, Tk
    root = Tk()      

    notebook = Autoresized_Notebook(root)    
    notebook.add(Frame(notebook, width=400, height=200, name="a"),text="TAB 1")
    notebook.add(Frame(notebook, width=400, height=300, name="b"),text="TAB 2")
    notebook.add(Frame(notebook, width=400, height=100, name="c"),text="TAB 3")

    notebook.pack()

    root.mainloop()
