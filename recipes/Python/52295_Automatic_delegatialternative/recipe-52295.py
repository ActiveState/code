# ***if*** File _was_ a class...:
class UppercaseFile(File):
    # we could just override what we need to:
    def write(self, astring):
        return File.write(self, astring.upper())
    def writelines(self, strings):
        return File.writelines(self, map(string.upper,strings))
# ...arranging for an upperOpen(...) might not be quite trivial...

# but, File _isn't_ a class, so...:
class UppercaseFile:
    # initialization is explicit
    def __init__(self, file):
        # not self.file=file, to avoid triggering __setattr__
        self.__dict__['file'] = file

    # 'overrides' aren't very different:
    def write(self, astring):
        return self.file.write(self, astring.upper())
    def writelines(self, strings):
        return self.file.writelines(self, map(string.upper,strings))

    # automatic delegation isn't too difficult, either:
    def __getattr__(self, attr):
        return getattr(self.file, attr)
    def __setattr__(self, attr, value):
        return setattr(self.file, attr, value)        
# ...and upperOpen(whatever) is trivial indeed:
def upperOpen(*args):
    return UppercaseFile(open(*args))
