import os

class CheckExt:
    def __init__(self, ext):
        self.ext=ext
    def checkExt(self, file):
        if os.path.splitext(file)[-1]==self.ext: return 1

def getFilesByExt(dir, ext):
    ce = CheckExt(ext)
    return filter(ce.checkExt, os.listdir(dir))




if __name__ == '__main__':
    """ quick test to see if works """
    print getFilesByExt('.', '.py')
    raw_input('press any key') # if run by double click
