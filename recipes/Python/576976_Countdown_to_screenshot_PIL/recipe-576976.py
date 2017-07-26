import time
import ImageGrab
def screeny():
    for ii in range(1, 11, 1)[::-1]:
        time.sleep(1)
        print ii
    img=ImageGrab.grab()
    img.save(r"C:\blblblblblblaa\screeny.jpg")
