import bisect

class AutoExp:
    def __init__(self, camera):
        self.camera = camera
    def __getitem__(self, index):
        self.camera.setshutter(index)
        im = cam.getframe() # returns a numarray array
        return im.mean()

def auto_expose(camera, target_mean=128):
    ms = bisect.bisect(AutoExp(camera), target_mean, 0, 1000)
    camera.setshutter(ms)
