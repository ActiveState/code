import ctypes
import time
import turtle

class SensorData(ctypes.Structure):
    _fields_ = [
        ('status', ctypes.c_int),
        ('raw_x', ctypes.c_short),
        ('raw_y', ctypes.c_short),
        ('x', ctypes.c_short),
        ('y', ctypes.c_short),
        ('temp', ctypes.c_byte),
        ('center_x', ctypes.c_short),
        ('center_y', ctypes.c_short),
    ]

def getXY():
    data = SensorData()
    ctypes.windll.Sensor.ShockproofGetAccelerometerData(ctypes.byref(data))
    return data.raw_x / 10.0, data.raw_y / 10.0

def main():
    centerx, centery = getXY()
    turtle.pensize(3)
    while 1:
        x, y = getXY()
        turtle.left(centery-y)
        turtle.forward(centerx-x)
        time.sleep(0.01)

if __name__ == '__main__':
    main()
