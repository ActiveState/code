import random
from multiprocessing import Process, Queue, Pipe
import sys
import time #For the timestamp and sleep function
if sys.platform == "win32":
  # On Windows, the best timer is time.clock()
  default_timer = time.clock
else:
  # On most other platforms, the best timer is time.time()
  default_timer = time.time

def pa(child_conn, parent_q):
  keep_running = True
  while keep_running:
    r = random.randint(0,10)
    if r == 10:
      parent_q.put([0, default_timer()])
    if child_conn.poll():
      msg = child_conn.recv()
      this_time = default_timer()
      if msg == 'quit':
        keep_running = False
      else:
        print this_time - msg

def pb(child_conn, parent_q):
  keep_running = True
  while keep_running:
    r = random.randint(0,10)
    if r == 10:
      parent_q.put([1, default_timer()])
    if child_conn.poll():
      msg = child_conn.recv()
      this_time = default_timer()
      if msg == 'quit':
        keep_running = False
      else:  
        print this_time - msg
  

if __name__ == '__main__':
  parent_conn0, child_conn0 = Pipe()
  parent_conn1, child_conn1 = Pipe()
  parent_q = Queue()
  p0 = Process(target=pa, args=(child_conn0, parent_q))
  p0.start()
  p1 = Process(target=pb, args=(child_conn1, parent_q))
  p1.start()
  keep_running = True
  while keep_running:
    ans = parent_q.get()#Blocking get
    this_time = default_timer()
    print ans[0], this_time - ans[1]
    r = random.randint(0,20)
    if r==10:
      parent_conn0.send('quit')
      parent_conn1.send('quit')
      keep_running = False
    else:
      parent_conn0.send(default_timer())
      parent_conn0.send(default_timer())
  p0.join()
  p1.join()
