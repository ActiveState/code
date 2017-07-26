# -*- coding: iso-8859-1 -*-

import os
import time
import math
from tkinter import *
from tkinter.font import Font
import tkinter.filedialog
import tkinter.messagebox

# parameters
encodings = ['latin-1','utf-8'] # available text file encodings (default first)
width,height=300,300 # meters canvas dimensions
len1,len2 = 0.85,0.3 # needle dimensions, relative to meter ray
ray = int(0.7*width/2) # meter circle
x0,y0 = width/2,width/2 # position of circle center inside canvas
min_speed,max_speed = 0,400 # minimum and maximum speed, in characters/minute
step_speed = 50 # step between speed marks on meter
min_err,max_err,step_err = 0,10,1 # same for error rate in %

# localisation
langs = {'en':'English','fr':'Français'}
try: # to guess language from locale
    import locale
    default_lang = locale.getdefaultlocale()[0][:2]
    langs[default_lang]
except:
    default_lang = 'en'

_ = {'title':{'en':'Typing skills meter','fr':'Dactylomètre'},
    'exo':{'en':'Exercices','fr':'Exercices'},
    'opts':{'en':'Options','fr':'Options'},
    'paste':{'en':'Paste','fr':'Coller'},
    'open':{'en':'Open...','fr':'Ouvrir...'},
    'clear':{'en':'Clear','fr':'Effacer'},
    'restart':{'en':'Start again','fr':'Recommencer'},
    'encoding':{'en':'Encoding','fr':'Encodage'},
    'speed':{'en':'Speed','fr':'Vitesse'},
    'err':{'en':'Errors','fr':'Erreurs'},
    'cpm':{'en':'Chars/min','fr':'Cars/min'}
    }

def set_libs(lang):
    root.title(_['title'][lang])
    menu.entryconfig(1,label=_['exo'][lang])
    menu.entryconfig(2,label=_['opts'][lang])
    speed.itemconfig(speed.title,text=_['speed'][lang])
    speed.itemconfig(speed.unit,text=_['cpm'][lang])
    errors.itemconfig(errors.title,text=_['err'][lang])
    errors.itemconfig(errors.unit,text='%')
    for i,entry in enumerate(['open','paste','clear','restart']):
        file_menu.entryconfig(i,label=_[entry][lang])
    
root = Tk()
font = Font(family="Courier New",size=12,weight='bold') # text font
meter_font = Font(family="Arial",size=12,weight='normal')

result_box = None
exo = None
t0 = None

class Exercise:

    def __init__(self,text=""):
        self.text = text
        model.delete(1.0,END)
        model.insert(END,self.text)

    def reset(self):
        self.start = None
        self.line,self.col = 1,0
        self.nb_errors = 0
        speed.draw_needle(0)
        errors.draw_needle(0)
        for tag in 'done','error','old_error':
            model.tag_remove(tag,1.0,END)
        model.mark_set(INSERT,1.0)
        model.focus()

class Meter(Canvas):

    def draw(self,vmin,vmax,step,title,unit):
        self.vmin = vmin
        self.vmax = vmax
        x0 = width/2
        y0 = width/2
        ray = int(0.7*width/2)
        self.title = self.create_text(width/2,20,fill="#000",
            font=meter_font)
        self.create_oval(x0-ray*1.1,y0-ray*1.1,x0+ray*1.1,y0+ray*1.1,
            fill="#DDD")
        self.create_oval(x0-ray,y0-ray,x0+ray,y0+ray,fill="#000")
        coef = 0.1
        self.create_oval(x0-ray*coef,y0-ray*coef,x0+ray*coef,y0+ray*coef,
            fill="white")
        for i in range(1+int((vmax-vmin)/step)):
            v = vmin + step*i
            angle = (5+6*((v-vmin)/(vmax-vmin)))*math.pi/4
            self.create_line(x0+ray*math.sin(angle)*0.9,
                y0 - ray*math.cos(angle)*0.9,
                x0+ray*math.sin(angle)*0.98,
                y0 - ray*math.cos(angle)*0.98,fill="#FFF",width=2)
            self.create_text(x0+ray*math.sin(angle)*0.75,
                y0 - ray*math.cos(angle)*0.75,
                text=v,fill="#FFF",font=meter_font)
            if i==int(vmax-vmin)/step:
                continue
            for dv in range(1,5):
                angle = (5+6*((v+dv*(step/5)-vmin)/(vmax-vmin)))*math.pi/4
                self.create_line(x0+ray*math.sin(angle)*0.94,
                    y0 - ray*math.cos(angle)*0.94,
                    x0+ray*math.sin(angle)*0.98,
                    y0 - ray*math.cos(angle)*0.98,fill="#FFF")
        self.unit = self.create_text(width/2,y0+0.8*ray,fill="#FFF",
            font=meter_font)
        self.needle = self.create_line(x0-ray*math.sin(5*math.pi/4)*len2,
            y0+ray*math.cos(5*math.pi/4)*len2,
            x0+ray*math.sin(5*math.pi/4)*len1,
            y0-ray*math.cos(5*math.pi/4)*len1,
            width=2,fill="#FFF")

    def draw_needle(self,v):
        v = max(v,self.vmin)
        v = min(v,self.vmax)
        angle = (5+6*((v-self.vmin)/(self.vmax-self.vmin)))*math.pi/4
        self.coords(self.needle,x0-ray*math.sin(angle)*len2,
            y0+ray*math.cos(angle)*len2,
            x0+ray*math.sin(angle)*len1,
            y0-ray*math.cos(angle)*len1)

def paste():
    global exo
    try:
        txt = root.clipboard_get()
        model.insert(END,txt)
        exo = Exercise(txt)
        exo.reset()
        root.clipboard_clear()
    except:
        return

def open_text():
    global exo
    exo_dir = os.path.join(os.getcwd(),'texts')
    if not os.path.exists(exo_dir):
        os.mkdir(exo_dir)
    filename = tkinter.filedialog.askopenfilename(initialdir=exo_dir)
    if filename:
        src = open(filename,encoding=encoding.get())
        try:
            model_txt = '\n'.join([l.rstrip() for l in src.readlines()])
        except UnicodeDecodeError:
            tkinter.messagebox.showerror('Encoding error',
                message=("Can't open file %s with encoding %s") 
                %(os.path.basename(filename),encoding.get()))
            return
        exo = Exercise(model_txt)
        exo.reset()

def clear():
    global exo
    model.delete(1.0,END)
    exo = None

def start_again():
    global result_box
    if exo is not None:
        exo.reset()
    if result_box is not None:
        result_box.destroy()
        result_box = None

def type_key(event):
    global exo,result_box, t0
    if exo is None:
        return 'break'
    pos = model.index("%s.%s" %(exo.line,exo.col))
    nbcars = len(model.get(0.0,pos))
    if exo is None:
        if nbcars>0:
            model_txt = model.get(0.0,END+"-1 chars")
            model_txt = model_txt.encode('utf-8')
            exo = Exercise(model_txt)
        else:
            return        
    if exo.start is None:
        exo.start = time.time()
    elif nbcars>3:
        carspm = 60*nbcars/(time.time()-exo.start)
        speed.draw_needle(carspm)
        
    pos = model.index("%s.%s" %(exo.line,exo.col))
    pos_see = model.index("%s+30c" %pos)
    model.see(pos_see)
    good = model.get(model.index("%s.%s" %(exo.line,exo.col)))
    typed = event.char
    if event.keysym in ["Shift_L","Shift_R","Multi_key"]:
        return 'break'

    flag = (typed=='\r' and good=='\n') or (good == typed)
    
    if not flag: # error
        exo.nb_errors += 1
        err_txt = "%s error" %exo.nb_errors
        if exo.nb_errors > 1:
            err_txt += "s"
        model.tag_add('error',pos)
    else:
        exo.col += 1
        if good == "\n":
            exo.line += 1
            exo.col = 0
        if 'error' in model.tag_names(pos):
            model.tag_remove('error',pos)
            model.tag_add('old_error',pos)
        else:
            model.tag_add('done',pos)
        model.mark_set(INSERT,model.index('%s+1c' %pos))
    if nbcars:
        err_rate = 100*round(float(exo.nb_errors)/float(nbcars),4)
        errors.draw_needle(err_rate)

    if model.index("%s.%s" %(exo.line,exo.col)) == model.index(END+"-1 chars"):
        result_box = Toplevel(root)
        Label(result_box,text="The exercice is finished").pack()
        Button(result_box,text="Start again",command=start_again).pack()
        Button(result_box,text="Other text",command=open_text).pack()

    return 'break'


encoding = StringVar(root)
encoding.set(encodings[0])
lang = StringVar(root)
lang.set(default_lang)

menu = Menu(root)
file_menu = Menu(menu,tearoff=False)
for command in open_text,paste,clear,start_again:
    file_menu.add_command(command=command)
menu.add_cascade(label="Exercices",menu=file_menu)

options_menu = Menu(menu,tearoff=False)
menuLang = Menu(options_menu,tearoff=0)
for lang in langs:
    menuLang.add_command(label=langs[lang],command=lambda x=lang:set_libs(x))
options_menu.add_cascade(menu=menuLang,label='Language')
menuEncoding = Menu(options_menu,tearoff=0)
for enc in encodings:
    menuEncoding.add_command(label=enc,command=lambda x=enc:encoding.set(x))
options_menu.add_cascade(menu=menuEncoding,label='Encoding')
menu.add_cascade(label="Options",menu=options_menu)

root.config(menu=menu)

# meters zone
meters = Frame(root,width=2*width,height=width,bg="white")
speed = Meter(meters,width=width,height=height)
speed.draw(min_speed,max_speed,step_speed,"Speed","Chars/min")
speed.pack(side=LEFT)
errors = Meter(meters,width=width,height=width)
errors.draw(min_err,max_err,step_err,"Errors","%")
errors.pack()
meters.pack(anchor=S,fill=Y,expand=True)

# text zone
model = Text(root,width=80,height=20,wrap=WORD,font=font,padx=10,pady=10,relief=RIDGE)
model.tag_config('done',foreground="#303030",background="#D0D0D0")
model.tag_config('error',foreground="#FF0000",background="#FFFFFF")
model.tag_config('old_error',foreground="#FF0000",background="#D0D0D0")
model.bind('<Key>',type_key)
model.pack()

set_libs(default_lang)
root.mainloop()
