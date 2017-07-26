import os 
import sys
import sh
from Queue import Queue
from threading import Thread
from termcolor import colored
from argparse import ArgumentParser
from time import sleep
from errno import EWOULDBLOCK

def highlight(rest_of_line):
    s = rest_of_line
    for x in rest_of_line.split():
        if x.startswith("http"):
            s = s.replace(x,colored(x,'blue',attrs = ['bold']))
    return s

def split_line(line):
    for pos in range(15,len(line)):
        if line[pos] == ' ':
            return line[:13], line[13:pos].strip(), line[pos:].strip()
   
def tail_f(some_file):
    for line in sh.tail("-f", some_file, _iter_noblock=True):
        yield line

def line_gen(basedir,chan):
    subdir = chan+".chat"
    sdpath = os.path.join(basedir,subdir)
    fn = max(x for x in os.listdir(sdpath) if x.endswith(".txt"))
    path = os.path.join(sdpath,fn)
    ch = chan.encode('utf-8')
    for x in tail_f(path):
        if x == EWOULDBLOCK:
            continue
        s = x.encode('utf-8')
        time,name,rest = split_line(s)
        if name[-1] == ':'.encode('utf-8'):
            t = colored(time,'cyan',attrs=['bold'])
            c = colored(ch,'cyan',attrs=['bold'])
            n = colored(name,'red',attrs=['bold'])
            r = highlight(rest)
        else:
            t = colored(time,'cyan')
            c = colored(ch,'cyan')
            n = colored(name,'yellow',attrs=['dark'])
            r = colored(rest,attrs=['dark'])   
        yield ' '.join((t,c,n,r))
    
def consume(q, s):
    while not exitapp:
        q.put(s.next())
        
def merge(iters):
    q = Queue()
    for it in iters:
        t = Thread(target=consume, args=(q, it))
        t.daemon = True
        t.start()
    while True:
        if q.empty():
            sleep(.1)
        else:
            yield q.get()

def run(directory, channels):
    basedir = os.path.expanduser(directory)
    for x in merge(line_gen(basedir,ch) for ch in channels):
        print x
    
def main():
    parser = ArgumentParser(description = 'tail, merge, and colorize pidgin irc text logs')
    parser.add_argument('-d','--directory', 
        help='the directory that has the directories of the chat logs as subdirectories')
    parser.add_argument('-c','--channels', 
        help='a quoted string containing a list of irc channel names separated by spaces')
    args = parser.parse_args()
    run(args.directory, args.channels.split())

exitapp = False
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exitapp = True
        sys.exit(0)
