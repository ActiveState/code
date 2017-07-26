from StringIO import StringIO 
from tempfile import NamedTemporaryFile 
import sys 

class TempFile(object): 
    """A temporary file implementation that uses memory unless 
    either capacity is breached or fileno is requested, at which 
    point a real temporary file will be created and the relevant 
    details returned 
    """ 

    _strategies = (StringIO, NamedTemporaryFile) 

    def __init__(self, buffer, capacity): 
        """Creates a TempFile object containing the specified buffer. 
        If capacity is specified, we use a real temporary file once the 
        file gets larger than that size.  Otherwise, the data is stored 
        in memory. 
        """ 
        self.capacity = capacity 
        self._delegate = self._strategies[len(buffer) > self.capacity]() 
        self.write(buffer) 
    
    def fileno(self):
        """Forces this buffer to use a temporary file as the underlying.
        object and returns the fileno associated with it.
        """
        if isinstance(self._delegate, self._strategies[0]):
            new_delegate = self._strategies[1]()
            new_delegate.write(self.getvalue())
            self._delegate = new_delegate
        return self._delegate.fileno()

    def write(self, value):
        if isinstance(self._delegate, self._strategies[0]): 
            len_value = len(value) 
            if len_value >= self.capacity: 
                needs_new_strategy = True 
            else: 
                self.seek(0, 2)  # find end of file 
                needs_new_strategy = \
                    (self.tell() + len_value) >= self.capacity 
            if needs_new_strategy: 
                new_delegate = self._strategies[1]() 
                new_delegate.write(self.getvalue()) 
                self._delegate = new_delegate 
        self._delegate.write(value)

    def __getattr__(self, name): 
        try: 
            return getattr(self._delegate, name) 
        except AttributeError: 
            # hide the delegation 
            e = "object '%s' has no attribute '%s'" \
                     % (self.__class__.__name__, name) 
            raise AttributeError(e) 


if __name__ == "__main__": 
    print "testing tempfile:" 
    tmp = TempFile("", 100) 
    ten_chars = "1234567890" 
    tmp.write(ten_chars * 5) 
    print "tmp < 100: ", tmp._delegate
    tmp.write(ten_chars * 5) 
    print "tmp == 100: " , tmp._delegate
    tmp.write("the last straw") 
    print "tmp > 100: " , tmp._delegate
