# The natural approach would be to do initialization in the object 
# constructor:

class counter:
    def __init__(self):
        self.count = 0
    def next(self):
        self.count += 1
        return self.count


# But Python offer a terse and efficient alternative:

class counter:
    count = 0
    def next(self):
        self.count += 1
        return self.count
