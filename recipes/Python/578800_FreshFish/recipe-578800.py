import math
import time
import serial ## for heart rate monitor

try:
    import Adafruit_BBIO.GPIO as GPIO
    BBB = True
except:
    ## easier to write code on laptop then transfer to the BBB
    BBB = False

try:
    port = '/dev/ttyUSB0'
    ser = serial.Serial(port, baudrate=9600, timeout=.1)
except Exception, e:
    print 'No heartrate monitor detected', e
    ser = None

class FreshFish:
    '''
    Keep result around for specified time.  Refresh when "fish" goes bad
    '''
    def __init__(self, shelf_life=1):
        self.shelf_life = shelf_life
        self.last_time = 0
        self.last_result = None

    def __call__(self, f):
        def out():
            if time.time() - self.last_time < self.shelf_life:
                res = self.last_result
            else:
                res = f()
                self.last_time = time.time()
                self.last_result = res
            return res
        return out

@FreshFish(2)
def getHR():
    if BBB and ser:
        ser.write('G1' + chr(13))
        res = readline()
        if len(res) > 5:
            out = int(res.split()[2])
        else:
            out = 0
    else:
        ### return a dummy result
        out = int(50 * math.sin(time.time() / 20) + 50)
    return out

# ... in GUI

while True:
    ### getHR() gets called 10x / sec, but FreshFish limits hardware calls to 1x / 2 sec
    print getHR()
    time.sleep(.1) 
