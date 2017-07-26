# Very Very Simple Web Server
# This can be used to demonstrate how HTTP works!!
# TO DO
#   create a simple html file
#   path = "C:/index.html"
#   open browser in address bar
#   http://127.0.0.1:50007/index.html
#
from socket import *
HOST = '127.0.0.1'                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket(AF_INET,SOCK_STREAM)
s.bind((HOST, PORT))
#format of response message(DO NOT ALTER IF YOU DONT KNOW WHAT U R DOING)
str ='''HTTP/1.0 200 OK
Connection: close
Content-Length: 1
Content-Type: text/html

'''
s.listen(1)
while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    data = conn.recv(1024)
    if not data: break
    file = open(data[4:data[4:].find(' ')+4]) # extracts filename from request
    str1 = file.read()
    file.close()
    data = str +str1
    conn.send(data)
    conn.close()
