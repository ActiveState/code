import aens_time
import Tkinter

def main():
    root = Tkinter.Tk()
    root.resizable(False, False)
    root.title('Aens Time')
    string = Tkinter.StringVar()
    Tkinter.Label(textvariable=string, font=('helvetica', 16, 'bold')).grid(padx=5, pady=5)
    thread = aens_time.Mille_Timer(update, string)
    thread.start()
    root.mainloop()

def update(string):
    string.set(aens_time.format(aens_time.seconds()))

if __name__ == '__main__':
    main()
