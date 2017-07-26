# imageviewer.py
#requires python 2.x

from wax import *
import base64
import cStringIO
import os
import sys
 
class MainFrame(VerticalFrame):
        
    def Body(self):
        self.SetTitle("Image Viewer")
        whereami = os.path.abspath(os.path.dirname(__file__))
        os.chdir(whereami)
        wildcard="GIF images|*.gif|JPG images|*.jpg|JPEG images|*.jpeg|PNG images|*.png"
        dlg = FileDialog(self, title="Select Image file to display", 
                wildcard=wildcard, open=1, multiple=0)
        if dlg.ShowModal() == 'ok':
            filename = dlg.GetPath()
        else:
            raise SystemExit
        dlg.Destroy()
        label1 = Label(self, "Image as image...")
        self.AddComponent(label1, expand='h', border=5)
        label1.BackgroundColor = self.BackgroundColor = 'white'
        bitmap = Image(filename).ConvertToBitmap()
        self.AddComponent(Bitmap(self, bitmap))


        label2 = Label(self, "Image encoded as text...")
        self.AddComponent(label2, expand='h', border=5)
        label2.BackgroundColor = self.BackgroundColor = 'white'
        imageEncodeText = base64.encodestring(open(filename, "rb").read()) 
        imageText = TextBox(self, multiline=1, readonly=1,
                       Font=Font("Courier New", 8), Size=(650,200),
                       Value=imageEncodeText)
        self.AddComponent(imageText, expand='both')

        label2 = Label(self, "Text decoded back to image...")
        self.AddComponent(label2, expand='h', border=5)
        label2.BackgroundColor = self.BackgroundColor = 'white'
        data = base64.decodestring(imageEncodeText)
        path,fid = os.path.split(filename)
        head,tail = os.path.split(fid)
        fileout = "%s%sout%s" % (path,head,tail)
        f1 = open(fileout,'wb+')
        f1.write(data)
        f1.close()
        bitmap2 = Image(fileout).ConvertToBitmap()
        self.AddComponent(Bitmap(self, bitmap2))

        self.Pack()

app = Application(MainFrame)
app.MainLoop()
