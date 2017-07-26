# Version: 1.2
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print "Author's email: ", "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex")

try:
    from Tkinter import Frame, Text
    from Tkconstants import *
    import tkFont
except ImportError:
    from tkinter import Frame, Text
    from tkinter.constants import *
    from tkinter import font as tkFont

class AutoResizedText(Frame):
    def __init__(self, master, width=0, height=0, family=None, size=None,*args, **kwargs):
        
        Frame.__init__(self, master, width = width, height= height)
        self.pack_propagate(False)

        self._min_width = width
        self._min_height = height

        self._textarea = Text(self, *args, **kwargs)
        self._textarea.pack(expand=True, fill='both')

        if family != None and size != None:
            self._font = tkFont.Font(family=family,size=size)
        else:
            self._font = tkFont.Font(family=self._textarea.cget("font"))

        self._textarea.config(font=self._font)

        # I want to insert a tag just in front of the class tag
        # It's not necesseary to guive to this tag extra priority including it at the beginning
        # For this reason I am making this search
        self._autoresize_text_tag = "autoresize_text_"+str(id(self))
        list_of_bind_tags = list(self._textarea.bindtags())
        list_of_bind_tags.insert(list_of_bind_tags.index('Text'), self._autoresize_text_tag)

        self._textarea.bindtags(tuple(list_of_bind_tags))
        self._textarea.bind_class(self._autoresize_text_tag, "<KeyPress>",self._on_keypress)

    def _on_keypress(self, event):
        self._textarea.focus_set()
        
        if event.keysym == 'BackSpace':
            self._textarea.delete("%s-1c" % INSERT)
            new_text = self._textarea.get("1.0", END)
        elif event.keysym == 'Delete':
            self._textarea.delete("%s" % INSERT)
            new_text = self._textarea.get("1.0", END)
        # We check whether it is a punctuation or normal key
        elif len(event.char) == 1:
            if event.keysym == 'Return':
                # In this situation ord(event.char)=13, which is the CARRIAGE RETURN character
                # We want instead the new line character with ASCII code 10
                new_char = '\n'
            else:
                new_char = event.char


            old_text = self._textarea.get("1.0", END)
            new_text = self._insert_character_into_message(old_text, self._textarea.index(INSERT), new_char)

        else:
            # If it is a special key, we continue the binding chain
            return
    
        # Tk Text widget always adds a newline at the end of a line
        # This last character is also important for the Text coordinate system
        new_text = new_text[:-1]

        self._fit_to_size_of_text(new_text)

        # Finally we insert the new character
        if event.keysym != 'BackSpace' and event.keysym != 'Delete':
            self._textarea.insert(INSERT, new_char)
        
        return "break"

    def _insert_character_into_message(self, message, coordinate, char):
        target_row, target_column = map( int, coordinate.split('.'))

        this_row = 1
        this_column = 0
        index = 0

        for ch in message:
            if this_row == target_row and this_column == target_column:
                message = message[:index] + char + message[index:]
                return message

            index += 1

            if ch == '\n':
                this_row += 1
                this_column = 0
            else:
                this_column += 1

    def _fit_to_size_of_text(self, text):
        number_of_lines = 0
        widget_width = 0

        for line in text.split("\n"):
            widget_width = max(widget_width,self._font.measure(line))
            number_of_lines += 1

        # We need to add this extra space to calculate the correct width
        widget_width += 2*self._textarea['bd'] + 2*self._textarea['padx'] + self._textarea['insertwidth']

        if widget_width < self._min_width:
            widget_width = self._min_width

        self._textarea.configure(height=number_of_lines)
        widget_height = max(self._textarea.winfo_reqheight(), self._min_height)

        self.config(width=widget_width, height=widget_height)

        # If we don't call update_idletasks, the window won't be resized before an insertion
        self.update_idletasks()

    @property
    def tag(self):
        return self._autoresize_text_tag

    def focus(self):
        self._textarea.focus()
        
    def bind(self, event, handler, add=None):
        self._textarea.bind(event, handler, add)

    def get(self, start, end=None):
        return self._textarea.get(start, end)

    def update(self, text):
        self._textarea.delete('1.0', 'end')        
        self._fit_to_size_of_text(text)
        self._textarea.insert('1.0', text)

if __name__ == '__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root = Tk()
    auto_text = AutoResizedText(root, family="Arial",size=15, width = 100, height = 50)
    auto_text.pack()
    auto_text.focus()
    root.mainloop()
