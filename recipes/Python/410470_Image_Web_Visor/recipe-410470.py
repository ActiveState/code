# ImageWebVisor
#------------------------------------------------------------
#| Thanks to the Jython  and aspn comunity to this program  |
#| This is a ImageWebVisor                                  |
#| You can see a image in the web and your system           |
#------------------------------------------------------------


import java.awt as awt
import java.lang as lang
from javax.swing import *
from java.net import URL

def exit(event):
    lang.System.exit(0)

class visor(JFrame):

    def __init__(self):
        JFrame.__init__(self,title="ImageWebVisor",size=(550,510),windowClosing=exit)
        self.contentPane.layout=awt.BorderLayout()
        self.dir=JTextField(preferredSize=(400,30))
        boton=JButton("Ver/View",preferredSize=(100,30),actionPerformed=self.pres)
        panel=JPanel()
        panel.add(self.dir)
        panel.add(boton)
        self.label=JLabel("",horizontalAlignment=SwingConstants.CENTER,verticalAlignment=SwingConstants.CENTER)
        self.bar=JScrollPane(self.label)
        self.contentPane.add(panel,awt.BorderLayout.NORTH)
        self.contentPane.add(self.bar,awt.BorderLayout.CENTER)
        
        self.dir.text="URL de la Imagen a ver/ URL of imagen to view"
        
    def pres(self,event):
        title=self.dir.text
        self.setTitle(title)
        self.label.setIcon(ImageIcon(URL(title)))
        self.show()
        
        

if __name__=="__main__":
    visor().show()
