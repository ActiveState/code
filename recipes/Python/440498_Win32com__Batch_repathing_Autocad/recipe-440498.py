# Relative-refs.pyw
"""A short python script for repathing xrefs in Autocad."""

import win32com.client,os, os.path, tkFileDialog
from Tkinter import *
from tkMessageBox import askokcancel
from time import sleep

# Get a COM object for Autocad
acad = win32com.client.Dispatch("AutoCAD.Application")

def repath(filename):
    print 'Repathing %s...' %filename
    doc = acad.Documents.Open(filename)
    
    blocks = doc.Database.Blocks # Internally xrefs are just blocks!
    xrefs = [item for item in blocks if item.IsXRef]
    
    if xrefs:
        for xref in xrefs:
            old_path = xref.Path
            new_path = os.path.join('..\\x-ref\\',os.path.basename(old_path))
            xref.Path = new_path
            print 'Old path name was %s, new path name is %s.\n' %(old_path, new_path)
    try:
        doc.Close(True) # Close and save
    except: # Something when wrong,
        doc.Close(False) # close then report it
        raise
    
class Logger:
    """A filelike object that prints its input on the screen."""
    
    def __init__(self, logfile=None):
        """Takes one argument, a file like object for logging."""
        print 'Starting logger...'
        if not logfile:
            self.logfile = open('relative-refs.log','w')
        else:
            self.logfile = logfile
        sys.stderr = self                 # Super cheap logging facility...
        sys.stdout = self                 # Just redirect output to a file.
        print 'Logger running...'
    
    def write(self, line):
        sys.__stdout__.write(line)
        self.logfile.write(line)
    
    def close(self):
        """The close method restores stdout and stderr to normal."""
        self.logfile.close()
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__

class Tktextfile:
    """A file like interface to the Tk text widget."""
    
    def __init__(self, root):
        """Create a scrollable text widget to be written to."""
        self.root = root
        self.text = Text(root,width=40,height=20)
        self.text.pack(side=LEFT, expand=True, fill=BOTH)
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.text.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        self.text.focus()
    
    def write(self, line):
        """Write method for file like widget."""
        self.text.insert(INSERT, line)
        self.text.see(END)
    
    def close(self):
        """Fake close method."""
        pass

if __name__ == '__main__':
    if acad.Visible:
        acad.Visible = False
    root = Tk()
    text = Tktextfile(root)
    logger = Logger(text)
    dir = tkFileDialog.askdirectory()

    answer = askokcancel('RePath','Re path all dwg files in ' + dir + '?')
    
    if answer:
        for dirpath, subdirs, files in os.walk(dir):
            for name in files:
                ext = name.split('.')[-1] or ''
                # We want dwg files which are not in the x-ref directory
                if ext.lower() == 'dwg' and 'x-ref' not in dirpath.lower():
                    drawing = os.path.join(dirpath, name)
                    try:
                        repath(drawing)
                    except:
                        print 'Unable to repath drawing %s!' %drawing
                root.update()
    acad.Visible = True
