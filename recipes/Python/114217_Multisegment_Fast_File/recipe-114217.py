# mget.py
#
# by Nelson Rush
#
# MIT/X license.
#
# A simple program to download files in segments.
#
# - Fixes by David Loaiza for Python 2.5 added.
# - Nelson added fixes to bring the code to 2.7 and add portability between Windows/Linux.
# - The output of segment information has been corrected and cleaned up.
# - In outside cases where the client instances were not being closed, they are now closed.
#
import sys
import os
import asyncore
import socket
import platform
from string import *
from math import *
from time import *
from mmap import *

platformName = platform.system()
SEEK_BEG = 0
SEEK_SET = 1
SEEK_END = 2

class http_client(asyncore.dispatcher):
    def __init__ (self,host,path,parts,pbegin=0,pend=0,m=None):
        asyncore.dispatcher.__init__(self)
        # Initialize class member variables.
        self.keepalive = False
        self.done = 0
        self.h = [self]
        self.recvhead = 1
        self.bytes = 0
        self.ack = 0
        self.begin = time()
        self.path = path
        self.parts = parts
        self.host = host
        self.buffer = ""
        self.pbegin = pbegin
        self.pend = pend
        self.length = 8192
        self.f = None
        # Grab the filename from the end of the URL.
        self.filename = split(path,"/")[-1]
        # Check if file exists and if so ask if overwrite necessary.
        if os.access(self.filename,os.O_RDWR) and self.parts > 0:
            u = raw_input("File already exists, overwrite? [y/N] ")
            if u == 'y' or u == 'Y':
                print "Overwriting..."
            else:
                print "Aborting..."
                return None
        # Connect to the host with it on port 80.
        print "Connecting..."
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 80))
        # Parts are greater than 0 so we are the parent, open file, get header.
        if self.parts > 0:
            # Open and memory map the file.
            self.f = open(self.filename,'wb+')
            self.f.write("\0")
            self.f.flush() # We have to flush to make the file buffer ready for mmap.
            # Windows uses 0 for second parameter to auto-size to current file size.
            # Whereas, on Linux and other platforms, mmap requires a size.
            if platformName == "Windows":
                self.m = mmap(self.f.fileno(), 0)
            else:
                self.m = mmap(self.f.fileno(), os.fstat(self.f.fileno()).st_size)
            # Download the header.
            self.buffer = "HEAD %s HTTP/1.1\r\nHost: %s\r\n\r\n" % (self.path,self.host)
            print "Downloading http://%s%s" % (self.host,self.path)
        # Otherwise, we are a child, skip the header and download our segment.
        elif self.parts == 0:
            # Set our own mmap to the one given to us by the parent.
            self.m = m
            # Prepare ourselves to download the segment.
            self.bytes = self.pbegin
            self.length = self.pend
            self.recvhead = 2
            self.buffer = "GET %s HTTP/1.1\r\nHost: %s\r\nRange: bytes=%lu-%lu\r\n\r\n" % (self.path,self.host,self.pbegin,self.pend)
            print self.buffer
    def handle_connect(self):
        pass
    def handle_read(self):
        # Recieve incoming data.
        data = self.recv(8192)
        # Handle recieving the header, stage 1.
        if self.recvhead == 1:
            self.head = data
            print self.head
            # If the file was not found, exit.
            if find(data,"404 Not Found") > -1:
                print "404 Not Found"
                self.close()
                self.m.close()
                self.f.close()
                return None
            # Was it found, if not just check if OK.
            if find(data,"302 Found") == -1:
                # If we did not recieve the OK, exit.
                if find(data,"200 OK") == -1:
                    print "Unable to continue download."
                    self.close()
                    self.m.close()
                    self.f.close()
                    return None
            # If we cannot determine the length of the file, exit.
            if find(data,"Content-Length") == -1:
                print "Cannot determine size."
                self.close()
                self.m.close()
                self.f.close()
                return None
            # Determine the length of the file.
            line = self.head[find(self.head,"Content-Length"):]
            line = line[:find(line,"\r\n")]
            line = line[find(line,":")+1:]
            self.length = int(line)
            self.m.resize(self.length)
            self.recvhead = 2
            # If the number of parts is 1, only get the file.
            if self.parts == 1:
                self.buffer = "GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" % (self.path,self.host)
                print self.buffer
                self.pbegin = 0
                self.pend = self.length
            # If the parts is greater than 1, split into segments.
            elif self.parts > 1:
                l = self.length / self.parts
                print "Segment size =",l
                # Download the other segments in separate instances.
                if self.parts == 2:
                    self.h.append(http_client(self.host,self.path,0,l + 1,self.length,self.m))
                if self.parts > 2:
                    for i in range(1,self.parts-1):
                        self.h.append(http_client(self.host,self.path,0,(i * l) + 1,(i+1) * l,self.m))
                    self.h.append(http_client(self.host,self.path,0,((i+1) * l) + 1,self.length,self.m))
                # Set up the parent download, from beginning of file to segment size.
                self.buffer = "GET %s HTTP/1.1\r\nHost: %s\r\nRange: bytes=0-%lu\r\n\r\n" % (self.path,self.host,l)
                self.length = l
                self.pbegin = 0
                self.pend = self.length
                print self.buffer
        # Stage 2, clip the second incoming header and start grabbing the file itself.
        elif self.recvhead == 2:
            # A blank line specifies the end of the header.
            body = data[find(data,"\r\n\r\n")+4:]
            size = len(body)
            if size > 0:
                # Write what we have to the file.
                self.m[self.bytes:self.bytes+size] = body
                self.bytes += size
                # Keep track of position and inform the user every 1k downloaded.
                if len(xrange(size / 1024)) == 0:
                    self.ack = size
                else:
                    print "Segment %7lu-%7lu\t\ts%7lu to %7lu bytes recieved" % (self.pbegin,self.pend,self.bytes-size,self.bytes-1)
                if self.bytes >= self.length:
                    self.complete = time()
                    self.close()
            self.recvhead = 0
        # Just download the rest of the file.
        else:
            size = len(data)
            dataend = self.bytes + size
            self.m[self.bytes:dataend] = data
            self.bytes += size
            # Keep track of position and inform the user every 1k downloaded.
            if len(xrange(size / 1024)) == 0:
                self.ack += size
            else:
                print "Segment %7lu-%7lu\t\t%7lu to %7lu bytes recieved" % (self.pbegin,self.pend,self.bytes-size,self.bytes-1)
            if len(range(self.ack / 1024)) > 0:
                print "Segment %7lu-%7lu\t\t%7lu to %7lu bytes recieved" % (self.pbegin,self.pend,self.bytes-size,self.bytes-1)
                self.ack -= (1024 * len(xrange(self.ack / 1024)))
            if self.bytes >= self.length:
                self.complete = time()
                self.close()
    # Check to see if the buffer is clear.
    def writable(self):
        return(len(self.buffer) > 0)
    # Handle transmission of the data.
    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
    # Handle closing of the connection.
    def handle_close(self):
        self.complete = time()
        if self.bytes > self.length:
            self.bytes = self.bytes - 1
        print "Segment %7lu-%7lu\t\t%7lu to %7lu bytes recieved" % (self.pbegin,self.pend,self.bytes,self.length)
        self.close()

# Main
if __name__ == '__main__':
    from urlparse import *
    if len(sys.argv) < 2:
        print 'usage: %s host' % sys.argv[0]
    else:
       url = sys.argv[1]
       if find(url,"http://") == -1:
           url = "http://" + url
       url = urlparse(url)
       client = http_client(url[1],url[2],3)
       asyncore.loop()
       client.m.close()
       client.f.close()
       print "Client download finished."
