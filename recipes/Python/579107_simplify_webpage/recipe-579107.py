#!/usr/bin/torify /usr/bin/python
import Tkinter
import tkFont
import requests
import html2text
import urllib2

class TkDND(object):

    def __init__(self, master):
        master.tk.eval('package require tkdnd')
        self.master = master
        self.tk = master.tk
        self._subst_format = ('%A', '%a', '%b', '%D', '%d', '%m', '%T',
                '%W', '%X', '%Y', '%x', '%y')
        self._subst_format_str = " ".join(self._subst_format)

    def bindtarget(self, window, callback, dndtype, event='<Drop>', priority=50):
        cmd = self._prepare_tkdnd_func(callback)
        return self.tk.call('dnd', 'bindtarget', window, dndtype, event,
                cmd, priority)
                
    def _prepare_tkdnd_func(self, callback):
        funcid = self.master.register(callback, self._dndsubstitute)
        cmd = ('%s %s' % (funcid, self._subst_format_str))
        return cmd               

    def _dndsubstitute(self, *args):
        if len(args) != len(self._subst_format):
            return args

        def try_int(x):
            x = str(x)
            try:
                return int(x)
            except ValueError:
                return x

        A, a, b, D, d, m, T, W, X, Y, x, y = args

        event = Tkinter.Event()
        event.action = A       # Current action of the drag and drop operation.
        event.action_list = a  # Action list supported by the drag source.
        event.mouse_button = b # Mouse button pressed during the drag and drop.
        event.data = D         # The data that has been dropped.
        event.descr = d        # The list of descriptions.
        event.modifier = m     # The list of modifier keyboard keys pressed.
        event.dndtype = T
        event.widget = self.master.nametowidget(W)
        event.x_root = X       # Mouse pointer x coord, relative to the root win.
        event.y_root = Y
        event.x = x            # Mouse pointer x coord, relative to the widget.
        event.y = y
        event.action_list = str(event.action_list).split()

        for name in ('mouse_button', 'x', 'y', 'x_root', 'y_root'):
            setattr(event, name, try_int(getattr(event, name)))
        return (event, )

class TextPlus(Tkinter.Text):
    def __init__(self, *args, **kwargs):
        Tkinter.Text.__init__(self, *args, **kwargs)
        _rc_menu_install(self)
        # overwrite default class binding so we don't need to return "break"
        self.bind_class("Text", "<Control-a>", self.event_select_all)  
        self.bind("<Button-3><ButtonRelease-3>", self.show_menu)

    def event_select_all(self, *args):
        self.focus_force()        
        self.tag_add("sel","1.0","end")

    def show_menu(self, e):
        self.tk.call("tk_popup", self.menu, e.x_root, e.y_root)

class EntryPlus(Tkinter.Entry):
    def __init__(self, *args, **kwargs):
        Tkinter.Entry.__init__(self, *args, **kwargs)
        _rc_menu_install(self, go=True)
        # overwrite default class binding so we don't need to return "break"
        self.bind_class("Entry", "<Control-a>", self.event_select_all)  
        self.bind("<Button-3><ButtonRelease-3>", self.show_menu)

    def event_select_all(self, *args):
        self.focus_force()
        self.selection_range(0, Tkinter.END)

    def event_paste_and_go(self, *args):
        self.delete(0,Tkinter.END)
        self.focus_force()
        self.event_generate("<<Paste>>")
        handlereturn(self)

    def show_menu(self, e):
        self.tk.call("tk_popup", self.menu, e.x_root, e.y_root)

def _rc_menu_install(w, go = False):
    w.menu = Tkinter.Menu(w, tearoff=0)
    w.menu.add_command(label="Cut")
    w.menu.add_command(label="Copy")
    w.menu.add_command(label="Paste")
    if go:
        w.menu.add_command(label="Paste & Go")
    w.menu.add_separator()
    w.menu.add_command(label="Select all")        

    w.menu.entryconfigure("Cut", command=lambda: w.focus_force() or w.event_generate("<<Cut>>"))
    w.menu.entryconfigure("Copy", command=lambda: w.focus_force() or w.event_generate("<<Copy>>"))
    w.menu.entryconfigure("Paste", command=lambda: w.focus_force() or w.event_generate("<<Paste>>"))
    if go:
        w.menu.entryconfigure("Paste & Go", command=w.event_paste_and_go)
    w.menu.entryconfigure("Select all", command=w.event_select_all) 

def handle(event):
    event.widget.delete(0,Tkinter.END)
    url = event.data.strip()
    event.widget.insert(0,url)
    textwindow(url)

def handlereturn(entry):
    p = entry.get().splitlines()[0]
    if not p.startswith('http'):
        p = 'file://'+ p
    textwindow(p)
    
def convert65536(s):
    #convert out-of-range characters 
    res = []
    for c in s:
        k = ord(c)
        if k < 65536:
            res.append(c)
        else:
            res.append("{"+str(k)+"?}")
    return "".join(res)
    
def gethtml(link):
    user_agent = "Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0"
    headers={'user-agent':user_agent}
    s = requests.Session()
    try:
        res = s.get(link,headers=headers).text
    except requests.exceptions.InvalidSchema:
        req=urllib2.Request(link,None,headers)
        r = urllib2.urlopen(req)
        res = r.read().decode('utf8')
    return res

def textwindow(url):
    title = url
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    s = gethtml(url)
    s = h.handle(s)
    s = h.unescape(s)
    text = convert65536(s)
    top = Tkinter.Toplevel()
    top.geometry("+200+100")
    top.title(title)
    top.bind("<Escape>", lambda _ : top.destroy())
    S = Tkinter.Scrollbar(top)
    customFont = tkFont.Font(family="Arial", size=16)
    T = TextPlus(top,height=20,width=78,font=customFont,bg="lightgrey")
    S.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)
    T.pack(side=Tkinter.LEFT,fill=Tkinter.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(Tkinter.END,text)

def main():
    root = Tkinter.Tk()
    root.geometry("950x32+200+32")
    root.title('markdown')
    dnd = TkDND(root)
    customFont = tkFont.Font(family="Arial", size=14)
    entry = EntryPlus(font=customFont,bg="lightgrey")
    entry.pack(expand=1,fill='both')
    dnd.bindtarget(entry,handle,'text/plain')
    entry.bind("<Return>", lambda _ : handlereturn(entry))
    root.mainloop()

if __name__=="__main__":
    main()
