# ======== Select a directory:

import Tkinter, tkFileDialog

root = Tkinter.Tk()
dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
if len(dirname ) > 0:
    print "You chose %s" % dirname 


# ======== Select a file for opening:
import Tkinter,tkFileDialog

root = Tkinter.Tk()
file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file')
if file != None:
    data = file.read()
    file.close()
    print "I got %d bytes from this file." % len(data)


# ======== "Save as" dialog:
import Tkinter,tkFileDialog

myFormats = [
    ('Windows Bitmap','*.bmp'),
    ('Portable Network Graphics','*.png'),
    ('JPEG / JFIF','*.jpg'),
    ('CompuServer GIF','*.gif'),
    ]

root = Tkinter.Tk()
fileName = tkFileDialog.asksaveasfilename(parent=root,filetypes=myFormats ,title="Save the image as...")
if len(fileName ) > 0:
    print "Now saving under %s" % nomFichier
