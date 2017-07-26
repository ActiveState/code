## Accordion Widget (Tkinter)  
Originally published: 2014-07-17 18:03:32  
Last updated: 2014-07-18 11:39:51  
Author: Peter Mojeiko  
  
An expanding/collapsing widget for Tkinter.

usage:

    from accordion import Accordion, Chord
    root = Tk()
    accordion = Accordion(root)
    accordion.pack()
    chord1 = Chord(accordion, title='Chord')
    # create widgets and give them chord1 as parent
    accordion.append_chords([chord1])
    root.mainloop()

There's a more detailed example at the bottom of the file.