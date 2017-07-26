'''The SuperText class inherits from Tkinter's Text class and provides added
functionality to a standard text widget:

- Option to turn scrollbar on/off
- Right-click pop-up menu
- Two themes included (terminal and typewriter)

Compliant with Python 2.5-2.7

Author: @ifthisthenbreak
'''

from Tkinter import Tk, Frame, Text, Scrollbar, Menu
from tkMessageBox import askokcancel


class SuperText(Text):
    
    def __init__(self, parent, scrollbar=True, **kw):
        
        self.parent = parent
        
        frame = Frame(parent)
        frame.pack(fill='both', expand=True)
        
        # text widget
        Text.__init__(self, frame, **kw)
        self.pack(side='left', fill='both', expand=True)
        
        # scrollbar
        if scrollbar:
            scrb = Scrollbar(frame, orient='vertical', command=self.yview) 
            self.config(yscrollcommand=scrb.set)
            scrb.pack(side='right', fill='y')
        
        # pop-up menu
        self.popup = Menu(self, tearoff=0)
        self.popup.add_command(label='Cut', command=self._cut)
        self.popup.add_command(label='Copy', command=self._copy)
        self.popup.add_command(label='Paste', command=self._paste)
        self.popup.add_separator()
        self.popup.add_command(label='Select All', command=self._select_all)
        self.popup.add_command(label='Clear All', command=self._clear_all)
        self.bind('<Button-3>', self._show_popup)
        
    def apply_theme(self, theme='standard'):
        '''theme=['standard', 'typewriter', 'terminal']'''

        if theme == 'typewriter':
            '''takes all inserted text and inserts it one char every 100ms'''
            text = self.get('1.0', 'end')
            self.delete('1.0', 'end')
            self.char_index = 0
            self._typewriter([char for char in text])
            
        elif theme == 'terminal':
            '''blocky insert cursor'''
            self.cursor = '1.0'
            self.fg = self.cget('fg')
            self.bg = self.cget('bg')
            self.switch = self.fg
            self.config(insertwidth=0)
            self._blink_cursor()
            self._place_cursor()
        
    def _show_popup(self, event):
        '''right-click popup menu'''
        
        if self.parent.focus_get() != self:
            self.focus_set()
        
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()
            
    def _cut(self):
        
        try:
            selection = self.get(*self.tag_ranges('sel'))
            self.clipboard_clear()
            self.clipboard_append(selection)
            self.delete(*self.tag_ranges('sel'))
        except TypeError:
            pass
    
    def _copy(self):
        
        try:
            selection = self.get(*self.tag_ranges('sel'))
            self.clipboard_clear()
            self.clipboard_append(selection)
        except TypeError:
            pass
        
    def _paste(self):
        
        self.insert('insert', self.selection_get(selection='CLIPBOARD'))
        
    def _select_all(self):
        '''selects all text'''
        
        self.tag_add('sel', '1.0', 'end-1c')
        
    def _clear_all(self):
        '''erases all text'''
        
        isok = askokcancel('Clear All', 'Erase all text?', parent=self,
                           default='ok')
        if isok:
            self.delete('1.0', 'end')

    def _typewriter(self, text): # theme: typewriter
        '''after the theme is applied, this method takes all the inserted text
        and types it out one character every 100ms'''

        self.insert('insert', text[self.char_index])
        self.char_index += 1

        if self.char_index == len(text):
            self.after_cancel(self.typer)
        else:
            self.typer = self.after(100, self._typewriter, text)

    def _place_cursor(self): # theme: terminal
        '''check the position of the cursor against the last known position
        every 15ms and update the cursorblock tag as needed'''

        current_index = self.index('insert')

        if self.cursor != current_index:
            self.cursor = current_index
            self.tag_delete('cursorblock')
            
            start = self.index('insert')
            end = self.index('insert+1c')
            
            if start[0] != end[0]:
                self.insert(start, ' ')
                end = self.index('insert')
                
            self.tag_add('cursorblock', start, end)
            self.mark_set('insert', self.cursor)

        self.after(15, self._place_cursor)

    def _blink_cursor(self): # theme: terminal
        '''alternate the background color of the cursorblock tagged text
        every 600 milliseconds'''
        
        if self.switch == self.fg:
            self.switch = self.bg
        else:
            self.switch = self.fg

        self.tag_config('cursorblock', background=self.switch)

        self.after(600, self._blink_cursor)


lorem = '''Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''

def typewriter_sample():
    
    typewriter = SuperText(root, scrollbar=False, font=('Times', 10, 'bold'))
    typewriter.pack(fill='both', expand=True)
    
    typewriter.insert(1.0, lorem)
    typewriter.apply_theme(theme='typewriter')

def terminal_sample():

    options = {'bg': 'black', 'fg': 'green', 'font': ('Courier', 10)}
    
    terminal = SuperText(root, scrollbar=True)
    terminal.pack(fill='both', expand=True)
    
    terminal.insert(1.0, lorem)
    terminal.config(options)
    terminal.apply_theme(theme='terminal')
    
if __name__ == '__main__':
    
    root = Tk()

    typewriter_sample()
    terminal_sample()

    root.mainloop()
