import threading
import sys, os
import time
import unicodedata

class SpinCursor(threading.Thread):
    """ A console spin cursor class """
    
    def __init__(self, msg='',maxspin=0,minspin=10,speed=5):
        # Count of a spin
        self.count = 0
        self.out = sys.stdout
        self.flag = False
        self.max = maxspin
        self.min = minspin
        # Any message to print first ?
        self.msg = msg
        # Complete printed string
        self.string = ''
        # Speed is given as number of spins a second
        # Use it to calculate spin wait time
        self.waittime = 1.0/float(speed*4)
        if os.name == 'posix':
            self.spinchars = (unicodedata.lookup('FIGURE DASH'),u'\\ ',u'| ',u'/ ')
        else:
            # The unicode dash character does not show
            # up properly in Windows console.
            self.spinchars = (u'-',u'\\ ',u'| ',u'/ ')        
        threading.Thread.__init__(self, None, None, "Spin Thread")
        
    def spin(self):
        """ Perform a single spin """

        for x in self.spinchars:
            self.string = self.msg + "...\t" + x + "\r"
            self.out.write(self.string.encode('utf-8'))
            self.out.flush()
            time.sleep(self.waittime)

    def run(self):

        while (not self.flag) and ((self.count<self.min) or (self.count<self.max)):
            self.spin()
            self.count += 1

        # Clean up display...
        self.out.write(" "*(len(self.string) + 1))
        
    def stop(self):
        self.flag = True
        
if __name__ == "__main__":
    spin = SpinCursor(msg="Spinning...",minspin=5,speed=5)
    spin.start()
