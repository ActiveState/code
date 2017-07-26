## Accordion Widget (Tkinter)

Originally published: 2014-07-17 18:03:32
Last updated: 2014-07-18 11:39:51
Author: Peter Mojeiko

An expanding/collapsing widget for Tkinter.\n\nusage:\n\n    from accordion import Accordion, Chord\n    root = Tk()\n    accordion = Accordion(root)\n    accordion.pack()\n    chord1 = Chord(accordion, title='Chord')\n    # create widgets and give them chord1 as parent\n    accordion.append_chords([chord1])\n    root.mainloop()\n\nThere's a more detailed example at the bottom of the file.