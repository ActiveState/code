'''The Accordion widget inherits from Tkinter's Frame class and provides stacked
expandable and collapseable containers for displaying other widgets.

Compliant with Python 2.5-2.7

Author: @ifthisthenbreak
'''

from Tkinter import Tk, Frame, PhotoImage, Label


class Chord(Frame):
    '''Tkinter Frame with title argument'''
    def __init__(self, parent, title='', *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.title = title

class Accordion(Frame):
    def __init__(self, parent, accordion_style=None):
        Frame.__init__(self, parent)

        # if no style dict, assign default style
        if accordion_style:
            self.style = accordion_style
        else:
            self.style = accordion_style = {
                'title_bg': 'ghost white',
                'title_fg': 'black',
                'highlight': 'white smoke'
                }
        
        self.columnconfigure(0, weight=1)
        
    def append_chords(self, chords=[]):
        '''pass a [list] of Chords to the Accordion object'''

        self.update_idletasks()
        row = 0
        width = max([c.winfo_reqwidth() for c in chords])
        
        for c in chords:
            i = PhotoImage() # blank image to force Label to use pixel size
            label = Label(self, text=c.title,
                          image=i,
                          compound='center',
                          width=width,
                          bg=self.style['title_bg'],
                          fg=self.style['title_fg'],
                          bd=2, relief='groove')
            
            label.grid(row=row, column=0)
            c.grid(row=row+1, column=0, sticky='nsew')
            c.grid_remove()
            row += 2
            
            label.bind('<Button-1>', lambda e,
                       c=c: self._click_handler(c))
            label.bind('<Enter>', lambda e,
                       label=label, i=i: label.config(bg=self.style['highlight']))
            label.bind('<Leave>', lambda e,
                       label=label, i=i: label.config(bg=self.style['title_bg']))
                       
    def _click_handler(self, chord):
        if len(chord.grid_info()) == 0:
            chord.grid()
        else:
            chord.grid_remove()
        
            
if __name__ == '__main__':
    from Tkinter import Entry, Button, Text


    root = Tk()

    # create the Accordion
    acc = Accordion(root)
    
    # first chord
    first_chord = Chord(acc, title='First Chord', bg='white')
    Label(first_chord, text='hello world', bg='white').pack()

    # second chord
    second_chord = Chord(acc, title='Second Chord', bg='white')
    Entry(second_chord).pack()
    Button(second_chord, text='Button').pack()

    # third chord
    third_chord = Chord(acc, title='Third Chord', bg='white')
    Text(third_chord).pack()

    # append list of chords to Accordion instance
    acc.append_chords([first_chord, second_chord, third_chord])
    acc.pack(fill='both', expand=1)

    root.mainloop()
