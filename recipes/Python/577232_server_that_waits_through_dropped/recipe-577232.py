# Server code ------------------------------
from multiprocessing.connection import Listener
import time

address = ''
port = 6000
authkey = 'test'

keep_running = True
while keep_running:
  print 'Waiting for client'
  listener = Listener((address, port), authkey=authkey) 
  remote_conn = listener.accept()
  print 'Got client ' + listener.last_accepted[0] + ':%d' %(listener.last_accepted[1])

  try:
    while True:
      if remote_conn.poll():
        msg = remote_conn.recv()
        print 'msg: ' + msg
        if msg=='quit':
          keep_running = False
          break
      else:
        time.sleep(0.01)
  except EOFError:
    print 'Lost connection to client'
    listener.close()

## Client code ----------------------------------
from multiprocessing.connection import Client

address = ('', 6000)
conn = Client(address, authkey='test')
    
keep_running = True
while keep_running:
  msg=raw_input('Enter string ')
  conn.send(msg)
  if msg=='quit':
    keep_running = False
