####################
# source/gui_logs.py
####################

from tkinter import messagebox, simpledialog, font
from tkinter import Frame, Label, Button, StringVar
from tkinter import NSEW, LEFT, W, DISABLED, NORMAL
import textwrap, functools

################################################################################

TITLE_SIZE = 16
TEXT_WIDTH = 40

################################################################################

class _Dialog(simpledialog.Dialog):

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        try:
            self.apply()
        finally:
            self.cancel(force=True)

    def cancel(self, event=None, force=False):
        title = 'Warning'
        message = 'Are you sure you want\nto stop taking this test?'
        if force or messagebox.askyesno(title, message, master=self):
            if self.parent is not None:
                self.parent.focus_set()
            self.destroy()

################################################################################

class ShowStatus(_Dialog):

    WAIT = 3

    def __init__(self, parent, title, message, callback):
        self.message = message
        self.callback = callback
        super().__init__(parent, title)

    def body(self, master):
        style = font.Font(self, size=TITLE_SIZE)
        self.status = Label(master, text=self.message, font=style)
        self.status.grid(sticky=NSEW, padx=TITLE_SIZE, pady=TITLE_SIZE)
        return self.status

    def buttonbox(self):
        self.after(self.WAIT * 1000, self.ok)

    def apply(self):
        root.after_idle(self.callback)

################################################################################

class AskQuestion(_Dialog):

    def __init__(self, parent, event, callback):
        self.question = textwrap.wrap(event.question, TEXT_WIDTH)
        self.choices = event.choices
        self.answer = event.answer
        self.callback = callback
        super().__init__(parent, event.category)

    def body(self, master):
        self.labels = []
        for line in self.question:
            self.labels.append(Label(master, text=line, justify=LEFT))
            self.labels[-1].grid(sticky=NSEW)

    def buttonbox(self):
        self.buttons = []
        box = Frame(self)
        for choice in self.choices:
            options = {'text': textwrap.fill(choice, TEXT_WIDTH),
                       'width': TEXT_WIDTH,
                       'command': functools.partial(self.click, choice)}
            self.buttons.append(Button(box, **options))
            self.buttons[-1].grid(padx=5, pady=5)
        box.pack()

    def click(self, choice):
        self.answer(choice)
        self.ok()

    def apply(self):
        root.after_idle(self.callback)

################################################################################

class ReviewProblems(_Dialog):

    def __init__(self, parent, event, flag):
        self.problems = list(event.problems())
        self.problem = 0
        self.flag = flag
        super().__init__(parent, 'Problems')

    def body(self, master):
        title = font.Font(self, size=TITLE_SIZE)
        legend = font.Font(self, weight='bold')
        # Create display variables.
        self.category = StringVar(master)
        self.question = StringVar(master)
        self.answer = StringVar(master)
        self.right = StringVar(master)
        # Create form labels.
        self.c_label = Label(master, textvariable=self.category, font=title)
        self.q_label = Label(master, textvariable=self.question)
        self.you_answered = Label(master, text='You answered:', font=legend)
        self.a_label = Label(master, textvariable=self.answer)
        self.right_answer = Label(master, text='Right answer:', font=legend)
        self.r_label = Label(master, textvariable=self.right)
        # Create control buttons.
        options = {'text': '< < <',
                   'width': TEXT_WIDTH // 2,
                   'command': self.go_back}
        self.back = Button(master, **options)
        options = {'text': '> > >',
                   'width': TEXT_WIDTH // 2,
                   'command': self.go_next}
        self.next = Button(master, **options)
        # Display the body.
        options = {'sticky': NSEW, 'padx': 5, 'pady': 5}
        self.c_label.grid(row=0, column=0, columnspan=2, **options)
        self.q_label.grid(row=1, column=0, columnspan=2, **options)
        self.you_answered.grid(row=2, column=0, **options)
        self.a_label.grid(row=2, column=1, **options)
        self.right_answer.grid(row=3, column=0, **options)
        self.r_label.grid(row=3, column=1, **options)
        self.back.grid(row=4, column=0, **options)
        self.next.grid(row=4, column=1, **options)
        # Update the labels.
        self.update()
        
    def go_back(self):
        self.problem -= 1
        self.update()

    def go_next(self):
        self.problem += 1
        self.update()

    def update(self):
        # Update the labels.
        problem = self.problems[self.problem]
        self.category.set(problem.category)
        self.question.set(textwrap.fill(problem.question, TEXT_WIDTH))
        self.answer.set(textwrap.fill(problem.answer, TEXT_WIDTH // 2))
        self.right.set(textwrap.fill(problem.right, TEXT_WIDTH // 2))
        # Update the buttons.
        if self.problem == 0:
            self.back['state'] = DISABLED
        else:
            self.back['state'] = NORMAL
        if self.problem + 1 == len(self.problems):
            self.next['state'] = DISABLED
        else:
            self.next['state'] = NORMAL

    def apply(self):
        self.flag[0] = True

################################################################################

class ShowReport(_Dialog):
    
    RULE = '='

    def __init__(self, parent, event, callback):
        self.level = event.level
        self.right = event.right
        self.wrong = event.wrong
        self.total = event.total
        self.callback = callback
        super().__init__(parent, 'Report')

    def body(self, master):
        title = font.Font(self, size=TITLE_SIZE)
        legend = {'anchor': W,
                  'justify': LEFT,
                  'font': font.Font(self, weight='bold')}
        # Create all labels.
        text = 'Cumulative score for\nprevious {}:'.format(self.level)
        self.explanation = Label(master, text=text, font=title)
        self.ruler_one = Label(master, text=(self.RULE * TEXT_WIDTH))
        self.answers_right = Label(master, text='Answers right:', **legend)
        self.display_right = Label(master, text=str(self.right))
        self.answers_wrong = Label(master, text='Answers wrong:', **legend)
        self.display_wrong = Label(master, text=str(self.wrong))
        self.percent = Label(master, text='Percentage correct:', **legend)
        percentage = str(int(100 * self.right / self.total + 0.5)) + '%'
        self.display = Label(master, text=percentage)
        self.ruler_two = Label(master, text=(self.RULE * TEXT_WIDTH))
        # Display the results.
        options = {'sticky': NSEW, 'padx': 5, 'pady': 5}
        self.explanation.grid(row=0, column=0, columnspan=2, **options)
        self.ruler_one.grid(row=1, column=0, columnspan=2, **options)
        self.answers_right.grid(row=2, column=0, **options)
        self.display_right.grid(row=2, column=1, **options)
        self.answers_wrong.grid(row=3, column=0, **options)
        self.display_wrong.grid(row=3, column=1, **options)
        self.percent.grid(row=4, column=0, **options)
        self.display.grid(row=4, column=1, **options)
        self.ruler_two.grid(row=5, column=0, columnspan=2, **options)

    def apply(self):
        root.after_idle(self.callback)
