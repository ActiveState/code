## {{{ http://code.activestate.com/recipes/180801/ (r4)
#!/usr/bin/env python

"""Program for converting image files' format. Converts one file at a time or all
files (of a selected format) in a directory at once.
Converted files have same basename as original files.
-- Added: recursive mode will manage files in subfolders too
-- Added: possible to delete original files
-- REQUIRES http://code.activestate.com/recipes/577230/

Uses workaround: askdirectory() does not allow choosing
a new dir, so asksaveasfilename() is used instead, and
the filename is discarded, keeping just the directory.
-- hence you need create an empty image in recursive mode in order to select a root folder not containing images !
"""

import filePattern # this file should contain http://code.activestate.com/recipes/577230/ 

import os, os.path, string, sys
from Tkinter import *
from tkFileDialog import *
#import Image
from PIL import Image
openfile = '' # full pathname: dir(abs) + root + ext
indir = ''
outdir = ''
def getinfilename():
    global openfile, indir
    ftypes=(('Bitmap Images', '*.bmp'),
            ('Jpeg Images', '*.jpg'),
            ('Png Images', '*.png'),
            ('Tiff Images', '*.tif'),
            ('Gif Images', '*.gif'),
            ("All files", "*"))
    if indir:
        openfile = askopenfilename(initialdir=indir,
                                   filetypes=ftypes)
    else:
        openfile = askopenfilename(filetypes=ftypes)
    if openfile:
        indir = os.path.dirname(openfile)

def getoutdirname():
    global indir, outdir
    if openfile:
        indir = os.path.dirname(openfile)
        outfile = asksaveasfilename(initialdir=indir,
                                    initialfile='foo')
    else:
        outfile = asksaveasfilename(initialfile='foo')
    outdir = os.path.dirname(outfile)

def save(infile, outfile):
    # should maybe treat transparency apart for some image format ?
    if infile != outfile:
        try:
            Image.open(infile).save(outfile)
            return True
        except IOError:
            print "Cannot convert", infile
    return False

def selector():    
    path, file = os.path.split(openfile)
    base, ext = os.path.splitext(file)
    if varRec.get():
        G= filePattern._paths_from_path_patterns([indir], includes=["*%s"%ext])
        l=[g for g in G]
        return l
    else:        
        if var.get():
            ls = os.listdir(indir)
            filelist = []
            for f in ls:
                if os.path.splitext(f)[1] == ext:
                    filelist.append(f)
        else:
            filelist = [file]
        return filelist
def convert():
    newext = frmt.get()
    filelist= selector()
    should_delete= varDel.get()
    done= "Done. Deleted" if should_delete else "Done. Created" 
    for f in filelist:
        infile = os.path.join(indir, f)
        ofile = os.path.join(outdir, f)
        outfile = os.path.splitext(ofile)[0] + newext
        succeed= save(infile, outfile)    
        if should_delete and succeed:     
            os.remove(infile)        
    done= "%s=%s" % (done,len(filelist))
    win = Toplevel(root)
    Button(win, text=done, command=win.destroy).pack()

def ________________gui_________________():pass
# Divide GUI into 3 frames: top, mid, bot
root = Tk()
topframe = Frame(root,
                 borderwidth=2,
                 relief=GROOVE)
topframe.pack(padx=2, pady=2)

midframe = Frame(root,
                 borderwidth=2,
                 relief=GROOVE)
midframe.pack(padx=2, pady=2)

botframe = Frame(root)
botframe.pack()

Button(topframe,
       text='Select image to convert',
       command=getinfilename).pack(side=TOP, pady=4)

multitext = """Convert all image files
(of this format) in this folder?"""
var = IntVar()
chk = Checkbutton(topframe,
                  text=multitext,
                  variable=var).pack(pady=2)
mt= """recursive"""
varRec = IntVar()
chkRec = Checkbutton(topframe,
                  text=mt,
                  variable=varRec).pack(pady=6)
mt2= """Delete original"""
varDel = IntVar()
chkDel = Checkbutton(topframe,
                  text=mt2,
                  variable=varDel).pack(pady=8)
                  
Button(topframe,
       text='Select save location',
       command=getoutdirname).pack(side=BOTTOM, pady=4)


Label(midframe, text="New Format:").pack(side=LEFT)
frmt = StringVar()
formats = ['.bmp', '.gif', '.jpg', '.png', '.tif']
for item in formats:
    Radiobutton(midframe,
                text=item,
                variable=frmt,
                value=item).pack(anchor=NW)

Button(botframe, text='Convert', command=convert).pack(side=LEFT,
                                                       padx=5,
                                                       pady=5)
Button(botframe, text='Quit', command=root.quit).pack(side=RIGHT,
                                                      padx=5,
                                                      pady=5)

root.title('Image Converter')
root.mainloop()
