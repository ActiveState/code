import os
import cPickle as pickle

class fileUpdate(file):
    def __init__(self, name, mode, bufsize=-1):
        file.__init__(self, name, mode, bufsize)
        self.pkl_path = '.%s.pkl' % name
        self.offset = None
        if os.path.exists(self.pkl_path):
            self.pkl_file = open(self.pkl_path)
            self.offset = pickle.load(self.pkl_file)

            self.seek(self.offset, 0)

    def close(self):
        self.recordExitOffset()
        file.close(self)

    def recordExitOffset(self):
        pickle.dump(self.tell(), open(self.pkl_path, 'w'))

    def next(self):
        try:
            return file.next(self)
        except StopIteration:
            self.recordExitOffset()
            raise StopIteration
