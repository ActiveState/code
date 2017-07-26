try:
    from Tkinter import Frame, Entry, Tk
except ImportError:
    from tkinter import Frame, Entry, Tk
    

root = Tk()
frame1 = Frame(root, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=100, height=100, bd= 0)
frame1.pack()
frame1.pack_propagate(False)

Entry(frame1).pack()


frame2 = Frame(root, highlightbackground="red", highlightcolor="red", highlightthickness=1, width=100, height=100, bd= 0)
frame2.pack()
frame2.pack_propagate(False)

Entry(frame2).pack()

root.mainloop()
