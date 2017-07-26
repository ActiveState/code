import source   # Access the source
source.main()   # and execute main.

####################
# source/__init__.py
####################

import tkinter, time, os, sys, test.support
import xml.sax._exceptions

from tkinter import Label, Frame, LabelFrame, Entry, Button
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showwarning, showerror

from . import exe_queue, gui_logs, splash, teach_me, testbank

################################################################################

def main():
    with test.support.captured_output('stderr') as stderr:
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        with splash.Splash(root, 'images//QuizMe Logo.gif', 3):
            # Set up the root window.
            root.title('QuizMe 2.5')
            root.resizable(False, False)
            root.wm_iconbitmap(default='images//Icon.ico')
            # Create the program GUI.
            application = QuizMe(root)
            application.grid()
        mainloop(root)
    cleanup(stderr)

def mainloop(root):
    # Threading Support Experiment
    gui_logs.root = exe_queue.Pipe(root)
    while True:
        try:
            root.update()
        except:
            return
        time.sleep(1 / 64)
        gui_logs.root.update()

def cleanup(stream):
    # Record Any Errors
    value = stream.getvalue()
    if value:
        today = time.asctime()
        ruler = '=' * len(today)
        stamp = '{1}\n{0}\n{1}\n'.format(today, ruler)
        file = open('error.log', 'at')
        file.write(stamp)
        file.write(value)
        file.close()

################################################################################

class QuizMe(Frame):

    PROMPT = 'What testbank do you want to open?'

    def __init__(self, master):
        # Initialize the Frame object.
        super().__init__(master)
        # Create every opening widget.
        self.intro = Label(self, text=self.PROMPT)
        self.group = LabelFrame(self, text='Filename')
        self.entry = Entry(self.group, width=35)
        self.click = Button(self.group, text='Browse ...', command=self.file)
        self.enter = Button(self, text='Continue', command=self.start)
        # Make Windows entry bindings.
        def select_all(event):
            event.widget.selection_range(0, tkinter.END)
            return 'break'
        self.entry.bind('<Control-Key-a>', select_all)
        self.entry.bind('<Control-Key-/>', lambda event: 'break')
        # Position them in this frame.
        options = {'sticky': tkinter.NSEW, 'padx': 5, 'pady': 5}
        self.intro.grid(row=0, column=0, **options)
        self.group.grid(row=1, column=0, **options)
        self.entry.grid(row=0, column=0, **options)
        self.click.grid(row=0, column=1, **options)
        self.enter.grid(row=2, column=0, **options)

    def file(self):
        # Find filename for self.entry
        options = {'defaultextension': '.xml',
                   'filetypes': [('All', '*'), ('XML', '.xml')],
                   'initialdir': os.path.join(os.getcwd(), 'tests'),
                   'parent': self,
                   'title': 'Testbank to Open'}
        filename = askopenfilename(**options)
        if filename:
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, filename)

    def start(self):
        # Validate self.entry and begin
        path = self.entry.get()
        if os.path.exists(path):
            if os.path.isfile(path):
                try:
                    bank = testbank.parse(path)
                    engine = teach_me.FAQ(bank)
                except xml.sax._exceptions.SAXParseException as error:
                    title = error.getMessage().title()
                    LN = error.getLineNumber()
                    CN = error.getColumnNumber()
                    message = 'Line {}, Column {}'.format(LN, CN)
                    showerror(title, message, master=self)
                except AssertionError as error:
                    title = 'Validation Error'
                    message = error.args[0]
                    showerror(title, message, master=self)
                except:
                    title = 'Error'
                    message = 'Unknown exception was thrown!'
                    showerror(title, message, master=self)
                else:
                    self.done = False
                    self.next_event = iter(engine).__next__
                    self.after_idle(self.execute_quiz)
            else:
                title = 'Warning'
                message = 'File does not exist.'
                showwarning(title, message, master=self)
        else:
            title = 'Information'
            message = 'Path does not exist.'
            showinfo(title, message, master=self)

    def execute_quiz(self):
        # Follow the logic from the last program.
        # This will be called to handle an event.
        try:
            event = self.next_event()
        except StopIteration:
            assert self.done, 'Final event not processed!'
        else:
            if isinstance(event, teach_me.Enter):
                gui_logs.ShowStatus(self, 'Entering', event, self.execute_quiz)
            elif isinstance(event, teach_me.Exit):
                gui_logs.ShowStatus(self, 'Exiting', event, self.execute_quiz)
                self.last_exit = event.kind
            elif isinstance(event, teach_me.Question):
               gui_logs. AskQuestion(self, event, self.execute_quiz)
            elif isinstance(event, teach_me.Report):
                flag = [True]
                if self.last_exit == 'Section' and event.wrong:
                    flag[0] = False
                    gui_logs.ReviewProblems(self, event, flag)
                if flag[0]:
                    gui_logs.ShowReport(self, event, self.execute_quiz)
                if event.final:
                    title = 'Congratulations!'
                    message = 'You have finished the test.'
                    showinfo(title, message, master=self)
                    self.done = True
            else:
                title = 'Type Error'
                message = repr(event)
                showerror(title, message, master=self)
