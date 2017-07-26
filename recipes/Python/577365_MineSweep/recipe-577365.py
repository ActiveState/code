################################################################################
# Version 1
################################################################################

import tkinter
import functools

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height):
        root = tkinter.Tk()
        window = cls(root, width, height)
        root.mainloop()

    def __init__(self, master, width, height):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__build_buttons()
        self.grid()

    def __build_buttons(self):
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self)
                button.grid(column=x, row=y)
                button['text'] = '?'
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __push(self, x, y):
        print('Column = {}\nRow = {}'.format(x, y))

if __name__ == '__main__':
    MineSweep.main(10, 10)

################################################################################
# Version 2
################################################################################

import tkinter
import functools
import random

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        window = cls(root, width, height, mines)
        root.mainloop()

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__started = False
        self.__build_buttons()
        self.grid()

    def __build_buttons(self):
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self)
                button.grid(column=x, row=y)
                button['text'] = '?'
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __push(self, x, y):
        if not self.__started:
            self.__build_mines()
            while self.__buttons[y][x].mine:
                self.__build_mines()
            self.__started = True
        button = self.__buttons[y][x]
        text = 'NY'[button.mine] + '({}, {})'.format(x, y)
        button['text'] = text

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 3
################################################################################

import tkinter
import functools
import random

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        window = cls(root, width, height, mines)
        root.mainloop()

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__started = False
        self.__build_buttons()
        self.grid()

    def __build_buttons(self):
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self)
                button.grid(column=x, row=y)
                button['text'] = '?'
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __push(self, x, y):
        if not self.__started:
            self.__build_mines()
            while self.__buttons[y][x].mine:
                self.__build_mines()
            self.__started = True
        button = self.__buttons[y][x]
        if button.mine:
            button['text'] = 'X'
        else:
            button['text'] = str(self.__total(x, y))
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        return count

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 4
################################################################################

import tkinter
import functools
import random

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        window = cls(root, width, height, mines)
        root.mainloop()

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__started = False
        self.__build_buttons()
        self.grid()

    def __build_buttons(self):
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self)
                button.grid(column=x, row=y)
                button['text'] = '?'
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __push(self, x, y):
        if not self.__started:
            self.__build_mines()
            while self.__buttons[y][x].mine:
                self.__build_mines()
            self.__started = True
        button = self.__buttons[y][x]
        if not button.pushed:
            button.pushed = True
            if button.mine:
                button['text'] = 'X'
            else:
                count = self.__total(x, y)
                button['text'] = count and str(count) or ' '
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            for x_offset in range(-1, 2):
                x_index = x + x_offset
                for y_offset in range(-1, 2):
                    y_index = y + y_offset
                    if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                        self.__push(x_index, y_index)
        return count

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 5
################################################################################

import tkinter
import functools
import random

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        window = cls(root, width, height, mines)
        root.mainloop()

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__started = False
        self.__playing = True
        self.__build_buttons()
        self.grid()

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=0,
                                 columnspan=10, sticky=tkinter.EW)
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self)
                button.grid(column=x, row=y+1)
                button['text'] = '?'
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button['text'] = '?'
        self.__started = False
        self.__playing = True

    def __push(self, x, y):
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
            button = self.__buttons[y][x]
            if not button.pushed:
                button.pushed = True
                if button.mine:
                    button['text'] = 'X'
                    self.__playing = False
                else:
                    count = self.__total(x, y)
                    button['text'] = count and str(count) or ' '
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            for x_offset in range(-1, 2):
                x_index = x + x_offset
                for y_offset in range(-1, 2):
                    y_index = y + y_offset
                    if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                        self.__push(x_index, y_index)
        return count

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 6
################################################################################

import tkinter
import functools
import random
from tkinter.simpledialog import askstring

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        window = cls(root, width, height, mines)
        root.mainloop()

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__build_buttons()
        self.grid()

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=0,
                                 columnspan=10, sticky=tkinter.EW)
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self)
                button.grid(column=x, row=y+1)
                button['text'] = '?'
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button['text'] = '?'
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height

    def __push(self, x, y):
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
            button = self.__buttons[y][x]
            if not button.pushed:
                self.__push_button(button, x, y)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
        else:
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        name = askstring('New Record', 'What is your name?')
        if name is not None:
            print(name, 'has won!')
        else:
            print("I don't know who you are!")
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 7
################################################################################

import tkinter
import functools
import random
from tkinter.simpledialog import askstring

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('MineSweep')
        window = cls(root, width, height, mines)
        root.mainloop()

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__build_timer()
        self.__build_buttons()
        self.grid()

    def __build_timer(self):
        self.__time = tkinter.IntVar()
        self.__timer = tkinter.Label(textvariable=self.__time)
        self.__timer.grid(columnspan=10, sticky=tkinter.EW)

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=1,
                                 columnspan=10, sticky=tkinter.EW)
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self, width=2, height=1, text='?')
                button.grid(column=x, row=y+2)
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button['text'] = '?'
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height

    def __push(self, x, y):
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
            button = self.__buttons[y][x]
            if not button.pushed:
                self.__push_button(button, x, y)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
        else:
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        name = askstring('New Record', 'What is your name?')
        if name is not None:
            print(name, 'has won!')
        else:
            print("I don't know who you are!")
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 8
################################################################################

import tkinter
import functools
import random
from tkinter.simpledialog import askstring

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('MineSweep')
        window = cls(root, width, height, mines)
        root.mainloop()

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__build_timer()
        self.__build_buttons()
        self.grid()

    def __build_timer(self):
        self.__secs = tkinter.IntVar()
        self.__timer = tkinter.Label(textvariable=self.__secs)
        self.__timer.grid(columnspan=10, sticky=tkinter.EW)
        self.__after_handle = None

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=1,
                                 columnspan=10, sticky=tkinter.EW)
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self, width=2, height=1, text='?')
                button.grid(column=x, row=y+2)
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button['text'] = '?'
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height
        if self.__after_handle is not None:
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        self.__secs.set(0)

    def __push(self, x, y):
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
                self.__after_handle = self.after(1000, self.__tick)
            button = self.__buttons[y][x]
            if not button.pushed:
                self.__push_button(button, x, y)

    def __tick(self):
        self.__after_handle = self.after(1000, self.__tick)
        self.__secs.set(self.__secs.get() + 1)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        else:
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.after_cancel(self.__after_handle)
                self.__after_handle = None
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        name = askstring('New Record', 'What is your name?')
        if name is not None:
            print(name, 'has won!')
        else:
            print("I don't know who you are!")
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 9
################################################################################

import tkinter
import functools
import random
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import pickle

################################################################################

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines):
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('MineSweep')
        window = cls(root, width, height, mines)
        root.mainloop()

################################################################################

    def __init__(self, master, width, height, mines):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__scores = ScoreTable()
        self.__build_timer()
        self.__build_buttons()
        self.grid()

    def __build_timer(self):
        self.__secs = tkinter.IntVar()
        self.__timer = tkinter.Label(textvariable=self.__secs)
        self.__timer.grid(columnspan=10, sticky=tkinter.EW)
        self.__after_handle = None

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=1,
                                 columnspan=10, sticky=tkinter.EW)
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self, width=2, height=1, text='?')
                button.grid(column=x, row=y+2)
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button['text'] = '?'
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height
        if self.__after_handle is not None:
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        self.__secs.set(0)

    def __push(self, x, y):
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
                self.__after_handle = self.after(1000, self.__tick)
            button = self.__buttons[y][x]
            if not button.pushed:
                self.__push_button(button, x, y)

    def __tick(self):
        self.__after_handle = self.after(1000, self.__tick)
        self.__secs.set(self.__secs.get() + 1)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        else:
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.after_cancel(self.__after_handle)
                self.__after_handle = None
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        score = self.__secs.get()
        if self.__scores.eligible(score):
            name = askstring('New Record', 'What is your name?')
            if name is None:
                name = 'Anonymous'
            self.__scores.add(name, score)
        else:
            showinfo('You did not get on the high score table.')
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'
        for name, score in self.__scores.listing():
            print('{:20}{}'.format(name, score))
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

################################################################################

class ScoreTable:

    def __init__(self, size=10):
        self.__data = {999: [''] * size}

    def add(self, name, score):
        assert self.eligible(score)
        if score in self.__data:
            self.__data[score].insert(0, name)
        else:
            self.__data[score] = [name]
        if len(self.__data[max(self.__data)]) == 1:
            del self.__data[max(self.__data)]
        else:
            del self.__data[max(self.__data)][-1]

    def eligible(self, score):
        return score <= max(self.__data)

    def listing(self):
        for key in sorted(self.__data.keys()):
            for name in self.__data[key]:
                yield name, key

################################################################################

if __name__ == '__main__':
    MineSweep.main(10, 10, 10)

################################################################################
# Version 10
################################################################################

import tkinter
import functools
import random
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import pickle
import os.path

################################################################################

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines, scores):
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('MineSweep')
        window = cls(root, width, height, mines, scores)
        root.protocol('WM_DELETE_WINDOW', window.close)
        root.mainloop()

################################################################################

    def __init__(self, master, width, height, mines, scores):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__scores = ScoreTable()
        self.__record_file = scores
        if os.path.isfile(scores):
            self.__scores.load(scores)
        self.__build_timer()
        self.__build_buttons()
        self.grid()

    def close(self):
        self.__scores.save(self.__record_file)
        self.quit()

    def __build_timer(self):
        self.__secs = tkinter.IntVar()
        self.__timer = tkinter.Label(textvariable=self.__secs)
        self.__timer.grid(columnspan=10, sticky=tkinter.EW)
        self.__after_handle = None

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=1,
                                 columnspan=10, sticky=tkinter.EW)
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self, width=2, height=1, text='?')
                button.grid(column=x, row=y+2)
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button['text'] = '?'
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height
        if self.__after_handle is not None:
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        self.__secs.set(0)

    def __push(self, x, y):
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
                self.__after_handle = self.after(1000, self.__tick)
            button = self.__buttons[y][x]
            if not button.pushed:
                self.__push_button(button, x, y)

    def __tick(self):
        self.__after_handle = self.after(1000, self.__tick)
        self.__secs.set(self.__secs.get() + 1)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        else:
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.after_cancel(self.__after_handle)
                self.__after_handle = None
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        score = self.__secs.get()
        if self.__scores.eligible(score):
            name = askstring('New Record', 'What is your name?')
            if name is None:
                name = 'Anonymous'
            self.__scores.add(name, score)
        else:
            showinfo('You did not get on the high score table.')
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'
        for name, score in self.__scores.listing():
            print('{:20}{}'.format(name, score))
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

################################################################################

class ScoreTable:

    def __init__(self, size=10):
        self.__data = {999: [''] * size}

    def add(self, name, score):
        assert self.eligible(score)
        if score in self.__data:
            self.__data[score].insert(0, name)
        else:
            self.__data[score] = [name]
        if len(self.__data[max(self.__data)]) == 1:
            del self.__data[max(self.__data)]
        else:
            del self.__data[max(self.__data)][-1]

    def eligible(self, score):
        return score <= max(self.__data)

    def listing(self):
        for key in sorted(self.__data.keys()):
            for name in self.__data[key]:
                yield name, key

    def load(self, filename):
        self.__data = pickle.load(open(filename, 'rb'))

    def save(self, filename):
        pickle.dump(self.__data, open(filename, 'wb'))

################################################################################

if __name__ == '__main__':
    MineSweep.main(10, 10, 10, 'scores.dat')

################################################################################
# Version 11
################################################################################

import tkinter
import functools
import random
from tkinter.simpledialog import askstring, Dialog
from tkinter.messagebox import showinfo
import pickle
import os.path

################################################################################

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines, scores):
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('MineSweep')
        window = cls(root, width, height, mines, scores)
        root.protocol('WM_DELETE_WINDOW', window.close)
        root.mainloop()

################################################################################

    def __init__(self, master, width, height, mines, scores):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__scores = ScoreTable()
        self.__record_file = scores
        if os.path.isfile(scores):
            self.__scores.load(scores)
        self.__build_timer()
        self.__build_buttons()
        self.grid()

    def close(self):
        self.__scores.save(self.__record_file)
        self.quit()

    def __build_timer(self):
        self.__secs = tkinter.IntVar()
        self.__timer = tkinter.Label(textvariable=self.__secs)
        self.__timer.grid(columnspan=10, sticky=tkinter.EW)
        self.__after_handle = None

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=1,
                                 columnspan=10, sticky=tkinter.EW)
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self, width=2, height=1, text='?')
                button.grid(column=x, row=y+2)
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button['text'] = '?'
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height
        if self.__after_handle is not None:
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        self.__secs.set(0)

    def __push(self, x, y):
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
                self.__after_handle = self.after(1000, self.__tick)
            button = self.__buttons[y][x]
            if not button.pushed:
                self.__push_button(button, x, y)

    def __tick(self):
        self.__after_handle = self.after(1000, self.__tick)
        self.__secs.set(self.__secs.get() + 1)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        else:
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.after_cancel(self.__after_handle)
                self.__after_handle = None
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        score = self.__secs.get()
        if self.__scores.eligible(score):
            name = askstring('New Record', 'What is your name?')
            if name is None:
                name = 'Anonymous'
            self.__scores.add(name, score)
        else:
            showinfo('You did not get on the high score table.')
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'
        HighScoreView(self, 'High Scores', self.__scores.listing())
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False

################################################################################

class ScoreTable:

    def __init__(self, size=10):
        self.__data = {999: [''] * size}

    def add(self, name, score):
        assert self.eligible(score)
        if score in self.__data:
            self.__data[score].insert(0, name)
        else:
            self.__data[score] = [name]
        if len(self.__data[max(self.__data)]) == 1:
            del self.__data[max(self.__data)]
        else:
            del self.__data[max(self.__data)][-1]

    def eligible(self, score):
        return score <= max(self.__data)

    def listing(self):
        for key in sorted(self.__data.keys()):
            for name in self.__data[key]:
                yield name, key

    def load(self, filename):
        self.__data = pickle.load(open(filename, 'rb'))

    def save(self, filename):
        pickle.dump(self.__data, open(filename, 'wb'))

################################################################################

class HighScoreView(Dialog):

    def __init__(self, parent, title, generator):
        self.__scores = generator
        super().__init__(parent, title)

    def body(self, master):
        self.__labels = []
        for row, (name, score) in enumerate(self.__scores):
            label = tkinter.Label(master, text=name)
            self.__labels.append(label)
            label.grid(row=row, column=0)
            label = tkinter.Label(master, text=str(score))
            self.__labels.append(label)
            label.grid(row=row, column=1)
        self.__okay = tkinter.Button(master, command=self.ok, text='Okay')
        self.__okay.grid(ipadx=100, columnspan=2, column=0, row=row+1)
        return self.__okay

    def buttonbox(self):
        pass

################################################################################

if __name__ == '__main__':
    MineSweep.main(10, 10, 10, 'scores.dat')

################################################################################
# Version 12
################################################################################

import tkinter
import functools
import random
from tkinter.simpledialog import askstring, Dialog
from tkinter.messagebox import showinfo
import os.path

################################################################################

class MineSweep(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines, scores):
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('MineSweep')
        window = cls(root, width, height, mines, scores)
        root.protocol('WM_DELETE_WINDOW', window.close)
        root.mainloop()

################################################################################

    def __init__(self, master, width, height, mines, scores):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__scores = ScoreTable()
        self.__record_file = scores
        if os.path.isfile(scores):
            self.__scores.load(scores)
        self.__build_timer()
        self.__build_buttons()
        self.grid()

    def close(self):
        self.__scores.save(self.__record_file)
        self.quit()

    def __build_timer(self):
        self.__secs = tkinter.IntVar()
        self.__timer = tkinter.Label(textvariable=self.__secs)
        self.__timer.grid(columnspan=self.__width, sticky=tkinter.EW)
        self.__after_handle = None

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=1,
                                 columnspan=self.__width, sticky=tkinter.EW)
        self.__reset_button.blink_handle = None
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self, width=2, height=1,
                                        text='?', fg='red')
                button.grid(column=x, row=y+2)
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button.config(text='?', fg='red')
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height
        if self.__after_handle is not None:
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        self.__secs.set(0)

    def __push(self, x, y, real=True):
        button = self.__buttons[y][x]
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
                self.__after_handle = self.after(1000, self.__tick)
            if not button.pushed:
                self.__push_button(button, x, y)
            elif real:
                self.__blink(button, button['bg'], 'red')
        elif real:
            self.__blink(button, button['bg'], 'red')

    def __blink(self, button, from_bg, to_bg, times=8):
        if button.blink_handle is not None and times == 8:
            return
        button['bg'] = (to_bg, from_bg)[times & 1]
        times -= 1
        if times:
            blinker = functools.partial(self.__blink, button,
                                        from_bg, to_bg, times)
            button.blink_handle = self.after(250, blinker)
        else:
            button.blink_handle = None

    def __tick(self):
        self.__after_handle = self.after(1000, self.__tick)
        self.__secs.set(self.__secs.get() + 1)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
            self.__blink(self.__reset_button, button['bg'], 'red')
        else:
            button['fg'] = 'SystemButtonText'
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.after_cancel(self.__after_handle)
                self.__after_handle = None
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        score = self.__secs.get()
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'
        if self.__scores.eligible(score):
            name = askstring('New Record', 'What is your name?')
            if name is None:
                name = 'Anonymous'
            self.__scores.add(name, score)
        else:
            showinfo('You did not get on the high score table.')
        HighScoreView(self, 'High Scores', self.__scores.listing())
        
    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index, False)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False
                button.blink_handle = None

################################################################################

class ScoreTable:

    def __init__(self, size=10):
        self.__data = {999: [''] * size}

    def add(self, name, score):
        assert self.eligible(score)
        if score in self.__data:
            self.__data[score].insert(0, name)
        else:
            self.__data[score] = [name]
        if len(self.__data[max(self.__data)]) == 1:
            del self.__data[max(self.__data)]
        else:
            del self.__data[max(self.__data)][-1]

    def eligible(self, score):
        return score <= max(self.__data)

    def listing(self):
        for key in sorted(self.__data.keys()):
            for name in self.__data[key]:
                yield name, key

    def load(self, filename):
        self.__data = eval(open(filename, 'r').read())

    def save(self, filename):
        open(filename, 'w').write(repr(self.__data))

################################################################################

class HighScoreView(Dialog):

    def __init__(self, parent, title, generator):
        self.__scores = generator
        super().__init__(parent, title)

    def body(self, master):
        self.__labels = []
        for row, (name, score) in enumerate(self.__scores):
            label = tkinter.Label(master, text=name)
            self.__labels.append(label)
            label.grid(row=row, column=0)
            label = tkinter.Label(master, text=str(score))
            self.__labels.append(label)
            label.grid(row=row, column=1)
        self.__okay = tkinter.Button(master, command=self.ok, text='Okay')
        self.__okay.grid(ipadx=100, columnspan=2, column=0, row=row+1)
        return self.__okay

    def buttonbox(self):
        pass

################################################################################

if __name__ == '__main__':
    MineSweep.main(10, 10, 10, 'scores.txt')
