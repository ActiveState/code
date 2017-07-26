class FileSpec(object):
    def __init__(self, path):
        self.drive, self.path_minus_drive = os.path.splitdrive(path)
        self.dir, self.name = os.path.split(path)
        self.corename, self.ext = os.path.splitext(self.name)
        self.ext = self.ext.lower()
        self.dir_minus_drive = self.dir[2:]        

    def substitute_drive(self, drive):
        return os.path.join(drive, os.sep, self.path_minus_drive)
        
    def substitute_dir(self, dir_):
        return os.path.join(dir_, self.name)
        
    def substitute_name(self, name):
        return os.path.join(self.dir, name)
        
    def substitute_corename(self, corename):
        return os.path.join(self.dir, corename + self.ext)
        
    def substitute_ext(self, ext):
        return os.path.join(self.dir, self.corename + ext)
