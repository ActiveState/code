# Author: Miguel Martinez Lopez

try:
    from Tkinter import Label
    from ttk import Style
    from tkFont import Font, nametofont
except ImportError:
    from tkinter import Label
    from tkinter.ttk import Style
    from tkinter.font import Font, nametofont

def get_background_of_widget(widget):
    try:
        # We assume first tk widget
        background = widget.cget("background")
    except:
        # Otherwise this is a ttk widget
        style = widget.cget("style")

        if style == "":
            # if there is not style configuration option, default style is the same than widget class
            style = widget.winfo_class()

        background = Style().lookup(style, 'background')
    
    return background

class Link_Button(Label, object):
    def __init__(self, master, text, background=None, font=None, familiy=None, size=None, underline=True, visited_fg = "#551A8B", normal_fg = "#0000EE", visited=False, action=None):
        self._visited_fg = visited_fg
        self._normal_fg = normal_fg
        
        if visited:
            fg = self._visited_fg
        else:
            fg = self._normal_fg

        if font is None:
            default_font = nametofont("TkDefaultFont")
            family = default_font.cget("family")

            if size is None:
                size = default_font.cget("size")

            font = Font(family=family, size=size, underline=underline)

        Label.__init__(self, master, text=text, fg=fg, cursor="hand2", font=font)

        if background is None:
            background = get_background_of_widget(master)

        self.configure(background=background)

        self._visited = visited
        self._action = action

        self.bind("<Button-1>", self._on_click)

    @property
    def visited(self):
        return self._visited
        
    @visited.setter
    def visited(self, is_visited):
        if is_visited:
            self.configure(fg=self._visited_fg)
            self._visited = True
        else:
            self.configure(fg=self._normal_fg)
            self._visited = False

    def _on_click(self, event):
        if not self._visited:
            self.configure(fg=self._visited_fg)

        self._visited = True

        if self._action:
            self._action()


if __name__ == "__main__":
    import webbrowser

    try:
        from Tkinter import Tk, Frame
    except ImportError:
        from tkinter import Tk, Frame    

    def callback():
        webbrowser.open_new(r"http://www.google.com")

    root = Tk()
    frame = Frame(root, bg="white")
    frame.pack(expand=True, fill="both")

    link = Link_Button(frame, text="Google Hyperlink", action=callback)
    link.pack(padx=10, pady=10)
    root.mainloop()
