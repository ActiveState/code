import sys, os, struct, traceback
from cStringIO import StringIO

    
class ErlangPort(object):
    PACK = '!h'
    def __init__(self):
        self._in = sys.stdin
        self._out = sys.stdout
        
    def recv(self):
        buf = self._in.read(2)
        if len(buf) ==2:
            (sz,) = struct.unpack(self.PACK, buf)
            return self._in.read(sz)
        
    def send(self, what):
        sz = len(what)
        buf = struct.pack(self.PACK, sz)
        self._out.write(buf)
        return self._out.write(what)

    def run(self):
        buf = self.recv()
        while buf:
            try:
                result = self.process(buf)
            except:
                result = traceback.format_exc()
            self.send(result) 
            buf = self.recv()


class ErlangPortTest(ErlangPort):
    cmds = (0,lambda x: x+2, lambda x: x*2)
    def process(self, message):
        fn,arg = struct.unpack('!BB', message)
        res = self.cmds[fn](arg)
        return struct.pack('!B', res)



class ErlangPyTest(ErlangPortTest):
    class SandBox:
        def process(self, message):
            exec message
    sandbox = SandBox()
    def process(self, code):
        try:
            realout = sys.stdout
            sys.stdout = StringIO()
            self.sandbox.process(code)
            result = sys.stdout.getvalue()
        finally:
            if sys.stdout: sys.stdout.close()
            if realout: sys.stdout = realout
        return result
            

if __name__ =='__main__':
    import sys
    try:
        command = sys.argv[1]
        if command == 'PortTest':
            ErlangPortTest().run()
        elif command =='pytest':
            ErlangPyTest().run()
    except IndexError:
        print """
Usage:
First of all see the c Port section in the Erlang guide.
http://www.erlang.org/doc/tutorial/c_port.html#4

1. Start Erlang and compile the Erlang user guide example code:
http://www.erlang.org/doc/tutorial/complex1.erl


unix> erl
Erlang (BEAM) emulator version 4.9.1.2

Eshell V4.9.1.2 (abort with ^G)
1> c(complex1).
{ok,complex1}
    
3. Run the example.
2> complex1:start("python -u port.py PortTest").
<0.34.0>
3> complex1:foo(3).
4
4> complex1:bar(5).
10
5> complex1:stop().
stop
    
For more fun try.


6> c("c:\\tg\\python.erl").
:/tg/python.erl:42: Warning: variable 'Reason' is unused
{ok,python}
7> python:start("c:\\python25\\python.exe -u c:\\tg\\port.py pytest").
<0.38.0>
8> python:exec("import os")
9> python:exec("self.x = os.environ['PATH']").
* 2: syntax error before: python **
10> python:exec("import os").                  
[]
11> python:exec("self.x = os.environ['PATH']").
[]
12> python:exec("print self.x").
"H:\\PROGRA~1\\ERL55~1.5\\ERTS-5~1.5\\bin;H:\\PROGRA~1\\ERL55~1.5\\bin
m Files\\ActivePositionManager\\;C:\\WINNT\\system32;C:\\WINNT;C:\\WI
32\\Wbem;"
"""
