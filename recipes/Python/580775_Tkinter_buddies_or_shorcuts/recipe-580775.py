def shortcut_for_underlining_text(widget, callback, ignore_case=True):
    text = widget.cget("text")
    
    if text == "":
        raise Exception("No text for widget")

    underline = widget.cget("underline")

    if underline == -1:
        raise Exception("No underline found on widget text")

    toplevel = widget.winfo_toplevel()
    char = text[underline]
    
    if ignore_case:
        hotkey = "<Alt-%s>"%char.lower()
        toplevel.bind(hotkey, callback)
            
        hotkey = "<Alt-%s>"%char.upper()
        toplevel.bind(hotkey, callback)
    else:
        hotkey = "<Alt-%s>"%char
        toplevel.bind(hotkey, callback)    

def create_buddy(label, partner, ignore_case=True):
    shortcut_for_underlining_text(label, lambda event: partner.focus(), ignore_case=ignore_case)

def create_shortcut_to_button(button, ignore_case=True):
    shortcut_for_underlining_text(button, lambda event: button.invoke(), ignore_case=ignore_case)

if __name__ == "__main__":
    try:
        from Tkinter import Tk, Label, Entry, Toplevel, Button
        from tkMessageBox import showinfo
    except ImportError:
        from tkinter import Tk, Label, Entry, Toplevel, Button
        from tkinter.messagebox import showinfo

    root = Tk()
    root.wm_title("Login")

    l= Label(root, text="User Name:", underline=5)
    l.grid(row=0, column=0)
    e = Entry(root)
    e.grid(row=0, column=1)

    create_buddy(l,e)

    l= Label(root, text="Password:", underline=0)
    l.grid(row=1, column=0)
    e = Entry(root)
    e.grid(row=1, column=1)

    create_buddy(l,e)

    def login():
        showinfo("Login","Executed login callback")
    
    button = Button(root, text="Log in", command=login, underline=0)
    button.grid(row=2, column=0)
    
    create_shortcut_to_button(button)

    dialog = Toplevel(root)
    dialog.wm_title("Sign up")

    l= Label(dialog, text="Name:", underline=0)
    l.grid(row=0, column=0)
    e = Entry(dialog)
    e.grid(row=0, column=1)

    create_buddy(l,e)

    l= Label(dialog, text="Address:", underline=0)
    l.grid(row=1, column=0)
    e = Entry(dialog)
    e.grid(row=1, column=1)
    
    create_buddy(l,e)
    
    l= Label(dialog, text="Telephone:", underline=0)
    l.grid(row=2, column=0)
    e = Entry(dialog)
    e.grid(row=2, column=1)
    
    create_buddy(l,e)
    
    root.mainloop()
