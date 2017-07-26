from Tkinter import *

class MultiListbox(Frame):
    def __init__(self, master, lists):
	Frame.__init__(self, master)
	self.lists = []
	for l,w in lists:
	    frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
	    Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
	    lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
			 relief=FLAT, exportselection=FALSE)
	    lb.pack(expand=YES, fill=BOTH)
	    self.lists.append(lb)
	    lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
	    lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
	    lb.bind('<Leave>', lambda e: 'break')
	    lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
	    lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
	frame = Frame(self); frame.pack(side=LEFT, fill=Y)
	Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
	sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
	sb.pack(expand=YES, fill=Y)
	self.lists[0]['yscrollcommand']=sb.set

    def _select(self, y):
	row = self.lists[0].nearest(y)
	self.selection_clear(0, END)
	self.selection_set(row)
	return 'break'

    def _button2(self, x, y):
	for l in self.lists: l.scan_mark(x, y)
	return 'break'

    def _b2motion(self, x, y):
	for l in self.lists: l.scan_dragto(x, y)
	return 'break'

    def _scroll(self, *args):
	for l in self.lists:
	    apply(l.yview, args)

    def curselection(self):
	return self.lists[0].curselection()

    def delete(self, first, last=None):
	for l in self.lists:
	    l.delete(first, last)

    def get(self, first, last=None):
	result = []
	for l in self.lists:
	    result.append(l.get(first,last))
	if last: return apply(map, [None] + result)
	return result
	    
    def index(self, index):
	self.lists[0].index(index)

    def insert(self, index, *elements):
	for e in elements:
	    i = 0
	    for l in self.lists:
		l.insert(index, e[i])
		i = i + 1

    def size(self):
	return self.lists[0].size()

    def see(self, index):
	for l in self.lists:
	    l.see(index)

    def selection_anchor(self, index):
	for l in self.lists:
	    l.selection_anchor(index)

    def selection_clear(self, first, last=None):
	for l in self.lists:
	    l.selection_clear(first, last)

    def selection_includes(self, index):
	return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
	for l in self.lists:
	    l.selection_set(first, last)

if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='MultiListbox').pack()
    mlb = MultiListbox(tk, (('Subject', 40), ('Sender', 20), ('Date', 10)))
    for i in range(1000):
	mlb.insert(END, ('Important Message: %d' % i, 'John Doe', '10/10/%04d' % (1900+i)))
    mlb.pack(expand=YES,fill=BOTH)
    tk.mainloop()
