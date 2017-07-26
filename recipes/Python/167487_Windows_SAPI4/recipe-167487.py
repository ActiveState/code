from Tkinter import *
import win32com.client
import pythoncom
from win32com.client import *
import time
from random import *

defaultNamedOptArg=pythoncom.Missing
defaultNamedNotOptArg=pythoncom.Missing
defaultUnnamedArg=pythoncom.Missing

gencache.EnsureModule('{EEE78583-FE22-11D0-8BEF-0060081841DE}', 0, 1, 0)

class Sapi4:

    voice_list = []

    def __init__(self):
        #init
        self.SpeedPercent=StringVar()
        self.PitchPercent=StringVar()
        self.VolumeLeftPercent=StringVar()
        self.VolumeRightPercent=StringVar()
        
        try:
            self.directss = win32com.client.DispatchWithEvents("{EEE78591-FE22-11D0-8BEF-0060081841DE}", Sapi4Events)
            voice_no = self.directss.Find(0)
            print 'Woohoo: have found engine'  
            self.voice = self.directss.Select(voice_no)			
            voice_name = self.directss.ModeName(voice_no)
            self.sapi_compliant = 1
            if len(self.voice_list) < 1:
                self.getVoiceList()
            self.selectVoice(voice_name)
        except:			
            print 'Bugger: unable to initialise speech!'
            #self.quit()
        return None

    def selectVoice(self, voice_name=''):
        #select voice
        voice_index = 0
        voice_no = 0
        found = 0
        for voice_compare in self.voice_list:
            voice_no = voice_no + 1						
            if voice_compare == voice_name:
                found = 1
                break	
        if found == 0:
            voice_no = 1
        self.directss.AudioReset() 		
        
        try:
            self.directss.Select(voice_no)		
            self.sapi_compliant = 1
        except:	
            self.sapi_compliant = 0
        self.directss.Speak(' ')	#don't understand why we need this here but voice doesn't change otherwise          
        self.voice_no = voice_no
        self.voice_index = voice_no - 1
        self.voice_name = self.directss.ModeName(voice_no)	
        #print 'Selected voice: ' + self.voice_name      
        
        self.MinSpeed = self.directss.MinSpeed
        self.MaxSpeed = self.directss.MaxSpeed
        self.Speed = self.directss.Speed	
        #print 'Speed: from ' + str(self.MinSpeed) + ' to ' + str(self.MaxSpeed) + ' - current ' + str(self.Speed) 
                
        self.MinPitch = self.directss.MinPitch
        self.MaxPitch = self.directss.MaxPitch
        self.Pitch = self.directss.Pitch
        #print 'Pitch: from ' + str(self.MinPitch) + ' to ' + str(self.MaxPitch) + ' - current ' + str(self.Pitch)

        self.MinVolumeLeft = self.directss.MinVolumeLeft
        self.MaxVolumeLeft = self.directss.MaxVolumeLeft
        self.VolumeLeft = self.directss.VolumeLeft
        #print 'VolumeLeft: from ' + str(self.MinVolumeLeft) + ' to ' + str(self.MaxVolumeLeft) + ' - current ' + str(self.VolumeLeft)
        
        self.MinVolumeRight = self.directss.MinVolumeRight
        self.MaxVolumeRight = self.directss.MaxVolumeRight	
        self.VolumeRight = self.directss.VolumeRight
        #print 'VolumeRight: from ' + str(self.MinVolumeRight) + ' to ' + str(self.MaxVolumeRight) + ' - current ' + str(self.VolumeRight)
        #print 
        
        return voice_no

    def getVoiceList(self):
        #fill list of avaliable voices
        voice_count = self.directss.CountEngines
        voice_no = 1
        self.voice_list=[]
        while voice_no < voice_count + 1:
            voice_name = self.directss.ModeName(voice_no)
            #print 'adding voice' + voice_name
            self.voice_list.append(voice_name)
            voice_no = voice_no + 1	
        return None

    def setSpeed(self, speed):
        #set voice speed
        self.directss.Speed = int(speed)
        speed_percent = str(((self.directss.Speed - self.directss.MinSpeed)*100)  / (self.directss.MaxSpeed-self.directss.MinSpeed)) + '%'
        self.SpeedPercent.set(speed_percent) 	
        return None  
    
    def setPitch(self, pitch):
        #set voice pitch
        self.directss.Pitch = int(pitch)
        pitch_percent = str(((self.directss.Pitch - self.directss.MinPitch)*100)  / (self.directss.MaxPitch-self.directss.MinPitch)) + '%'
        self.PitchPercent.set(pitch_percent)
        return None

    def setVolumeLeft(self, volume):
        #set voice volume left
        self.directss.VolumeLeft = int(volume)
        volume_percent = str(((self.directss.VolumeLeft - self.directss.MinVolumeLeft)*100)  / \
        (self.directss.MaxVolumeLeft-self.directss.MinVolumeLeft)) + '%'
        self.VolumeLeftPercent.set(volume_percent)
        self.setVolumeRight(volume) #change right volume to match left
        return None        

    def setVolumeRight(self, volume):
        #set voice volume right - this seems to have no effect - left volume appears to 
        #control both left and right channels for the engines tested with
        self.directss.VolumeRight = int(volume)
        volume_percent = str(((self.directss.VolumeRight - self.directss.MinVolumeRight)*100)  / \
        (self.directss.MaxVolumeRight-self.directss.MinVolumeRight)) + '%'
        self.VolumeRightPercent.set(volume_percent)
        return None 
        
class Sapi4Events:

    def OnAudioStart(self, hi=defaultNamedNotOptArg, lo=defaultNamedNotOptArg):
        # method AudioStart
        global gwordpositionjumpto		
        global gspeaking
        global gwords
        global gwordposition
        global gcharposition     	
        global ghide	
        global gpaused            
        gspeaking = int(1)        
        if gpaused == 0:   
            gwordposition = int(0)                        
            gcharposition = int(0)            
            ghide = 1
        if gwordpositionjumpto > 0:
            wordposition = 0
            while wordposition < (gwordpositionjumpto -1):
                gcharposition = gcharposition + len(gwords[wordposition]) + 1
                wordposition = wordposition + 1
            gwordposition = gwordpositionjumpto
            gwordpositionjumpto = 0
    
    def OnWordPosition(self, hi=defaultNamedNotOptArg, lo=defaultNamedNotOptArg, byteoffset=defaultNamedNotOptArg):
        # method WordPosition
        global gwords
        global gwordposition
        global gcharposition
        gwordposition = gwordposition + 1
        word = gwords[gwordposition-1]
        #print word + ' ' + str(gwordposition) 
        gcharposition = gcharposition + len(word) + 1

    def OnAudioStop(self, hi=defaultNamedNotOptArg, lo=defaultNamedNotOptArg):
        #method AudioStop
        global gspeaking
        gspeaking = int(0)


class ExampleSapi:
    def __init__(self, dialog):

        self.dialog = dialog
        dialog.title("Voice Settings")		
        self.sapi = Sapi4()
        self.frame_dialog = Frame(dialog, height=500)
        self.frame_dialog.pack(side=TOP, expand=NO, fill=BOTH)
        
        #buttons
        frame_button = Frame(dialog)
        frame_button.pack(side=BOTTOM, expand=NO, fill=X)
        button = Button(frame_button, text='Close', command=dialog.destroy, width=10, foreground='DarkRed')
        button.pack(side=RIGHT, padx=2, pady=2)			
        button = Button(frame_button, text='Test', command=self.test, width=10, foreground='DarkBlue')
        button.pack(side=RIGHT, padx=2, pady=2)
                
        frame_left = Frame(self.frame_dialog)
        frame_left.pack(side=TOP, expand=YES, fill=BOTH)
        
        scrollbar = Scrollbar(frame_left, orient=VERTICAL)
        self.listbox = Listbox(frame_left, yscrollcommand=scrollbar.set, exportselection=0, font="Arial 10")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        for item in self.sapi.voice_list:
            self.listbox.insert(END, item)
        self.listbox.pack(side=LEFT, padx=2, pady=2, expand=YES, fill=BOTH)
        self.listbox.select_set(self.sapi.voice_index)
        self.listbox.see(self.sapi.voice_index)
        
        #settings frame
        frame_right = Frame(self.frame_dialog)
        frame_right.pack(side=TOP, expand=NO, fill=BOTH)
        
        #speed
        self.label_speed = Label(frame_right, text=" Speed:", font="Arial 10") 
        self.label_speed.grid(row=0, col=0, sticky=E, padx=2, pady=1) 
        self.scale_speed = Scale(frame_right, length=300, orient='horizontal', command=self.sapi.setSpeed, showvalue=0)
        self.scale_speed.grid(row=0, column=1, sticky=W, padx=2, pady=1)  		
        self.label_speed_percent = Label(frame_right, textvariable=self.sapi.SpeedPercent, width=5)
        self.label_speed_percent.grid(row=0, column=2, sticky=W, padx=2, pady=1)

        #pitch
        self.label_pitch = Label(frame_right, text=" Pitch:", font="Arial 10") 
        self.label_pitch.grid(row=1, column=0, sticky=E, padx=2, pady=1) 
        self.scale_pitch = Scale(frame_right, length=300, orient='horizontal', command=self.sapi.setPitch, showvalue=0)
        self.scale_pitch.grid(row=1, column=1, sticky=W, padx=2, pady=1)  		
        self.label_pitch_percent = Label(frame_right, textvariable=self.sapi.PitchPercent, width=5)
        self.label_pitch_percent.grid(row=1, column=2, sticky=W, padx=2, pady=1)

        #volume left
        self.label_volume_left = Label(frame_right, text=" Volume:", font="Arial 10") 
        self.label_volume_left.grid(row=2, column=0, sticky=E, padx=2, pady=1) 
        self.scale_volume_left = Scale(frame_right, length=300, orient='horizontal', command=self.sapi.setVolumeLeft, showvalue=0)
        self.scale_volume_left.grid(row=2, column=1, sticky=W, padx=2, pady=1)  		
        self.label_volume_left_percent = Label(frame_right, textvariable=self.sapi.VolumeLeftPercent, width=5)
        self.label_volume_left_percent.grid(row=2, column=2, sticky=W, padx=2, pady=1)

        #volume right - does not appear to work
#        label = Label(frame_right, text=" Volume Right:", font="Arial 10") 
#        label.grid(row=3, col=0, sticky=E, padx=2, pady=1) 
#        self.scale_volume_right = Scale(frame_right, length=200, orient='horizontal', command=self.sapi.setVolumeRight, showvalue=0)
#        self.scale_volume_right.grid(row=3, column=1, sticky=W, padx=2, pady=1)  		
#        label = Label(frame_right, textvariable=self.sapi.VolumeRightPercent, width=5)
#        label.grid(row=3, column=2, sticky=W, padx=2, pady=1)

        #test text
        self.test_text = StringVar()
        self.test_text.set('This is a test. This is a test. This is a test.')
        label = Label(frame_right, text=" Test Text:", font="Arial 10")
        label.grid(row=3, column=0, sticky=E, padx=2, pady=1) 
        text = Entry(frame_right, textvariable = self.test_text, font="Arial 10", width=50, exportselection=0)
        text.grid(row=3, column=1, columnspan=2, sticky=W, padx=2, pady=1) 
		
        #canvas
        self.canvas = Canvas(self.frame_dialog, height=120)
        self.canvas.pack(expand=NO, fill=BOTH)
        self.drawFace()
        
        self.canvas.after(1000, self.drawFaceBlink)
        self.listbox.after(500, self.poll)
        self.setVoice(self.listbox.get(self.listbox.curselection()[0]))
        self.centerMe()
        return None
    
    def setVoice(self, voice_name):
        #select voice            
        voice_no = self.sapi.selectVoice(voice_name)		
        self.scale_speed.configure(from_=self.sapi.directss.MinSpeed, to=self.sapi.directss.MaxSpeed)          
        self.scale_pitch.configure(from_=self.sapi.directss.MinPitch, to=self.sapi.directss.MaxPitch)             
        self.scale_volume_left.configure(from_=self.sapi.directss.MinVolumeLeft, to=self.sapi.directss.MaxVolumeLeft)          		
        #self.scale_volume_right.configure(from_=self.sapi.directss.MinVolumeRight, to=self.sapi.directss.MaxVolumeRight)
        #self.scale_volume_right.set(self.sapi.VolumeRight)
        #viavoice8 min max volumes are back to front - so hide volume scale
        #viavoice8 also change thier min speed and pitch values to the current values - so hide them too i guess
       
        self.scale_speed.set(self.sapi.directss.Speed)      
        self.scale_pitch.set(self.sapi.directss.Pitch)
        self.scale_volume_left.set(self.sapi.directss.VolumeLeft)
        
        if (self.sapi.directss.MinVolumeLeft > self.sapi.directss.MaxVolumeLeft) or self.sapi.sapi_compliant==0:
            self.label_speed.grid_forget()
            self.scale_speed.grid_forget()
            self.label_speed_percent.grid_forget()
            self.label_pitch.grid_forget()
            self.scale_pitch.grid_forget()
            self.label_pitch_percent.grid_forget()
            self.label_volume_left.grid_forget()
            self.scale_volume_left.grid_forget()
            self.label_volume_left_percent.grid_forget()
            self.canvas.forget()			
        else:
            self.label_speed.grid(row=0, col=0, sticky=E, padx=2, pady=1)
            self.scale_speed.grid(row=0, column=1, sticky=W, padx=2, pady=1)  
            self.label_speed_percent.grid(row=0, column=2, sticky=W, padx=2, pady=1)
            self.label_pitch.grid(row=1, col=0, sticky=E, padx=2, pady=1) 
            self.scale_pitch.grid(row=1, column=1, sticky=W, padx=2, pady=1)  
            self.label_pitch_percent.grid(row=1, column=2, sticky=W, padx=2, pady=1)
            self.label_volume_left.grid(row=2, col=0, sticky=E, padx=2, pady=1)
            self.scale_volume_left.grid(row=2, column=1, sticky=W, padx=2, pady=1)  
            self.label_volume_left_percent.grid(row=2, column=2, sticky=W, padx=2, pady=1)			
            self.canvas.pack()

        speak_text = 'You have selected the voice of ' + voice_name + '.'
        self.sapi.directss.Speak(speak_text) 
        return None

       
    def poll(self):
        new_voice_name = self.listbox.get(self.listbox.curselection()[0])
        if new_voice_name != self.sapi.voice_name:
            self.setVoice(new_voice_name)
        self.drawFaceMouthTalk()
        self.listbox.after(90, self.poll)
        return None

    def test(self):
        #test
        self.sapi.directss.AudioReset()
        if len(self.test_text.get()) < 1:
            self.test_text = 'This is a test. This is a test. This is a test.'
        self.sapi.directss.Speak(self.test_text.get())	
        return None

    def drawFace(self):
        #draw face
        self.face = self.canvas.create_oval(140, 10, 240, 110, tag='face', fill='yellow', width=3)
        self.eyeL = self.canvas.create_oval(170, 40, 180, 60, tag='eye', fill='black')	
        self.eyeR = self.canvas.create_oval(200, 40, 210, 60, tag='eye', fill='black')	
        self.mouthClosed = self.canvas.create_polygon(150, 60, 190, 100, 230, 60, 190, 100,  
            smooth=1, width=3, outline='Black', fill='Red')	
        #hidden at startup 					
        self.mouthOpen1 = self.canvas.create_polygon(150, 60, 170, 75, 190, 90, 210, 75, 230, 60, 190, 90,  
            splinesteps=20, smooth=1, width=3, outline='Black', fill='Red')	
        self.mouthOpen2 = self.canvas.create_polygon(150, 60, 160, 75, 190, 95, 220, 75, 230, 60, 190, 90,  
            splinesteps=20, smooth=1, width=3, outline='Black', fill='Red')					
        self.mouthOpen3 = self.canvas.create_polygon(150, 60, 170, 75, 190, 95, 210, 75, 230, 60, 190, 90,  
            splinesteps=20, smooth=1, width=3, outline='Black', fill='Red')		
        self.mouthOpen4 = self.canvas.create_polygon(150, 60, 160, 80, 190, 100, 220, 80, 230, 60, 190, 90,  
            splinesteps=20, smooth=1, width=3, outline='Black', fill='Red')					
        self.canvas.lower(self.mouthOpen1)		    
        self.canvas.lower(self.mouthOpen2)		
        self.canvas.lower(self.mouthOpen3)				
        self.canvas.lower(self.mouthOpen4)				
        self.blinkL = self.canvas.create_oval(165, 49, 185, 51, tag='eye', fill='black')
        self.blinkR = self.canvas.create_oval(195, 49, 215, 51, tag='eye', fill='black')		
        self.canvas.lower(self.blinkL)		
        self.canvas.lower(self.blinkR)                        
        return None

    def drawFaceMouthTalk(self):
        #open mouth
        global gspeaking
        if gspeaking == 0:
            self.canvas.lift(self.mouthClosed)
            self.canvas.lower(self.mouthOpen1)		    
            self.canvas.lower(self.mouthOpen2)
            self.canvas.lower(self.mouthOpen3)			
            self.canvas.lower(self.mouthOpen4)					
            return None
        mouthdisplay = randrange(1,5) 
        self.canvas.lower(self.mouthClosed)		    		
        self.canvas.lower(self.mouthOpen1)		    
        self.canvas.lower(self.mouthOpen2)
        self.canvas.lower(self.mouthOpen3)		
        self.canvas.lower(self.mouthOpen4)							
        if mouthdisplay == 1:
            self.canvas.lift(self.mouthOpen1)            
        if mouthdisplay == 2:
            self.canvas.lift(self.mouthOpen2)              
        if mouthdisplay == 3:
            self.canvas.lift(self.mouthOpen3)   
        if mouthdisplay == 4:
            self.canvas.lift(self.mouthOpen4) 			          
        return None
        
    def drawFaceBlink(self):
        #blink
        self.canvas.lift(self.blinkL)
        self.canvas.lift(self.blinkR)
        self.canvas.lower(self.eyeL)
        self.canvas.lower(self.eyeR)		
        self.canvas.after(200, self.drawFaceUnblink)
        return None

    def drawFaceUnblink(self):
        self.canvas.lift(self.eyeL)
        self.canvas.lift(self.eyeR)	
        self.canvas.lower(self.blinkL)
        self.canvas.lower(self.blinkR)		
        blinkat = randrange(1,10) * 1000
        self.canvas.after(blinkat, self.drawFaceBlink)		
        return None
        
    def centerMe(self):
        #center
        top = self.dialog
        top.update()
        sw = top.winfo_screenwidth()
        sh = top.winfo_screenheight()
        w = top.winfo_width()
        h = 470#top.winfo_height()
        x = (sw - w)/2
        y = (sh - h)/2
        geom = '%dx%d+%d+%d' % (w, h, x, y)
        top.geometry(geom)		
        return None
        
        
if __name__ == "__main__":
    root = Tk()
    Test = ExampleSapi(root)   
    root.mainloop()
