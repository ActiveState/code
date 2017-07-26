#!/usr/bin/env python
import socket, threading, time

def handle(s):
  print s
  print repr(s.recv(4096))
  html = "<html><body>"
  html += time.asctime()
  html += "</body></html>"
  
  s.send(html)
  s.close()
  
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8888));
s.listen(1);
while 1:
  t,_ = s.accept();
  threading.Thread(target = handle, args = (t,)).start()

#After running this, open a browser and go to http://localhost:8888/
