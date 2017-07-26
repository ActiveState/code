# Author: Miguel Martinez Lopez
#
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))

try:
    from Tkinter import Text, Frame, Label, PhotoImage, Button
    from ttk import Scrollbar

    from Tkconstants import *
except ImportError:
    from tkinter import Text, Frame, Label, PhotoImage, Button
    from tkinter.ttk import Scrollbar

    from tkinter.constants import *


class Tag(Frame):
    BACKGROUND = "#dddddd"
    PADDING = (5,7,5,7)
    LABEL_AND_BUTTON_SPACING = 2
    
    FOREGROUND_LABEL = "#0073ea"
    def __init__(self, master, text):
        self._text = text
        
        Frame.__init__(self, master, background=self.BACKGROUND, highlightbackground="red", borderwidth=1, relief=SOLID)
        
        Label(self, text=text, background=self.BACKGROUND, foreground=self.FOREGROUND_LABEL).pack(side=LEFT, pady=(self.PADDING[1], self.PADDING[3]), padx=(self.PADDING[0],0))
        
        self._close_IMG = PhotoImage(data="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFySURBVDiNpZM9juJAEIU/WxPY/EstQdICEYAQ+A5eX2CjDTgiMRfwzh4BmcAkTgAJiZZFsF7TbvAmeMUKZoKhouqnrqp+9V5bZVnyStgvVQNv94cgCN6EEAsApdQ8DEPzGQ5gVRRul5ae5wW2bbNarUKl1HeAZ3jV5N8LhBCL6XQaSCmdy+WC53lBFEVLgNlsFkgpHYDr9RpEUbQAfjxQMMagtSaOY8bjsTOZTHyAXq/nrNdrRqMRWuvnO1BKzTebzdIYEwwGAyeOY4bDYQ3glpMkSZ4kSaiUmj/s4H4P/X7f73a7td1uh2VZSCnZ7/fZdrt9v+f/QKEKrXWptaZqnuc5xpinhnlQQQjxTQjhnk4n2u02AFWulPqjlPr5oQqtVstvNBpumqa4rsvhcPhdliWdTqeepin1et0tisIHPlYhz3Ns2+Z4PGZZlv264X6z2aydz2eMMfcl/6sALG8TKIrivTLSE/xTFb5m5a/Gy7/xL3CL+6G7+HoOAAAAAElFTkSuQmCC")
        Button(self, highlightthickness=0, borderwidth=0, background=self.BACKGROUND, activebackground=self.BACKGROUND, image=self._close_IMG, command=self.destroy).pack(side=LEFT, pady=(self.PADDING[1], self.PADDING[3]), padx=(self.LABEL_AND_BUTTON_SPACING,self.PADDING[2]))
        
    @property
    def text(self):
        return self._text
        

class Tag_Entry(Frame):
    TAG_ENTRY_PADX = 7
    TAG_ENTRY_PADY = 5
    SPACING_BETWEEN_TAGS = 3

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)
        
        textarea_frame = Frame(self, bd=1, relief=SOLID,**kwargs)
        textarea_frame.pack(fill=X)
        textarea_frame.pack_propagate(False)
        
        self.textarea = Text(textarea_frame, height=1, pady=self.TAG_ENTRY_PADY, padx=self.TAG_ENTRY_PADX, highlightthickness =0, spacing1=0, spacing2=0, spacing3=0, borderwidth=0, wrap="none")
        self.textarea.pack(expand=True, fill=BOTH, padx=2)

        scrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.textarea.xview)
        scrollbar.pack(fill=X)

        self.textarea.configure(xscrollcommand=scrollbar.set)
        self.textarea.bind("<KeyPress>",self._on_keypress)

        tag = Tag(self.textarea, "")
        self.textarea.window_create("1.0", window=tag)
        self.update_idletasks()

        tag_reqheight = tag.winfo_reqheight()
        textarea_frame.configure(height=tag_reqheight + 2*self.TAG_ENTRY_PADY+2*self.textarea["borderwidth"])

        # I add a hidden frame because I want the cursor centered including when there is no tag
        self.textarea.window_create("1.0", window=Frame(self.textarea, height=tag_reqheight, width=0, borderwidth=0))
        tag.destroy()

    def add_tag(self, text):
        tag = Tag(self.textarea, text)

        self.textarea.window_create("1.%s"% len(self.textarea.window_names()), window=tag, padx=self.SPACING_BETWEEN_TAGS)
    
    def _index_of_first_char(self):
        return self.textarea.index("end-%sc"%len(self.textarea.get("1.0", END)))

    def _on_keypress(self, event):
        if event.keysym == 'BackSpace':
            if self.textarea.index(INSERT) == self._index_of_first_char():
                children = self.textarea.winfo_children()

                child = children[-1]
                if isinstance(child, Tag):
                    child.destroy()
            else:
                self.textarea.delete("%s-1c" % INSERT)
            
        elif event.keysym == 'Delete':
            self.textarea.delete("%s" % INSERT)
        
        elif event.keysym == 'Left':
            if self.textarea.index(INSERT) != self._index_of_first_char():
                self.textarea.mark_set(INSERT, "%s-1c"%insertion_index)

        elif event.keysym == 'Right':
            insertion_index = self.textarea.index(INSERT)
            self.textarea.mark_set(INSERT, "%s+1c"%insertion_index)

        elif event.keysym == 'Home':
            self.textarea.mark_set(INSERT, self._index_of_first_char())

        elif event.keysym == 'End':
            self.textarea.mark_set(INSERT, END)
        # We check whether it is a punctuation or normal key
        elif len(event.char) == 1:
            if event.keysym == 'Return':
                # In this situation ord(event.char)=13, which is the CARRIAGE RETURN character
                # We want instead the new line character with ASCII code 10
                text = self.textarea.get("1.0", END)
                self.textarea.delete("end-%sc"%len(text), END)

                text = text.strip()
                
                if text:           
                    self.add_tag(text)
                    self.update_idletasks()
                    self.textarea.see(END)
            else:
                self.textarea.insert(INSERT, event.char)
                self.textarea.see(END)
        return "break"

    @property
    def list_of_tags(self):
        list_of_tags = []
        for window_name in self.textarea.window_names():
            widget = self.nametowidget(window_name)
            
            if isinstance(widget, Tag):
                list_of_tags.append(widget.text)
            
        return list_of_tags
    
if __name__ == "__main__":
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root = Tk()
    root.geometry("300x300")
    tag_entry = Tag_Entry(root)
    tag_entry.pack(fill=X)


    tag_entry.add_tag("hello")
    # print all the tags
    print(tag_entry.list_of_tags)

    root.mainloop()
