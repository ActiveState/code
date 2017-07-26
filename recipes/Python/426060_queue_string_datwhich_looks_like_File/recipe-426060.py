class StringQueue(object):
    def __init__(self, data=""):
        self.l_buffer = []
        self.s_buffer = ""
        self.write(data)

    def write(self, data):
        #check type here, as wrong data type will cause error on self.read,
        #which may be confusing.
        if type(data) != type(""):
            raise TypeError, "argument 1 must be string, not %s" % type(data).__name__
        #append data to list, no need to "".join just yet.
        self.l_buffer.append(data)

    def _build_str(self):
        #build a new string out of list
        new_string = "".join(self.l_buffer)
        #join string buffer and new string
        self.s_buffer = "".join((self.s_buffer, new_string))
        #clear list
        self.l_buffer = []

    def __len__(self):
        #calculate length without needing to _build_str
        return sum(len(i) for i in self.l_buffer) + len(self.s_buffer)

    def read(self, count=None):
        #if string doesnt have enough chars to satisfy caller, or caller is
        #requesting all data
        if count > len(self.s_buffer) or count==None: self._build_str()
        #if i don't have enough bytes to satisfy caller, return nothing.
        if count > len(self.s_buffer): return ""
        #get data requested by caller
        result = self.s_buffer[:count]
        #remove requested data from string buffer
        self.s_buffer = self.s_buffer[len(result):]
        return result


if __name__ == "__main__":
    sq = StringQueue()
    sq.write('some data')
    print sq.read(4)
    sq.write('_and_some_more_data_!')
    print sq.read(4)
    print sq.read()
