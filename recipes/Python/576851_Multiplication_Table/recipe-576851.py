from Tkinter import *

class Application(Frame):
    """Multiplication Table"""
   
    def __init__(self,master):
        """initialize the frame"""
        Frame.__init__(self,master)
        self.grid()
        
        
        for i in range(12):
            val=i+1
            Label(self,text=val).grid(row=val,column=0)
            Label(self,text=val).grid(row=0,column=val)

        self.btns=[]
        for i in range(12):
            btns=[]
            for j in range(12):
                btns.append(self.create_widgets(i,j))
            self.btns.append(btns)
        
            

    def create_widgets(self,a,b):
        i=(a+1)*(b+1)
        bttn=Button(self,text="?",height=2,width=4)
        def button_action2(event,self=self,i=i):
            return self.button_action(event,i)
        bttn.bind("<ButtonRelease-1>",button_action2)
        bttn.grid(row=a+1,column=b+1)
 
           
    def button_action(self,ev,i):
        bttn=ev.widget
        bttn.configure(text=str(i),fg='red')
    
        

root=Tk()
root.title("Multiplication Table")
app=Application(root)


root.mainloop()
