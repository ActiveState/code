# Author: Miguel Martinez Lopez

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'with_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")
    
    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.with_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.with_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)
        
            state.with_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)
            
            state.with_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")
    
    entry.placeholder_state = state

    return state

if __name__ == "__main__":
    root = tk.Tk()

    login_frame = tk.LabelFrame(root, text="Login", padx=5, pady=5)
    login_frame.pack(padx=10, pady=10)
    
    label = tk.Label(login_frame, text="User: ")
    label.grid(row=0, column=0, sticky=tk.E)

    # I add a border of 1px width and color #bebebe to the entry using these parameters:
    #  - highlightthickness=1
    #  - highlightbackground="#bebebe"
    #
    entry = tk.Entry(login_frame, bd=1, bg="white", highlightbackground="#bebebe", highlightthickness=1)
    
    # I make the entry a little bit more height using ipady option
    entry.grid(row=0, column=1, ipady=1)

    add_placeholder_to(entry, 'Enter your username...')

    label = tk.Label(login_frame, text="Password: ")
    label.grid(row=1, column=0, sticky=tk.E)

    entry = tk.Entry(login_frame, bd=1, bg="white", highlightbackground="#bebebe", highlightthickness=1)
    entry.grid(row=1, column=1, ipady=1)

    add_placeholder_to(entry, 'Password...')
    
    # Every row has a minimum size
    login_frame.grid_rowconfigure(0, minsize=28)
    login_frame.grid_rowconfigure(1, minsize=28)
    
    root.mainloop()
