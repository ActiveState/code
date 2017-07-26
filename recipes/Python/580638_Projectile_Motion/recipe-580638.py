from tkinter import *
import math

class Window(Frame):
    #Frame Defaults
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    def init_window(self):
        self.master.title("Projectile Motion")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self,width=1500,height=650)
        self.canvas.place(x=0,y=100)

        #Create Controls
        self.mbtnPlanet = Menubutton(self,text="Choose Planet",width=15)
        self.mbtnPlanet.grid(row=0,column=0)
        ##Menu
        self.mbtnPlanet.menu = Menu(self.mbtnPlanet)
        self.mbtnPlanet["menu"] = self.mbtnPlanet.menu
        self.mbtnPlanet.menu.add_checkbutton(label="Mercury",command=self.Mercury)
        self.mbtnPlanet.menu.add_checkbutton(label="Venus",command=self.Venus)
        self.mbtnPlanet.menu.add_checkbutton(label="Earth",command=self.Earth)
        self.mbtnPlanet.menu.add_checkbutton(label="Moon",command=self.Moon)
        self.mbtnPlanet.menu.add_checkbutton(label="Mars",command=self.Mars)
        self.mbtnPlanet.menu.add_checkbutton(label="Jupiter",command=self.Jupiter)
        self.mbtnPlanet.menu.add_checkbutton(label="Saturn",command=self.Saturn)
        self.mbtnPlanet.menu.add_checkbutton(label="Uranus",command=self.Uranus)
        self.mbtnPlanet.menu.add_checkbutton(label="Neptune",command=self.Neptune)
        self.mbtnPlanet.menu.add_checkbutton(label="Pluto",command=self.Pluto)
        ##Menu
        self.lbEnergy = Label(self,text="Speed (m/s)",width=10)
        self.lbEnergy.grid(row=0,column=1)
        self.lbAngle = Label(self,text="Angle",width=10)
        self.lbAngle.grid(row=0,column=2)
        self.lbSphere = Label(self,text="Speed (m/s)",width=10)
        self.lbSphere.grid(row=0,column=3)
        self.txtEnergy = Entry(self,width=10)
        self.txtEnergy.grid(row=1,column=1)
        self.txtAngle = Entry(self,width=10)
        self.txtAngle.grid(row=1,column=2)
        self.txtEggSpeed = Entry(self,width=10)
        self.txtEggSpeed.grid(row=1,column=3)
        self.btnMotion = Button(self,text="Show",command=self.Projectile_Motion,width=10)
        self.btnMotion.grid(row=2,column=1)
        self.btnClear = Button(self,text="Clear",command=self.Clear,width=10)
        self.btnClear.grid(row=2,column=2)
        self.btnSphere = Button(self,text="360 degree model",command=self.Sphere,width=12)
        self.btnSphere.grid(row=2,column=3)

        #Bind
        self.btnMotion.bind('<Button-1>',lambda e:self.Projectile_Motion)
        self.btnClear.bind('<Button-2>',lambda e:self.Clear)
        self.btnSphere.bind('<Button-3>',lambda e:self.Sphere)

    def Mercury(self):
        self.mbtnPlanet.config(text="Mercury")
        self.mbtnPlanet.config(fg="gray15")
    def Venus(self):
        self.mbtnPlanet.config(text="Venus")
        self.mbtnPlanet.config(fg="firebrick3")
    def Earth(self):
        self.mbtnPlanet.config(text="Earth")
        self.mbtnPlanet.config(fg="forestgreen")
    def Moon(self):
        self.mbtnPlanet.config(text="Moon")
        self.mbtnPlanet.config(fg="gray60")
    def Mars(self):
        self.mbtnPlanet.config(text="Mars")
        self.mbtnPlanet.config(fg="darkgoldenrod3")
    def Jupiter(self):
        self.mbtnPlanet.config(text="Jupiter")
        self.mbtnPlanet.config(fg="darkorange")
    def Saturn(self):
        self.mbtnPlanet.config(text="Saturn")
        self.mbtnPlanet.config(fg="darkgoldenrod2")
    def Uranus(self):
        self.mbtnPlanet.config(text="Uranus")
        self.mbtnPlanet.config(fg="darkturquoise")
    def Neptune(self):
        self.mbtnPlanet.config(text="Neptune")
        self.mbtnPlanet.config(fg="slateblue2")
    def Pluto(self):
        self.mbtnPlanet.config(text="Pluto")
        self.mbtnPlanet.config(fg="steelblue")

    #Assign Functions
    def Projectile_Motion(self):
        Speed = self.txtEnergy.get()
        Angle = self.txtAngle.get()
        Planet = self.mbtnPlanet.cget("text")
        Color = self.mbtnPlanet.cget("fg")
        if Planet == "Mercury":
            g = 3.7
        elif Planet == "Venus":
            g = 8.87
        elif Planet == "Earth":
            g = 9.807
        elif Planet == "Moon":
            g = 1.622
        elif Planet == "Mars":
            g = 3.711
        elif Planet == "Jupiter":
            g = 24.79
        elif Planet == "Saturn":
            g = 10.44
        elif Planet == "Uranus":
            g = 8.69
        elif Planet == "Neptune":
            g = 11.15
        elif Planet == "Pluto":
            g = 0.658
        if Planet == "Choose Planet":
            print("Choose A Planet")
        else:
            Vx = float(Speed) * math.cos(math.radians(float(Angle)))
            Vy = float(Speed) * math.sin(math.radians(float(Angle)))
            if Vy > 0:
                Time = (2*Vy)/g
                Range = Vx*Time
                MaxHeight = Vy*(Time/2) - 0.5*g*(Time/2)**2
            else:
                Time = 0
                Range = 0
                MaxHeight = 0
            print(Planet+":")
            print("Velocity:",str(Speed)+"m/s,",str(Angle),"degrees")
            print("X motion:",str(round(Vx,2))+"m/s")
            print("Y motion:",str(round(Vy,2))+"m/s")
            print("Air Time:",str(round(Time,2))+"s")
            print("Range:",str(round(Range,2))+"m")
            print("Max Height:",str(round(MaxHeight,2))+"m"+'\n')
            self.canvas.create_line(0,550,1500,550)
            for t in range(1,101):
                self.canvas.create_line((Vx*(t-1))+750,-1*(Vy*(t-1)+(-0.5*g*(t-1)**2))+550,(Vx*t)+750,-1*(Vy*t+(-0.5*g*t**2))+550,fill=Color,dash=(5,5))

    def Sphere(self):
        Speed = self.txtEggSpeed.get()
        Planet = self.mbtnPlanet.cget("text")
        Color = self.mbtnPlanet.cget("fg")
        if Planet == "Mercury":
            g = 3.7
        elif Planet == "Venus":
            g = 8.87
        elif Planet == "Earth":
            g = 9.807
        elif Planet == "Moon":
            g = 1.622
        elif Planet == "Mars":
            g = 3.711
        elif Planet == "Jupiter":
            g = 24.79
        elif Planet == "Saturn":
            g = 10.44
        elif Planet == "Uranus":
            g = 8.69
        elif Planet == "Neptune":
            g = 11.15
        elif Planet == "Pluto":
            g = 0.658
        if Planet == "Choose Planet":
            print("Choose A Planet")
        else:
            for Angle in range(0,361):
                Vx = float(Speed) * math.cos(math.radians(float(Angle)))
                Vy = float(Speed) * math.sin(math.radians(float(Angle)))
                for t in range(1,101):
                    self.canvas.create_line((Vx*(t-1))+750,-1*(Vy*(t-1)+(-0.5*g*(t-1)**2))+550,(Vx*t)+750,-1*(Vy*t+(-0.5*g*t**2))+550,fill=Color,dash=(5,5))
                
    def Clear(self):
        self.canvas.delete("all")
        
#Window Defaults
root = Tk()
root.geometry("1500x750")
app = Window(root)
root.mainloop()
