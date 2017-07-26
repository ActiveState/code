import os
import sys
import random
import cPickle
import tkFileDialog
import tkSimpleDialog
import tkMessageBox
import tkColorChooser
import Tkinter
import StringIO
from Tkinter import *
from winreg import *

# Check on DEFAULT_IMAGE data.

DEFAULT_IMAGE = 'GIF89a \x00 \x00\xf7\x00\x00\x00\x00\x00\x80\x00\x00\x00\x80\x00\x80\x80\x00\x00\x00\x80\x80\x00\x80\x00\x80\x80\x80\x80\x80\xc0\xc0\xc0\xff\x00\x00\x00\xff\x00\xff\xff\x00\x00\x00\xff\xff\x00\xff\x00\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003\x00\x00f\x00\x00\x99\x00\x00\xcc\x00\x00\xff\x003\x00\x0033\x003f\x003\x99\x003\xcc\x003\xff\x00f\x00\x00f3\x00ff\x00f\x99\x00f\xcc\x00f\xff\x00\x99\x00\x00\x993\x00\x99f\x00\x99\x99\x00\x99\xcc\x00\x99\xff\x00\xcc\x00\x00\xcc3\x00\xccf\x00\xcc\x99\x00\xcc\xcc\x00\xcc\xff\x00\xff\x00\x00\xff3\x00\xfff\x00\xff\x99\x00\xff\xcc\x00\xff\xff3\x00\x003\x0033\x00f3\x00\x993\x00\xcc3\x00\xff33\x0033333f33\x9933\xcc33\xff3f\x003f33ff3f\x993f\xcc3f\xff3\x99\x003\x9933\x99f3\x99\x993\x99\xcc3\x99\xff3\xcc\x003\xcc33\xccf3\xcc\x993\xcc\xcc3\xcc\xff3\xff\x003\xff33\xfff3\xff\x993\xff\xcc3\xff\xfff\x00\x00f\x003f\x00ff\x00\x99f\x00\xccf\x00\xfff3\x00f33f3ff3\x99f3\xccf3\xffff\x00ff3fffff\x99ff\xccff\xfff\x99\x00f\x993f\x99ff\x99\x99f\x99\xccf\x99\xfff\xcc\x00f\xcc3f\xccff\xcc\x99f\xcc\xccf\xcc\xfff\xff\x00f\xff3f\xffff\xff\x99f\xff\xccf\xff\xff\x99\x00\x00\x99\x003\x99\x00f\x99\x00\x99\x99\x00\xcc\x99\x00\xff\x993\x00\x9933\x993f\x993\x99\x993\xcc\x993\xff\x99f\x00\x99f3\x99ff\x99f\x99\x99f\xcc\x99f\xff\x99\x99\x00\x99\x993\x99\x99f\x99\x99\x99\x99\x99\xcc\x99\x99\xff\x99\xcc\x00\x99\xcc3\x99\xccf\x99\xcc\x99\x99\xcc\xcc\x99\xcc\xff\x99\xff\x00\x99\xff3\x99\xfff\x99\xff\x99\x99\xff\xcc\x99\xff\xff\xcc\x00\x00\xcc\x003\xcc\x00f\xcc\x00\x99\xcc\x00\xcc\xcc\x00\xff\xcc3\x00\xcc33\xcc3f\xcc3\x99\xcc3\xcc\xcc3\xff\xccf\x00\xccf3\xccff\xccf\x99\xccf\xcc\xccf\xff\xcc\x99\x00\xcc\x993\xcc\x99f\xcc\x99\x99\xcc\x99\xcc\xcc\x99\xff\xcc\xcc\x00\xcc\xcc3\xcc\xccf\xcc\xcc\x99\xcc\xcc\xcc\xcc\xcc\xff\xcc\xff\x00\xcc\xff3\xcc\xfff\xcc\xff\x99\xcc\xff\xcc\xcc\xff\xff\xff\x00\x00\xff\x003\xff\x00f\xff\x00\x99\xff\x00\xcc\xff\x00\xff\xff3\x00\xff33\xff3f\xff3\x99\xff3\xcc\xff3\xff\xfff\x00\xfff3\xffff\xfff\x99\xfff\xcc\xfff\xff\xff\x99\x00\xff\x993\xff\x99f\xff\x99\x99\xff\x99\xcc\xff\x99\xff\xff\xcc\x00\xff\xcc3\xff\xccf\xff\xcc\x99\xff\xcc\xcc\xff\xcc\xff\xff\xff\x00\xff\xff3\xff\xfff\xff\xff\x99\xff\xff\xcc\xff\xff\xff!\xf9\x04\x01\x00\x00\x10\x00,\x00\x00\x00\x00 \x00 \x00\x00\x08\xbd\x00Q\x08\x1cH\xb0\xa0\xc1\x83\x08\x13*\\\xc8\xad\xa1\xc3\x87\x0e\x05\x1a\x99H\xb1"E\x82\x1036\x94h\xb1\xa3\x11\x8c\x1a!r\xf4X\x11d\xc8\x88(HZ4y\x92\xdbH\x95\x1f\x07\xb6D\t\xf3\xa2\xcc\x99.S\xd6\x8c)\x10g\xce\x9d<Q\xf8|\xa9\x92\xe5I\xa2$\x8d\x86D\xeaQ\xa9F\xa6\x1d\x9df\x84\xbar\xa1\xd5\xabX\xb3\nl\xc1\xb5\xab\xd7\xae\x02\xf5\x89\x1dKv,\xc1\xafh\xb9\x86-\xcbV\xdf\xd9\xb4_\xd7\xb6%\xfb\x16.X\x14s\xcb\xd6\xb5\xdbBn^\xb7\x03\xf9\xde\xfdk6\xb0\xe0\xbex\t\x03\xdez\xd8o\xde\xbdv\x1d\xcf\x85\x0cWr[\xcai-\xb3\xc5\x8cV\xb3^\xc3\x82=\xd3\xd5J\xba4\xd6\x80\x00;'

if not os.path.isdir('images'):
    if os.path.exists('images'):
        os.remove('images')
    os.mkdir('images')

if not os.path.isfile('images\\default.gif'):
    if os.path.exists('images\\default.gif'):
        os.rmdir('images\\default.gif')
    file('images\\default.gif', 'wb').write(DEFAULT_IMAGE)

# Define some helper classes.

class PhotoImage(Tkinter.PhotoImage):

    def __init__(self, name=None, cnf={}, master=None, **kw):
        Tkinter.PhotoImage.__init__(self, name, cnf, master, **kw)
        self.file = kw['file']

class Shortcut(tkSimpleDialog.Dialog):

    def __init__(self, parent, widget, title=None):
        self.widget = widget
        tkSimpleDialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        self.filename = LabelFrame(master, text='Filename')
        self.entry = Entry(self.filename)
        if hasattr(self.widget, 'shortcut'):
            self.entry.insert(0, self.widget.shortcut)
        self.entry.grid(row=0, column=0, padx=5, pady=5)
        self.button = Button(self.filename, text='Browse...', command=self.command)
        self.button.grid(row=0, column=1, padx=5, pady=5)
        self.filename.pack()
        return self.entry

    def command(self):
        filename = tkFileDialog.Open().show()
        if filename:
            filename = filename.replace('/', '\\')
            self.widget.shortcut = filename
            self.entry.delete(0, END)
            self.entry.insert(0, filename)

    def apply(self):
        self.widget.shortcut = self.entry.get()

    def validate(self):
        if os.path.exists(self.entry.get()):
            return True
        else:
            tkMessageBox.showerror('Error', 'File does not exist.')
            return False

class Create_PhotoImage(tkSimpleDialog.Dialog):

    def __init__(self, parent, reference, event, title):
        self.reference = reference
        self.event = event
        tkSimpleDialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        self.filename = LabelFrame(master, text='Filename')
        self.entry = Entry(self.filename)
        self.entry.grid(row=0, column=0, padx=5, pady=5)
        self.button = Button(self.filename, text='Browse...', command=self.commander)
        self.button.grid(row=0, column=1, padx=5, pady=5)
        self.filename.pack()
        return self.entry

    def commander(self):
        filename = tkFileDialog.askopenfilename(filetypes=[('GIF files', '*.gif')])
        if filename.lower().endswith('.gif'):
            self.entry.delete(0, END)
            self.entry.insert(0, filename.replace('/', '\\'))

    def validate(self):
        if os.path.exists(self.entry.get()) and self.entry.get().lower().endswith('.gif'):
            return True
        else:
            tkMessageBox.showerror('Error', 'File cannot be used..')
            return False

    def apply(self):
        global w, h
        filename = self.entry.get()
        canvas = self.event.widget
        put(canvas, PhotoImage(file=filename), float(self.event.x) / w, float(self.event.y) / h)

# Define action on exit.        

def do_exit(event):
##    all = media.find_all()
##    options = [media.config()['background'][-1]]
##    for item in all:
##        options.append([reference[item].file, media.coords(item)])
##        if hasattr(reference[item], 'shortcut'):
##            options[-1].append(reference[item].shortcut)
##    cPickle.dump(options, file('shell.ini', 'wb'), -1)
##    event.widget.quit()
    software = Key(key=HKEY.CURRENT_USER, sub_key='Software')
    if 'Atlantis Zero' not in software.keys:
        software.keys = 'Atlantis Zero'
    az = Key(key=software, sub_key='Atlantis Zero')
    if 'Demo Shell' not in az.keys:
        az.keys = 'Demo Shell'
    ds = Key(key=az, sub_key='Demo Shell')
    if 'winreg' not in ds.keys:
        ds.keys = 'winreg'
    winreg = Key(key=ds, sub_key='winreg', sam=KEY.ALL_ACCESS)
    del winreg.values
    winreg.values['background'] = REG_BINARY(media.config()['background'][-1])
    for index, item in enumerate(media.find_all()):
        temp = [reference[item].file, media.coords(item)]
        if hasattr(reference[item], 'shortcut'):
            temp.append(reference[item].shortcut)
        winreg.values['IMAGE_%s' % (index + 1)] = REG_BINARY(cPickle.dumps(temp, -1))
    event.widget.quit()

# Start setting up the GUI.

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(True)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
root.bind("<Escape>", do_exit)

reference = dict()
os.chdir(os.path.dirname(sys.argv[0]))

def put(media, image, x, y):
    media_w, media_h = int(media.config()['width'][-1]), int(media.config()['height'][-1])
    start_w, start_h = image.width() / 2, image.height() / 2
    stop_w, stop_h = media_w - start_w, media_h - start_h
    position = (stop_w - start_w) * x + start_w, (stop_h - start_h) * y + start_h
    handle = media.create_image(position, image=image)
    reference[handle] = image
    return handle

def files():
    return [os.path.join(os.getcwd(), 'images', name) for name in os.listdir(os.path.join(os.getcwd(), 'images'))]

curx = cury = selected = None

def select(event):
    global selected, curx, cury
    selected = event.widget.find_withtag(CURRENT)
    if not selected:
        selected = None
    else:
        selected = selected[0]
        curx, cury = event.x, event.y
        event.widget.tag_raise(selected)

def move(event):
    global curx, cury
    canvas = event.widget
    sel = canvas.find_withtag(CURRENT)
    if sel:
        sel = sel[0]
    if sel and sel == selected:
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasx(event.y)
        canvas.move(selected, event.x - curx, event.y - cury)
        curx = event.x
        cury = event.y

def activate(event):
    global selected
    canvas = event.widget
    sel = canvas.find_withtag(CURRENT)
    if sel:
        sel = sel[0]
    if sel and sel == selected:
        selected = None
        widget = reference[sel]
        if hasattr(widget, 'shortcut') and os.path.exists(widget.shortcut):
            os.chdir(os.path.dirname(widget.shortcut))
            os.startfile(widget.shortcut)
        else:
            filename = tkFileDialog.Open().show()
            if filename:
                widget.shortcut = filename.replace('/', '\\')

def new_PhotoImage():
    Create_PhotoImage(root, reference, the_event, 'New Shortcut')

def edit_PhotoImage():
    Shortcut(root, selected_PhotoImage, 'Shortcut')

def delete_PhotoImage():
    global the_canvas, selected
    if len(reference) == 1:
        tkMessageBox.showerror('Error', 'Cannot delete last shortcut.')
    else:
        the_canvas.delete(selected)
        del reference[selected]

shortcut_menu = Menu(root, tearoff=0)
shortcut_menu.add_command(label='New', command=new_PhotoImage)
shortcut_menu.add_command(label='Edit', command=edit_PhotoImage)
shortcut_menu.add_command(label='Delete', command=delete_PhotoImage)

def properties(event):
    global selected_PhotoImage, selected, the_canvas, the_event
    canvas = event.widget
    sel = canvas.find_withtag(CURRENT)
    if sel:
        selected_PhotoImage = reference[sel[0]]
        selected = sel[0]
        the_canvas = canvas
        the_event = event
        shortcut_menu.post(event.x_root, event.y_root)
    else:
        color = tkColorChooser.askcolor(canvas.config()['background'][-1])
        if color[1]:
            canvas.config(background=color[1])

media = Canvas(root, width=w, height=h)
media.bind('<Button-1>', select)
media.bind('<B1-Motion>', move)
media.bind('<Double-Button-1>', activate)
media.bind('<Button-3>', properties)
media.pack()

# CONFIGURATION

def do_config():
##    options = cPickle.load(file('shell.ini', 'rb'))
##    media.config(background=options[0])
##    for item in options[1:]:
##        name = item[0]
##        coords = item[1]
##        image = PhotoImage(file=name)
##        reference[media.create_image(coords, image=image)] = image
##        if len(item) == 3:
##            image.shortcut = item[2]
    option = Key(key=HKEY.CURRENT_USER, sub_key='Software\\Atlantis Zero\\Demo Shell\\winreg').values
    media.config(background=option['background'].value)
    for name in option:
        if name != 'background':
            item = cPickle.loads(option[name].value)
            name = item[0]
            coords = item[1]
            image = PhotoImage(file=name)
            reference[media.create_image(coords, image=image)] = image
            if len(item) == 3:
                image.shortcut = item[2]

def do_setup():
    if len(sys.argv) > 1 and sys.argv[1] == 'random':
        do_random = True
    else:
        do_random = False
    if do_random:
        media.config(background='#ffffff')
    else:
        media.config(background='#00007f')
    names = files()
    random.shuffle(names)
    for name in names:
        if name.lower().endswith('default.gif'):
            calibrate = name
        elif name.lower().endswith('.gif') and do_random:
            image = PhotoImage(file=name)
            put(media, image, random.random(), random.random())
    for x in range(2):
        for y in range(2):
            media.tag_lower(put(media, PhotoImage(file=calibrate), x, y))
            
##if os.path.exists('shell.ini'):
try:
    do_config()
except:
    do_setup()
##else:
##    do_setup()

root.mainloop()
