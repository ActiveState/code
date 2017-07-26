from Tkinter import *
from ScrolledText import ScrolledText
from unicodedata import lookup
import os

class Diacritical:
    """Mix-in class that adds keyboard bindings for accented characters, plus
    other common functionality.
    
    An inheriting class must define a select_all method that will respond
    to Ctrl-A."""

    accents = (('acute', "'"), ('grave', '`'), ('circumflex', '^'),
               ('tilde', '='), ('diaeresis', '"'), ('cedilla', ','),
               ('stroke', '/'), ('ring above', ';'))

    def __init__(self):
        # Fix some key bindings
        self.bind("<Control-Key-a>", self.select_all)
        # We will need Ctrl-/ for the "stroke", but it cannot be unbound, so
        # let's prevent it from being passed to the standard handler
        self.bind("<Control-Key-/>", lambda event: "break")
        # Diacritical bindings
        for a, k in self.accents:
            # Little-known feature of Tk, it allows to bind an event to
            # multiple keystrokes
            self.bind("<Control-Key-%s><Key>" % k,
                      lambda event, a=a: self.insert_accented(event.char, a))

    def insert_accented(self, c, accent):
        if c.isalpha():
            if c.isupper():
                cap = 'capital'
            else:
                cap = 'small'
            try:
                c = lookup("latin %s letter %c with %s" % (cap, c, accent))
                self.insert(INSERT, c)
                # Prevent plain letter from being inserted too, tell Tk to
                # stop handling this event
                return "break"
            except KeyError, e:
                pass

class DiacriticalEntry(Entry, Diacritical):
    """Tkinter Entry widget with some extra key bindings for
    entering typical Unicode characters - with umlauts, accents, etc."""

    def __init__(self, master=None, **kwargs):
        Entry.__init__(self, master=None, **kwargs)
        Diacritical.__init__(self)

    def select_all(self, event=None):
        self.selection_range(0, END)
        return "break"

class DiacriticalText(ScrolledText, Diacritical):
    """Tkinter ScrolledText widget with some extra key bindings for
    entering typical Unicode characters - with umlauts, accents, etc."""

    def __init__(self, master=None, **kwargs):
        ScrolledText.__init__(self, master=None, **kwargs)
        Diacritical.__init__(self)

    def select_all(self, event=None):
        self.tag_add(SEL, "1.0", "end-1c")
        self.mark_set(INSERT, "1.0")
        self.see(INSERT)
        return "break"


def test():
    frame = Frame()
    frame.pack(fill=BOTH, expand=YES)
    if os.name == "nt":
        # Set default font for all widgets; use Windows typical default
        frame.option_add("*font", "Tahoma 8")
    # The editors
    entry = DiacriticalEntry(frame)
    entry.pack(fill=BOTH, expand=YES)
    text = DiacriticalText(frame, width=76, height=25, wrap=WORD)
    if os.name == "nt":
        # But this looks better than the default set above
        text.config(font="Arial 10")
    text.pack(fill=BOTH, expand=YES)
    text.focus()
    frame.master.title("Diacritical Editor")
    frame.mainloop()

if __name__ == "__main__":
    test()
