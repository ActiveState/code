import tkinter
import tkinter.ttk
import getpass
import uuid
import os
import time
import traceback

# XXX The file will be obsolete by tomorrow.

HOLD = 'Logos Storage'

################################################################################

class Logos(tkinter.ttk.Frame):

    @classmethod
    def main(cls):
        # Create and configure the root.
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        root.title('Logos')
        root.minsize(200, 200)
        # Create Logos and setup for resizing.
        view = cls(root)
        view.grid(row=0, column=0, sticky=tkinter.NSEW)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        # Enter the main GUI event loop.
        root.mainloop()

    ########################################################################

    # These are all instance methods.

    def __init__(self, master):
        super().__init__(master)
        # Get the username and save list of found files.
        self.__user = getpass.getuser()
        self.__dirlist = set()
        # Create widgets.
        self.__log = tkinter.Text(self)
        self.__bar = tkinter.ttk.Scrollbar(self, orient=tkinter.VERTICAL,
                                           command=self.__log.yview)
        self.__ent = tkinter.ttk.Entry(self, cursor='xterm')
        # Configure widgets.
        self.__log.configure(state=tkinter.DISABLED, wrap=tkinter.WORD,
                             yscrollcommand=self.__bar.set)
        # Create binding.
        self.__ent.bind('<Return>', self.create_message)
        # Position widgets.
        self.__log.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.__bar.grid(row=0, column=1, sticky=tkinter.NS)
        self.__ent.grid(row=1, column=0, columnspan=2, sticky=tkinter.EW)
        # Configure resizing.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Focus entry.
        self.__ent.focus_set()
        # Schedule message discovery.
        self.after_idle(self.get_messages)

    def get_messages(self):
        # Schedule method for one second from now.
        self.after(1000, self.get_messages)
        # Get a list of new files.
        files = set(os.listdir(HOLD))
        diff = files - self.__dirlist
        self.__dirlist = files
        # Load each new message.
        messages = []
        for name in diff:
            path = os.path.join(HOLD, name)
            try:
                with open(path) as file:
                    user, clock, message = self.load_message(file)
                messages.append((user, float(clock), message))
            except:
                # Print any error for debugging purposes.
                traceback.print_exc()
                os.remove(path)
        # Sort the messages according to time and display them.
        messages.sort(key=lambda m: m[1])
        for m in messages:
            self.display_message(m[0], m[2])

    def display_message(self, user, text):
        # Put a new message on the screen.
        self.__log['state'] = tkinter.NORMAL
        message = '{} - {}\n'.format(user, text)
        self.__log.insert('1.0', message)
        self.__log['state'] = tkinter.DISABLED

    def create_message(self, event):
        # Get the text, clear it, show on screen, and create file.
        text = event.widget.get()
        event.widget.delete(0, tkinter.END)
        self.display_message(self.__user, text)
        self.save_file(text)

    def save_file(self, message):
        # Save message in HOLD using a UUID for the name.
        name = uuid.uuid1().hex
        path = os.path.join(HOLD, name)
        self.__dirlist.add(name)
        with open(path, 'w') as file:
            self.save_message(file, message)

    ########################################################################

    # If one the format is changed, both methods must be altered.

    def load_message(self, file):
        # Read the file, splitting on newline, and get first three lines.
        user, clock, message = file.read().split('\n')[:3]
        return user, clock, message

    def save_message(self, file, message):
        # Save username, timestamp, and message on separate lines.
        print(self.__user, file=file)
        print(time.time(), file=file)
        print(message, file=file, end='')

################################################################################

if __name__ == '__main__':
    Logos.main()
