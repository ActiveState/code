# amachine.py
# a tiny stack machine for our new language A, nothing special.
import math, os, re, operator, sys
end=[]
def run(l):
    stack=[[]]
    for i in l:
        if i is end:
            f=stack.pop()
            i=f[0](*f[1:])
        if callable(i):
            stack.append([i])
        else:
            stack[-1].append(i)
# end of amachine.py

# atest.py (written in our new language A)
# encoding: acodec
sys.stdout.write  "Hello!\n";
sys.stdout.write "4 *  sin(pi/4) + 3 = ";
sys.stdout.write str 
    operator.add operator.mul 4 math.sin math.pi/4;; 3;;;   
sys.stdout.write  "\n";
# End of atest.py

# Looks like atest.py can be executed by our tiny stack machine.
# After all, it is written in Language A.
# But certainly it can not be executed by the python interpreter directly.
# Obviously, atest.py is not written in Python. 
# Or is it?

# After load the following module, it is Python enough for the python interpreter.

# acodec.py
import encodings, codecs, re, sys
# a mini tokenizer
_qs=r"'(?:[^'\\\n]|\\.|\\\n)*?'(?!')|'''(?:[^\\]|\\.)*?'''"
String = r"[uU]?[rR]?(?:%s|%s)"%(_qs, _qs.replace("'",'"'))
Comment=r'\#.*'
Name= r"[^#\"'\s\n;]+"
tok_re=re.compile(r"%s|%s|%s|(?P<e>[;\.])"%(Name, String , Comment))

# Our StreamReader
class aStreamReader(codecs.StreamReader):
    def readline(self, size=None, keepends=True):
        def repl(m):
            r=m.group()
            return "end," if m.group("e") else r+","
        if getattr(self, "pysrc", None)==None:			
            r=self.stream.read().decode("utf8")
            r="from amachine import *;run([%s])" % tok_re.sub(repl,r)
            self.pysrc=r.splitlines()
        return  u'%s\n'%self.pysrc.pop(0) if self.pysrc else u''
        
def search_function(s):
    if s!="acodec": 
        return None
    u8=encodings.search_function("utf8")
    return codecs.CodecInfo( name='acodec', 
        encode=u8.encode, decode=u8.decode,
        incrementalencoder=u8.incrementalencoder,
        incrementaldecoder=u8.incrementaldecoder,
        streamreader=aStreamReader,        # acodec StreamReader
        streamwriter=u8.streamwriter)

codecs.register(search_function)  # register our new codec search function
# End of acodec.py

# to test
# import acodec
# execfile("atest.py")   # Executed like python
# import atest.py        # Imported like python
# You can also use site.py or .pth file to load acodec.py automaticly. 
# then you can simply:
# python atest.py
