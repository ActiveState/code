# Author: Miguel Martinez Lopez
#
# Uncomment the next line to see my email
# print("Author's email: %s"%"61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex"))
#
#
# PIL is more efficient manipulating directly pixels than PhotoImage. See this discussion:
#    https://groups.google.com/forum/#!topic/comp.lang.python/nQ6YO-dTz10
#
# To install PIL on windows for Python 3, read this:
#     http://stackoverflow.com/questions/7407185/pil-for-python-3-2-on-windows-or-alternatives
#
# To install ImageTk for Python 2.7 on ubuntu do:
#    sudo apt-get install python-imaging-tk
# and for Python 3:
#    sudo apt-get install python3-pil.imagetk
#
try:
    from Tkinter import Canvas
    from Tkconstants import *
except ImportError:
    from tkinter import Canvas
    from tkinter.constants import *

from PIL import Image, ImageDraw, ImageTk

# Python 2/3 compatibility
try:
  basestring
except NameError:
  basestring = str

def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))

class GradientFrame(Canvas):

    def __init__(self, master, from_color, to_color, width=None, height=None, orient=HORIZONTAL, steps=None, **kwargs):
        Canvas.__init__(self, master, **kwargs)
        if steps is None:
            if orient == HORIZONTAL:
                steps = height
            else:
                steps = width

        if isinstance(from_color, basestring):
            from_color = hex2rgb(from_color)
            
        if isinstance(to_color, basestring):
            to_color = hex2rgb(to_color)

        r,g,b = from_color
        dr = float(to_color[0] - r)/steps
        dg = float(to_color[1] - g)/steps
        db = float(to_color[2] - b)/steps

        if orient == HORIZONTAL:
            if height is None:
                raise ValueError("height can not be None")
            
            self.configure(height=height)
            
            if width is not None:
                self.configure(width=width)

            img_height = height
            img_width = self.winfo_screenwidth()

            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                y0 = int(float(img_height * i)/steps)
                y1 = int(float(img_height * (i+1))/steps)

                draw.rectangle((0, y0, img_width, y1), fill=(int(r),int(g),int(b)))
        else:
            if width is None:
                raise ValueError("width can not be None")
            self.configure(width=width)
            
            if height is not None:
                self.configure(height=height)

            img_height = self.winfo_screenheight()
            img_width = width
            
            image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
            draw = ImageDraw.Draw(image)

            for i in range(steps):
                r,g,b = r+dr, g+dg, b+db
                x0 = int(float(img_width * i)/steps)
                x1 = int(float(img_width * (i+1))/steps)

                draw.rectangle((x0, 0, x1, img_height), fill=(int(r),int(g),int(b)))
        
        self._gradient_photoimage = ImageTk.PhotoImage(image)

        self.create_image(0, 0, anchor=NW, image=self._gradient_photoimage)

if __name__ == "__main__":
    try:
        from Tkinter import Tk, Label
    except ImportError:
        from tkinter import Tk, Label

    root = Tk()

    Label(root, text="Gradient 1:").pack(anchor=W)
    GradientFrame(root, from_color="#000000", to_color="#E74C3C", height=100).pack(fill=X)
    
    Label(root, text="Gradient 2 (GTK gradient):").pack(anchor=W, pady=(20,0))
    GradientFrame(root, from_color="#FCFCFC", to_color="#E2E2E2", height=30).pack(fill=X, pady=(0,10))
     

    root.mainloop()
