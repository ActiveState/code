# In Python, you can't code "if x=foo():" -- assignment is a statement, thus
# you can't fit it into an expression, as needed for conditions of if and
# while statements, &c.  No problem, if you just structure your code around
# this.  But sometimes you're transliterating C, or Perl, or ..., and you'd
# like your transliteration to be structurally close to the original.
#
# No problem, again!  One tiny, simple utility class makes it easy...:

class DataHolder:
    def __init__(self, value=None): self.value = value
    def set(self, value): self.value = value; return value
    def get(self): return self.value
# optional but handy, if you use this a lot, either or both of:
setattr(__builtins__,'DataHolder',DataHolder)
setattr(__builtins__,'data',DataHolder())

# and now, assign-and-set to your heart's content: rather than Pythonic
while 1:
    line = file.readline()
    if not line: break
    process(line)
# or better in modern Python, but quite far from C-like idioms:
for line in file.xreadlines():
    process(line)
# you CAN have your C-like code-structure intact in transliteration:
while data.set(file.readline()):
    process(data.get())
