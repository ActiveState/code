#!/usr/bin/python
import struct, socket, sys, time
# Working: nbd protocol, read/write serving up files, error handling, file size detection, in theory, large file support... not really, so_reuseaddr, nonforking

def recvall(sock, length):
  rv = []
  while sum(map(len, rv)) < length:
    rv.append(sock.recv(length-sum(map(len, rv))))
    assert rv[-1], "no more data to read"
  return ''.join(rv)

def serveclient():
    READ, WRITE, CLOSE = 0,1,2
    "Serves a single client until it exits."
    afile.seek(0, 2)
    asock.send('NBDMAGIC\x00\x00\x42\x02\x81\x86\x12\x53' + struct.pack('>Q', afile.tell()) + '\0'*128);
    while True:
        header = recvall(asock, struct.calcsize('>LL8sQL'))
        magic, request, handle, offset, dlen = struct.unpack('>LL8sQL', header)
        assert magic == 0x25609513
        if request == READ:
            afile.seek(offset)
            asock.send('gDf\x98\0\0\0\0'+handle)
            asock.send(afile.read(dlen))
            print "read\t0x%08x\t0x%08x" % (offset, dlen), time.time()
        elif request == WRITE:
            afile.seek(offset)
            afile.write(recvall(asock, dlen))
            afile.flush()
            asock.send('gDf\x98\0\0\0\0'+handle)
            print "write\t0x%08x\t0x%08x" % (offset, dlen), time.time()
        elif request == CLOSE:
            asock.close()
            print "closed"
            return
        else:
            print "ignored request", request

if __name__ == '__main__':
    "Given a port and a filename, serves up the file."
    afile = file(sys.argv[2], 'rb+')
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind(('', int(sys.argv[1])))
    lsock.listen(5)
    while True:
        (asock, addr) = lsock.accept()
        print "connection from", addr
        serveclient()
