# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))

import datetime
import collections

try:
    from Tkinter import StringVar, Text, Frame, PanedWindow, Scrollbar, Label, Entry
    from Tkconstants import *
    import ttk
except ImportError:
    from tkinter import StringVar, Text, Frame, PanedWindow, Scrollbar, Label, Entry
    from tkinter.constants import *
    import tkinter.ttk as ttk

User_Message = collections.namedtuple('User_Message', 'nick content')
Notification_Message = collections.namedtuple('Notification_Message', 'content tag')
Notification_Message.__new__.__defaults__ = ('notification',)

Notification_Of_Private_Message = collections.namedtuple('Notification_Message', 'content from_ to')

# TODO: Add frame topic
class Chatbox(object):
    def __init__(self, master, my_nick=None, command=None, topic=None, entry_controls=None, maximum_lines=None, timestamp_template=None, scrollbar_background=None, scrollbar_troughcolor=None, history_background=None, history_font=None, history_padx=None, history_pady=None, history_width=None, entry_font=None, entry_background=None, entry_foreground=None, label_template=u"{nick}", label_font=None, logging_file=None, tags=None):
        self.interior = Frame(master, class_="Chatbox")

        self._command = command

        self._is_empty = True

        self._maximum_lines = maximum_lines
        self._timestamp_template = timestamp_template
        
        self._command = command

        self._label_template = label_template
        
        self._logging_file = logging_file
        
        if logging_file is None:
            self._log = None
        else:
            try:
                self._log = open(logging_file, "r")
            except:
                self._log = None
        
        top_frame = Frame(self.interior, class_="Top")
        top_frame.pack(expand=True, fill=BOTH)
                
        self._textarea = Text(top_frame, state=DISABLED)

        self._vsb = Scrollbar(top_frame, takefocus=0, command=self._textarea.yview)
        self._vsb.pack(side=RIGHT, fill=Y)

        self._textarea.pack(side=RIGHT, expand=YES, fill=BOTH)
        self._textarea["yscrollcommand"]=self._vsb.set
        
        entry_frame = Frame(self.interior, class_="Chatbox_Entry")
        entry_frame.pack(fill=X, anchor=N)
        
        if entry_controls is not None:
            controls_frame = Frame(entry_frame, class_="Controls")
            controls_frame.pack(fill=X)
            entry_controls(controls_frame, chatbox=self)
            
            bottom_of_entry_frame = Frame(entry_frame)
            self._entry_label = Label(bottom_of_entry_frame)
            self._entry = Entry(bottom_of_entry_frame)
        else:            
            self._entry_label = Label(entry_frame)
            self._entry = Entry(entry_frame)
        
        self._entry.pack(side=LEFT, expand=YES, fill = X)
        self._entry.bind("<Return>", self._on_message_sent)
        
        self._entry.focus()

        if history_background:
            self._textarea.configure(background=history_background)
        
        if history_font:
            self._textarea.configure(font=history_font)

        if history_padx:
             self._textarea.configure(padx=history_padx)
             
        if history_width:
             self._textarea.configure(width=history_width)

        if history_pady:
            self._textarea.configure(pady=history_pady)

        if scrollbar_background:
            self._vsb.configure(background = scrollbar_background)

        if scrollbar_troughcolor:
            self._vsb.configure(troughcolor = scrollbar_troughcolor)

        if entry_font:
            self._entry.configure(font=entry_font)

        if entry_background:
            self._entry.configure(background=entry_background)
            
        if entry_foreground:
            self._entry.configure(foreground=entry_foreground)
        
        if label_font:
            self._entry_label.configure(font=label_font)

        if tags:
            for tag, tag_config in tags.items():
                self._textarea.tag_config(tag, **tag_config)
                
        self.set_nick(my_nick)

    @property
    def topic(self):
        return
        
    @topic.setter
    def topic(self, topic):
        return
        
    def focus_entry(self):
        self._entry.focus()

    def bind_entry(self, event, handler):
        self._entry.bind(event, handler)
        
    def bind_textarea(self, event, handler):
        self._textarea.bind(event, handler)
        
    def bind_tag(self, tagName, sequence, func, add=None):
        self._textarea.tag_bind(tagName, sequence, func, add=add) 
        
    def focus(self):
        self._entry.focus()

    def user_message(self, nick, content):
        if self._timestamp_template is None:
            self._write((u"%s:"%nick, "nick"), " ", (content, "user_message"))
        else:
            timestamp = datetime.datetime.now().strftime(self._timestamp_template)
            self._write((timestamp, "timestamp"), " ", (u"%s:"%nick, "nick"), " ", (content, "user_message"))

    def notification_message(self, content, tag=None):
        if tag is None:
            tag = "notification"

        self._write((content, tag))
        
    notification = notification_message
    
    def notification_of_private_message(self, content, from_, to):
        if self._timestamp_template is None:
            self.notification_message(u"{from_} -> {to}: {content}".format(from_=from_, to=to, content=content), "notification_of_private_message")
        else:
            timestamp = datetime.datetime.now().strftime(self._timestamp_template)
            self.notification_message(u"{timestamp} {from_} -> {to}: {content}".format(timestamp=timestamp, from_=from_, to=to, content=content), "notification_of_private_message")
        
    def new_message(self, message):
        if isinstance(message, User_Message):
            self.user_message(message.content, message.nick)
        elif isinstance(message, Notification_Message):
            self.notification(message.content, message.tag)
        elif isinstance(message, Notification_Of_Private_Message):
            self.notification_of_private_message(message.from_, message.to, message.content)
        else:
            raise Exception("Bad message")

    def tag(self, tag_name, **kwargs):
        self._textarea.tag_config(tag_name, **kwargs)

    def clear(self):
        self._is_empty = True
        self._textarea.delete('1.0', END)

    @property
    def logging_file(self):
        return self._logging_file

    def send(self, content):
        if self._my_nick is None:
            raise Exception("Nick not set")

        self.user_message(self._my_nick, content)

    def _filter_text(self, text):
        return "".join(ch for ch in text if ch <= u"\uFFFF")
    
    def _write(self, *args):
        if len(args) == 0: return
            
        relative_position_of_scrollbar = self._vsb.get()[1]
        
        self._textarea.config(state=NORMAL)
        
        if self._is_empty:
            self._is_empty = False
        else:
            self._textarea.insert(END, "\n")
            if self._log is not None:
                self._log.write("\n")

        for arg in args:
            if isinstance(arg, tuple):
                text, tag = arg
                        # Parsing not allowed characters
                text = self._filter_text(text)
                self._textarea.insert(END, text, tag)
            else:
                text = arg

                text = self._filter_text(text)
                self._textarea.insert(END, text)
            
            if self._log is not None:
                self._log.write(text)

        if self._maximum_lines is not None:
            start_line = int(self._textarea.index('end-1c').split('.')[0]) -self._maximum_lines 
            
            if lines_to_delete >= 1:
                self._textarea.delete('%s.0'%start_line, END)

        self._textarea.config(state=DISABLED)
        
        if relative_position_of_scrollbar == 1:
            self._textarea.yview_moveto(1)

    def _on_message_sent(self, event):
        message = self._entry.get()
        self._entry.delete(0, END)
        
        self.send(message)

        if self._command:
            self._command(message)

    def set_nick(self, my_nick):
        self._my_nick = my_nick

        if my_nick:
            text = self._label_template.format(nick=my_nick)

            self._entry_label["text"] = text
            self._entry_label.pack(side=LEFT,padx=(5,5), before=self._entry)
        else:
            self._entry_label.pack_forget()

if __name__ == "__main__":

    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root = Tk()
    root.title("Chat megawidget")

    def command(txt):
        print(txt)

    chatbox = Chatbox(root, my_nick="user1", command=command)
    chatbox.user_message("user2", "hello guys")
    
    chatbox.send("Hi, you are welcome!")
    chatbox.interior.pack(expand=True, fill=BOTH)

    root.mainloop()
