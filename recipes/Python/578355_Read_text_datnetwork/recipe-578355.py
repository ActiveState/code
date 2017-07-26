# To test it with netcat, start the script and execute:
# 
#    echo "Hello, cat." | ncat.exe 127.0.0.1 12345
#
import socket

HOST = 'localhost'   # use '' to expose to all networks
PORT = 12345

def incoming(host, port):
  """Open specified port and return file-like object"""
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # set SOL_SOCKET.SO_REUSEADDR=1 to reuse the socket if
  # needed later without waiting for timeout (after it is
  # closed, for example)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((host, port))
  sock.listen(0)   # do not queue connections
  request, addr = sock.accept()
  return request.makefile('r', 0)
# /-- network ---


for line in incoming(HOST, PORT):
  print line,
