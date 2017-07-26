#WebSocket module, designed to be exactly like socket

import socket
import struct

from base64 import b64encode
import hashlib

import json

AF_INET = 0
WSOCK_STREAM = 1

class error(Exception):
    pass


class websocketclient:
    def __init__(self, socket):
        self.socket = socket
        #self.socket.setblocking(False)

    def __decodeWebSocket (self, data):  #JS PORT
        if data == b'\x81': return
        datalength = data[1] & 127;
        indexFirstMask = 2;
        if (datalength == 126):
            indexFirstMask = 4;
        elif (datalength == 127):
            indexFirstMask = 10;
        
        masks = data[indexFirstMask:indexFirstMask + 4]
        i = indexFirstMask + 4;
        index = 0;
        output = "";
        while (i < len(data)):
            output += chr(data[i] ^ masks[index % 4]);
            i += 1
            index += 1
    
        return output;

    def __encodeWebSocket(self, bytesRaw):
        print(bytesRaw)

        bytesFormatted = []
        bytesFormatted.append(struct.pack('B', 129))
        if (len(bytesRaw) <= 125):
            bytesFormatted.append(struct.pack('B', len(bytesRaw)))
        elif (len(bytesRaw) >= 126 and len(bytesRaw) <= 65535):
            bytesFormatted.append(struct.pack('B', 126));
            bytesFormatted.append(struct.pack('B', ( len(bytesRaw) >> 8 ) & 255));
            bytesFormatted.append(struct.pack('B', ( len(bytesRaw)      ) & 255));
            
        else:
            bytesFormatted.append(struct.pack('B', 127));
            bytesFormatted.append(struct.pack('B', ( len(bytesRaw) >> 56 ) & 255));
            bytesFormatted.append(struct.pack('B', ( len(bytesRaw) >> 48 ) & 255));
            bytesFormatted.append(struct.pack('B', (len( bytesRaw) >> 40 ) & 255));
            bytesFormatted.append(struct.pack('B', (len( bytesRaw) >> 32 ) & 255));
            bytesFormatted.append(struct.pack('B', (len( bytesRaw) >> 24 ) & 255));
            bytesFormatted.append(struct.pack('B', (len( bytesRaw) >> 16 ) & 255));
            bytesFormatted.append(struct.pack('B', ( len(bytesRaw) >>  8 ) & 255));
            bytesFormatted.append(struct.pack('B', ( len(bytesRaw)       ) & 255));
        
        for i in range(len(bytesRaw)):
            bytesFormatted.append(struct.pack('B', ord(bytesRaw[i])))
        
        return bytesFormatted;

    def recv(self):
        length, = struct.unpack('xB', self.socket.recv(2))
        firstbyte = length
        length &= 127

        addbytes = b""

        if length == 126:
            #Requires 2 more bytes of data
            addbytes = self.socket.recv(2)
            length, = struct.unpack("!H", addbytes)

        if length == 127:
            addbytes = self.socket.recv(8)
            length, = struct.unpack("!Q", addbytes)

        length += 4

        return [self.__decodeWebSocket(b'\x81' + struct.pack('B', firstbyte) + addbytes + self.socket.recv(length))]


        
        '''retlist = []
        for chunk in buffer.split(b'\x81'):
            pop = self.__decodeWebSocket(b'\x81' + chunk)
            if pop: retlist.append(pop)

        return retlist'''

    def send(self, string):
        self.socket.send(b''.join(self.__encodeWebSocket(string)))


class websocket:
    def __init__(self, flag1, flag2):
        if (flag1, flag2) != (AF_INET, WSOCK_STREAM):
            raise (error, "Only supports flags AF_INET, WSOCK_STREAM!")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self, data):
        self.socket.bind(data)

    def listen(self, conns):
        self.socket.listen(conns * 5)

    def accept(self):
        client, addr = self.socket.accept()
        handshake = client.recv(10000).decode().split("\r\n")

        newshake = {}
        for item in handshake:
            if ":" in item:
                newshake[item.split(":")[0]] = item.split(":")[1][1:]

        handshake = newshake

        m = hashlib.sha1()

        thehash = handshake['Sec-WebSocket-Key'] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        m.update(thehash.encode())
        thehash = b64encode(m.digest())

        header = b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: " + thehash + b"\r\n\r\n"           
        client.send(header)
        
        return websocketclient(client), addr
