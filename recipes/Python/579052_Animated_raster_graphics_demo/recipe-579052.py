#rotozoom graphics raster demo Tkinter
#by Antoni Gual 

import tkinter
from math import sin,cos
from random  import randint
x,y=320,200 
  
class App:
    def __init__(self, t):
       self.img = tkinter.PhotoImage(width=x,height=y) 
       self.c = tkinter.Label(t,image=self.img);self.c.pack()
       t.after_idle(self.do_rotozoom)
       self.ang=0
       
    def do_rotozoom(self):
       self.ang=(self.ang+1)%100
       cs1=cs[self.ang]
       ss1=ss[self.ang]
       self.img.put((" ".join((("{"+" ".join(clr[((i*cs1-j*ss1) & (j*cs1+i*ss1))//256] 
          for i in range(-160,159)))+"}" for j in range(-100,99)))))
       t.after(20,self.do_rotozoom)     

#precalculate trig
cs,ss,ang=[],[],0
for i in range(100):
    aa=abs(sin(ang))*255
    cs.append(int(cos(ang)*aa))
    ss.append(int(sin(ang)*aa))
    ang+=0.062832
#precalculate a b/w color table   
clr=[]
for i in range(256):
    clr.append( "#{:06x}".format(i*0x10101))
    
t=tkinter.Tk()
a = App(t )
t.mainloop()
