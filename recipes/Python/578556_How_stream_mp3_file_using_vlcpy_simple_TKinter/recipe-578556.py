#!/usr/bin/python

"""
author email: anton.vredegoor@gmail.com
last edit: June 9, 2013
license: GPL

this uses vlc.py to stream an mp3 file, 
for example to some addresses on a lan.

installing:
------------

-first create a file named "vlc2all.m3u" with the 
following content:

#EXTM3U
rtp://@:50004

-copy vlc2all.m3u to some computer

-modify this script to include the computer's ip address,
 it's in the 'destinations' tuple at the end of this script
 
running:
------------

-start the script:
>>> python vlc-stream.py some.mp3

-a tkinter window appears, click 'go' to start streaming

-listen to the stream by opening vlc2all.m3u on the 
receiving computer (of course open it with vlc!)

"""
from Tkinter import *
import vlc
import os
import sys

class App:
    
    def __init__(self,master,instream,destinations):
        self.master=master
        self.instream = instream
        self.destinations = destinations
        self.initialized,self.playing,self.changed,self.newpos = False,False,False,0
        self.initialize_player()
        self.master.bind("<Escape>", lambda _ : self.master.destroy())
        self.container=Frame()
        self.container.pack(fill=BOTH,expand=YES)
        self.slider = Scale(self.container, from_= 0, to=100, orient=HORIZONTAL,\
                command=lambda _: self.setpos())
        self.slider.pack(side=BOTTOM,fill=BOTH,expand=YES)
        self.urlbar = Text(self.container)
        self.urlbar.pack(side=LEFT,fill=BOTH,expand=YES)
        self.urlbar.delete(1.0,END)
        self.urlbar.insert(END, url)
        self.button1=Button(self.container, text='GO', command= self.playurl, width=80)
        self.button1.pack(side=RIGHT,fill=BOTH,expand=YES);

    def initialize_player(self):
        "initialize  a vlc player which plays locally and stream to the lan"
        self.inst = vlc.Instance()   
        self.p = self.inst.media_player_new() 
        cmd = [self.instream]
        s = "sout=#duplicate{"
        for ip,port in self.destinations:
            s+="dst=rtp{dst=%s,port=%s}," %(ip,port)
        s = s[:-1]
        s+="}"
        cmd.append(s)
        cmd.append("no-sout-rtp-sap")    
        cmd.append("no-sout-standard-sap")
        cmd.append("sout-keep")
        self.med=self.inst.media_new(*cmd)   
        self.med.get_mrl()    
        self.p.set_media(self.med)
        self.initialized = True
        
    def setpos(self):
        self.oldpos = self.newpos
        self.newpos = self.slider.get()
        #a bit of a hack, but this should prevent slider callbacks
        #not involving a mouse adjustment messing up the sound position
        if self.newpos-self.oldpos <> 1:
            self.changed = True
    
    def poll(self):
        #song ended?
        if self.p.get_state()==6:
            self.pauseurl()
            self.p.set_media(self.med)
        #slider adjusted?
        if self.changed:
            self.p.set_position(self.newpos/100.0)
            self.changed=False
        pos = self.p.get_position()
        self.slider.set(pos*100.0)
        self.master.after(100,self.poll)
    
    def pauseurl(self):
        if self.playing:
            self.p.set_pause(1)
            self.playing = False
            self.button1.configure(text = "GO",command = self.playurl)

    def playurl(self):
        if not self.playing:
            self.p.play()
            self.playing = True
        self.button1.configure(text = "PAUSE",command = self.pauseurl)
        self.poll()

if __name__=='__main__':
    if len(sys.argv)>1:
        fn = sys.argv[1]
    else:
        fn = "00000000.mp3"
    outport = 50004
    url = "file://"+os.path.abspath(fn)
    destinations = ("192.168.123.122",outport),("192.168.123.125",outport),\
        ("192.168.123.188",outport),("192.168.123.190",outport)
    root=Tk()
    root.geometry("680x80")
    root.title("vlc-stream")
    a = App(root,url,destinations)
    root.mainloop()






    
        
        
        
        
