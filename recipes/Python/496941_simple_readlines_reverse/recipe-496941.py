import collections,cStringIO

def rev_readlines(arg):
    f=open(arg,'rb')
    f.seek(0,2)# go to the end
    line=collections.deque()
    while f.tell():    
        f.seek(-1,1)
        c=f.read(1)
        f.seek(-1,1)
        line.appendleft(c)
        if c =='\n':
            yield ''.join(line).strip()
            line.clear() #clear for next line
    yield ''.join(line).strip()

#bit of optimization, load groups of bytes from disk into memory
def rev_readlines2(arg,bufsize=8192):
    f1=open(arg,'rb')
    f1.seek(0,2)# go to the end
    leftover=''
    while f1.tell():
        print f1.tell()
        if f1.tell()<bufsize: bufsize=f1.tell()
        f1.seek(-bufsize,1)
        in_memory=f1.read(bufsize)+leftover
        f1.seek(-bufsize,1)
        buffer=cStringIO.StringIO(in_memory)
        buffer.seek(0,2)# go to the end
        line=collections.deque()
        while buffer.tell():
            buffer.seek(-1,1)
            c=buffer.read(1)
            buffer.seek(-1,1)
            line.appendleft(c)
            if c =='\n':
                yield ''.join(line).strip()
                line.clear()
        leftover=''.join(line).strip()
    yield leftover

#different approach and much faster
def rev_readlines3(arg,bufsize=8192):
    f1=open(arg,'rb')
    f1.seek(0,2)# go to the end
    leftover=''
    while f1.tell():
        if f1.tell()<bufsize: bufsize=f1.tell()
        f1.seek(-bufsize,1)
        in_memory=f1.read(bufsize)+leftover
        f1.seek(-bufsize,1)
        lines=in_memory.split('\n')
        for i in reversed(lines[1:]): yield i
        leftover=lines[0]
    yield leftover

for i in rev_readlines(filename): print i
