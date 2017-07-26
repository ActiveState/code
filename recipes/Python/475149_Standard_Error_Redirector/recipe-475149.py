================================================================================
stderr_server.py
================================================================================
PORT = 1337

import socket
serv = socket.socket()
serv.bind(('', PORT))
serv.listen(1)
while True:
    data = ''
    recv = ' '
    conn = serv.accept()[0]
    while recv:
        recv = conn.recv(1024)
        if recv:
            data += recv
        else:
            print data
================================================================================
stderr_client.py
================================================================================
SERV = 'eve.dorms.bju.edu'
PORT = 1337

import socket, sys
conn = socket.socket()
conn.connect((SERV, PORT))
sys.stderr = conn.makefile()
================================================================================
test.py
================================================================================
import stderr_client

number = 1 / 0
