# file: LabeledEntry.py
# A simple example of moving options and
# geometry methods from a widget to another
# Pedro Werneck <pedro.werneck@bol.com.br>

from Tkinter import *


class LabeledEntry(Entry):
    """
    An Entry widget with an attached Label
    """
    def __init__(self, master=None, **kw):
        """
        Valid resource names: background, bd, bg, borderwidth, cursor,
        exportselection, fg, font, foreground, highlightbackground,
        highlightcolor, highlightthickness, insertbackground,
        insertborderwidth, insertofftime, insertontime, insertwidth,
        invalidcommand, invcmd, justify, relief, selectbackground,
        selectborderwidth, selectforeground, show, state, takefocus,
        textvariable, validate, validatecommand, vcmd, width,
        xscrollcommand.
        
        The following options apply to the Label: text, textvariable,
        anchor, bitmap, image
        
        The following options apply to the Geometry manager: padx, pady,
        fill, side
        """
        fkw = {}                                       # Frame options dictionary
        lkw = {'name':'label'}                         # Label options dictionary
        skw = {'padx':0, 'pady':0, 'fill':'x',         # Geometry manager options dictionary
                'side':'left'}
        fmove = ('name',)                               # Options to move to the Frame dictionary
        lmove = ('text', 'textvariable',
                 'anchor','bitmap', 'image')            # Options to move to the Label dictionary
        smove = ('side', 'padx', 'pady','side')         # Options to move to the Geometry manager dictionary

        for k in kw.keys():
            if type(k) == ClassType or k in fmove:
                fkw[k] = kw[k]
                del kw[k]
            elif k in lmove:
                lkw[k] = kw[k]
                del kw[k]
            elif k in smove:
                skw[k] = kw[k]
                del kw[k]

        self.body = apply(Frame, (master, ), fkw)
        self.label = apply(Label, (self.body,), lkw)
        self.label.pack(side='left', fill=skw['fill'], padx=skw['padx'], pady=skw['pady'])
        apply(Entry.__init__, (self, self.body), kw)
        self.pack(side=skw['side'], fill=skw['fill'], padx=skw['padx'], pady=skw['pady'])


        methods = (Pack.__dict__.keys() +              # Set Frame geometry methods to self.
                   Grid.__dict__.keys() +
                   Place.__dict__.keys())              
        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.body, m))       


if __name__ == '__main__':
    root = Tk()
    le1 = LabeledEntry(root, name='label1', text='Label 1: ', width=5, relief=SUNKEN, bg='white', padx=3)
    le2 = LabeledEntry(root, name='label2', text='Label 2: ', relief=SUNKEN, bg='red', padx=3)
    le3 = LabeledEntry(root, name='label3', text='Label 3: ', width=40, relief=SUNKEN, bg='yellow', padx=3)

    le1.pack(expand=1, fill=X)
    le2.pack(expand=1, fill=X)
    le3.pack(expand=1, fill=X)
    root.mainloop()
