# Version: 1.0
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))

try:
    from Tkinter import Text, Frame, Label, Toplevel, PhotoImage
    from Tkconstants import *
    import tkFileDialog
    import tkMessageBox
    import ttk
    import tkFont
except ImportError:
    from tkinter import Text, Frame, Label, Toplevel, PhotoImage
    from tkinter.constants import *
    import tkinter.messagebox as tkMessageBox
    import tkinter.filedialog as tkFileDialog
    import tkinter.ttk as ttk
    import tkinter.font as tkFont

VERSION = 1.0
    
HELP_MESSAGE = '''
Tkinter Desktop Notes v%s

Editing Commands
    Ctrl-x : Cut selected text
    Ctrl-c : Copy selected text
    Ctrl-v : Paste cut/copied text
    Ctrl-Z : Undo
    Ctrl-Shift-z : Redo

File Commands
    Ctrl-o : Open file
    Ctrl-s : Save current note
    Ctrl-a : Save current note as <filename>
    Ctrl-n : Open new note

General
    Ctrl-h : Display this help window
'''%VERSION

class DraggableWindow(Toplevel):

    def __init__(self, master=None, disable_dragging =False, release_command = None):
        Toplevel.__init__(self, master)

        if disable_dragging == False:
            self.bind('<Button-1>', self.initiate_motion)
            self.bind('<ButtonRelease-1>', self.release_dragging)

        self.release_command = release_command


    def initiate_motion(self, event):
        # This is another possibility:
        #   OriX, OriY = self.window_position()
        #   self.deltaX = event.x_root - OriX
        #   self.deltaY = event.y_root - OriY
        #
        self.deltaX = event.x_root - self.winfo_x()
        self.deltaY = event.y_root - self.winfo_y()

        self.bind('<Motion>', self.drag_window)


    def drag_window(self, event):
        new_x = event.x_root - self.deltaX
        new_y = event.y_root - self.deltaY

        if new_x < 0 :
            new_x = 0

        if new_y < 0 :
            new_y = 0

        self.wm_geometry("+%s+%s" % (new_x, new_y))

    def release_dragging(self, event):
        self.unbind('<Motion>')

        if self.release_command != None :
            self.release_command()

    def disable_dragging(self) :
        self.unbind('<Button-1>')
        self.unbind('<ButtonRelease-1>')
        self.unbind('<Motion>')

    def enable_dragging(self):
        self.bind('<Button-1>', self.initiate_motion)
        self.bind('<ButtonRelease-1>', self.release_dragging)



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


class DesktopNote(DraggableWindow):
    BG_NOTE = '#ffff7d'
    FILETYPES = [('Text/ASCII', '*.txt'), ('All files', '*')]
            
    def __init__(self, master, title='Without title', min_width =110, min_height = 40):
        DraggableWindow.__init__(self, master)
        
        self.wm_attributes('-topmost', True)
        self.overrideredirect(True)

        self.filename = ''

        self.close_IMG = PhotoImage(data="R0lGODlhEAAQAPAAAAQEBAAAACH5BAEAAAEALAAAAAAQABAAAAImDI6ZFu3/DpxO0mlvBLFX7oEfJo5QZlZNaZTupp2shsY13So6VwAAOw==")
        self.minimize_IMG = PhotoImage(data="R0lGODlhEAAQAPAAAAQEBAAAACH5BAEAAAEALAAAAAAQABAAAAIiDI6ZFu3/DpxO0mlvBBrmbnBg83Wldl6ZgoljSsFYqNRcAQA7")
        self.restore_IMG = PhotoImage(data="R0lGODlhEAAQAPcAAAAAAAQEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAhFAP8FGEiwYEGB/xIqXLhwIMOHCh02NBgxAEODFhNKjNiwYsWDGQWGxIhQ48iJI09ynLhS48WUB1lCfLhxpkebHTHqtBgQADs=")
        self.minimizeAtRightSide_IMG = PhotoImage(data="R0lGODlhEAAQAPcAAAAAAAQEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAg+AP8FGEiwYEGB/xIqXLhwIMOHCh1CfChxosSKEC8GmJhQI0eBG0F+9MiRpMWQGCmiDPmxI8uWKUuCNEhzY0AAOw==")


        frameNote = Frame(self, bg=self.BG_NOTE, bd=1, highlightbackground='black',highlightcolor='black',highlightthickness=1)
        frameNote.pack()

        self.mimizedNote = Label(frameNote, text=title, bg=self.BG_NOTE, wraplength=1)
        self.mimizedNote.bind('<Button-1>', lambda event: self.maximize_from_right_side())

        self.maximizedNote = Frame(frameNote)
        self.maximizedNote.pack()

        Header = Frame(self.maximizedNote, bg=self.BG_NOTE)
        Header.pack(fill=X)

        ttk.Separator(self.maximizedNote, orient=HORIZONTAL).pack(expand=True, fill=X)

        titleLabel = Label(Header, text = title, bg=self.BG_NOTE)
        titleLabel.pack(side=LEFT)

        Button(Header, compound=TOP, image=self.close_IMG, bg=self.BG_NOTE,activebackground=self.BG_NOTE, command= self.destroy).pack(side=RIGHT)

        self.iconifyButton = Button(Header, image=self.minimize_IMG, command=self.minimize,  bg=self.BG_NOTE, activebackground=self.BG_NOTE)
        self.iconifyButton.pack(side=RIGHT)

        Button(Header, compound=TOP, image=self.minimizeAtRightSide_IMG, bg=self.BG_NOTE,activebackground=self.BG_NOTE, command= self.minimize_at_right_side).pack(side=RIGHT)

        self.text_box = AutoResizedText(self.maximizedNote, bd=0, bg=self.BG_NOTE, width=min_width, height=min_height)
        self.text_box.pack(expand=YES, fill=BOTH)

        self.text_box.bind('<Control-n>', lambda event: self.ask_title_and_create_window())
        self.text_box.bind('<Control-N>', lambda event: self.ask_title_and_create_window())
        self.text_box.bind('<Control-o>', lambda event: self.open_file())
        self.text_box.bind('<Control-O>', lambda event: self.open_file())
        self.text_box.bind('<Control-s>', lambda event: self.save_file())
        self.text_box.bind('<Control-S>', lambda event: self.save_file())
        self.text_box.bind('<Control-a>', lambda event: self.save_file_as())
        self.text_box.bind('<Control-A>', lambda event: self.save_file_as())
        self.text_box.bind('<Control-h>', lambda event: self.help())
        self.text_box.bind('<Control-H>', lambda event: self.help())

    def save_file(self, whatever = None):
        if not self.filename:
            self.save_file_as()
        else:
            with open(self.filename, 'w') as f:
                f.write(self.text_box.get('1.0', 'end'))

            # Comment out the following 2 lines if you don't want a 
            # pop-up message every time you save a file:
            tkMessageBox.showinfo('FYI', 'File Saved.')
            self.after(1, self.text_box.focus)
        return "break"

    def save_file_as(self, change_title = False):
        self.filename = tkFileDialog.asksaveasfilename(filetypes = self.FILETYPES)
        
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(self.text_box.get('1.0', 'end'))

            if change_title:
                self.title(self.filename)
            # comment out the following line if you don't want a
            # pop-up message every time you save a file:
            tkMessageBox.showinfo('FYI', 'File Saved')

        self.after(1, self.text_box.focus)
        return "break"

    def open_file(self, filename = None, change_title=False):
        if not filename:
            self.filename = tkFileDialog.askopenfilename(filetypes = self.FILETYPES)
        else:
            self.filename = filename

        if not self.filename:
            with open(self.filename, 'r') as f:
                self.text_box.update(f.read())

            if change_title:
                self.title('File %s' % self.filename)

        self.after(1, self.text_box.focus)
        return "break"

    def ask_title_and_create_window(self):
        toplevel = Toplevel()
        
        label = Label(toplevel, text="Title:")
        label.pack(anchor=W)

        entry = Entry(toplevel, width=15)
        entry.pack(anchor=W, fill=X)
        
        entry.bind("<Return>", lambda event: (self.new_window(entry.get()), toplevel.destroy()))
        
        entry.focus()
        
        return "break"

    @classmethod
    def new_window(class_, title):
        desktop_note = class_(root, title)
        desktop_note.text_box.focus()

    def help(self):
        tkMessageBox.showinfo('Tkinter Desktop Notes Help', message = HELP_MESSAGE)
        self.after(1, self.text_box.focus)
        return "break"

    def minimize_at_right_side(self):
        self.disable_dragging()
        self.maximizedNote.pack_forget()
        self.mimizedNote.pack()

        self.x = self.winfo_x()
        self.y = self.winfo_y()

        self.wm_geometry('-0+%d'%self.y)

    def maximize_from_right_side(self):
        self.maximizedNote.pack()
        self.mimizedNote.pack_forget()
        self.wm_geometry('+%d+%d'% (self.x,self.y))
        self.enable_dragging()

    def minimize(self):
        self.text_box.pack_forget()
        self.iconifyButton['command'] = self.maximize
        self.iconifyButton['image'] = self.restore_IMG

    def maximize(self):
        self.text_box.pack(expand=YES, fill=BOTH)
        self.iconifyButton['command'] = self.minimize
        self.iconifyButton['image'] = self.minimize_IMG


if __name__ == '__main__':
    try:
        from Tkinter import Tk, Entry, StringVar, Button, Label
        from Tkconstants import LEFT
    except ImportError:
        from tkinter import Tk, Entry, StringVar, Button, Label
        from tkinter.constants import LEFT

    def create_a_new_note():
        DesktopNote.new_window(title_var.get())
        
    root = Tk()
    Label(root,text="Title:").pack(side=LEFT)

    title_var = StringVar()
    title_var.set('TITLE')

    entry_title = Entry(root, textvariable=title_var)
    entry_title.pack(side=LEFT)
    entry_title.bind('<Return>', lambda event: create_a_new_note() )

    Button(root, text="Create another note", command=create_a_new_note).pack(side=LEFT)

    root.mainloop()
