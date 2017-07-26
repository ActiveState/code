from pawt import swing
from java import net

def view(url):
	frame = swing.JFrame("Image: " + url, visible=1)
	frame.getContentPane().add(swing.JLabel(swing.ImageIcon(net.URL(url))))
	frame.setSize(400,250)
	frame.show()
	
view("http://www.python.org/pics/pythonHi.gif")
