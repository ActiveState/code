import types
import os

class FileAdaptor:
    """A FileAdaptor instance takes a 'file-like' object having at
    least a 'read' method and, via the file method, returns a true file
    object."""
    def __init__(self, fileObj):
        self.fileObj = fileObj
        self.chunksize = 1024 * 10

        # If the input file-like object is actually a true file object,
        # we don't need to do anything.
        if type(self.fileObj) != types.FileType:
            # The file-like object must have a read method.
            if not hasattr(fileObj, "read"):
                raise ValueError, "not a file-like object"
            
            # Create our true file object as a temp file.
            self.tmpFileObj = os.tmpfile()

            # Read from the input file-like object (via its read method)
            # in chunks so we don't chew up too much memory, and write
            # out to the temp file.
            while True:
                data = fileObj.read(self.chunksize)
                if len(data) == 0:
                    break
                self.tmpFileObj.write(data)

            del data                

            # Make sure the temp file is ready to be read from its start.
            self.tmpFileObj.flush()
            self.tmpFileObj.seek(0, 0)

            self.fileObj = self.tmpFileObj                
        return

    def file(self):
        """Return the true file object."""
        return self.fileObj
