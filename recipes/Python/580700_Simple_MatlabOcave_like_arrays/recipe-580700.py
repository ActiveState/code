import code, re
import numpy

class MatLikeListConsole(code.InteractiveConsole):
    def push(self, line):
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        sqbr_re = re.compile(r'\[.*\]', re.S)
        list_found = re.findall(sqbr_re, source)
        if list_found:
            try:
                # [0] - assumes only one list at a time - limitation
                arr = numpy.array(numpy.mat(list_found[0].strip('[]')))
            except ValueError as e:
                print(e)
                more = False
            else:
                if arr.shape[0] == 1: # change single row matrix to 1D array 
                    arr = arr[0]
                str_np_arr = 'numpy.' + repr(arr) # back to string representation 
                more = self.runsource(re.sub(sqbr_re, str_np_arr, source), self.filename)
        else:
            # temporary change to string if only opening bracket present '['
            more = self.runsource(re.sub(r'\[', r"'''", source, re.S), self.filename) 
        if not more:
            self.resetbuffer()
        return more

console = MatLikeListConsole(locals=locals())
console.interact()


# and now...
>>> import matlist # assuming above code in this module or copy-paste to console window
Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:01:18) [MSC v.1900 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(MatLikeListConsole)
>>> A = [1 2 3] # 1D array
>>> A
array([1, 2, 3])
>>> 
>>> B = [1 2 3; # 2D matrix
... 4 5 6]
>>> B
array([[1, 2, 3],
       [4, 5, 6]])
>>> Error = [1 2; 3 4;] # wrong format
Rows not the same size.
>>> # Wiiiiii!!!
