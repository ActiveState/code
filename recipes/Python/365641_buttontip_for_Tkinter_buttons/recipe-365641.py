#!/usr/bin/python
from Tkinter import *

tipDelay = 1000


class TipButton(Button):
    def __init__(self,parent=None,tip='',**kw):
        Button.__init__(self,parent,kw)
        self.bind('<Enter>',self._delayedshow)
        self.bind('<Button-1>',self._leave)
        self.bind('<Leave>',self._leave)

        self.frame = Toplevel(self,bd=1,bg="black")
        self.frame.withdraw()
        self.frame.overrideredirect(1)
        self.frame.transient()     
        l=Label(self.frame,text=tip,bg="yellow",justify='left')
	l.update_idletasks()
        l.pack()
	l.update_idletasks()
        self.tipwidth = l.winfo_width()
        self.tipheight = l.winfo_height()

    def _delayedshow(self,event):
        self.focus_set()
        self.request=self.after(tipDelay,self._show)


    def _show(self):
        self.update_idletasks()
        FixX = self.winfo_rootx()+self.winfo_width()
        FixY = self.winfo_rooty()+self.winfo_height()
        if FixX + self.tipwidth > self.winfo_screenwidth():
            FixX = FixX-self.winfo_width()-self.tipwidth
        if FixY + self.tipheight > self.winfo_screenheight():
            FixY = FixY-self.winfo_height()-self.tipheight
        self.frame.geometry('+%d+%d'%(FixX,FixY))
        self.frame.deiconify()
#       print self.frame.geometry()
#	print self.winfo_screenwidth()

        
    def _leave(self,event):
        self.frame.withdraw()
        self.after_cancel(self.request)


#--- testing ---

if __name__ == '__main__':
    def log(a):
        print a

    main = Tk()
    b1 = TipButton(main,"tip1",text="Example1",\
                  command=(lambda e="tip1": log(e)))
    b2 = TipButton(main,"tip2",text="Example2",\
                  command=(lambda e="tip2": log(e)))
    b1.pack()
    b2.pack()


    main.mainloop()

### end module ###
