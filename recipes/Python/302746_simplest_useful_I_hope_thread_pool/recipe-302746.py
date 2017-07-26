import threading,Queue,time,sys,traceback

#Globals (start with a captial letter)
Qin  = Queue.Queue() 
Qout = Queue.Queue()
Qerr = Queue.Queue()
Pool = []   

def err_msg():
    trace= sys.exc_info()[2]
    try:
        exc_value=str(sys.exc_value)
    except:
        exc_value=''
    return str(traceback.format_tb(trace)),str(sys.exc_type),exc_value

def get_errors():
    try:
        while 1:
            yield Qerr.get_nowait()
    except Queue.Empty:
        pass

def process_queue():
    flag='ok'
    while flag !='stop':
        try:
            flag,item=Qin.get() #will wait here!
            if flag=='ok':
                newdata='new'+item
                Qout.put(newdata)
        except:
            Qerr.put(err_msg())
            
def start_threads(amount=5):
    for i in range(amount):
         thread = threading.Thread(target=process_queue)
         thread.start()
         Pool.append(thread)
def put(data,flag='ok'):
    Qin.put([flag,data]) 

def get(): return Qout.get() #will wait here!

def get_all():
    try:
        while 1:
            yield Qout.get_nowait()
    except Queue.Empty:
        pass
def stop_threads():
    for i in range(len(Pool)):
        Qin.put(('stop',None))
    while Pool:
        time.sleep(1)
        for index,the_thread in enumerate(Pool):
            if the_thread.isAlive():
                continue
            else:
                del Pool[index]
            break
#STANDARD use:
for i in ('b','c'): put(i)
start_threads()
stop_threads()
for i in get_all(): print i
for i in get_errors(): print i

#POOL use
#put element into input queue
put('a')

#setup threads -- will run forever as a pool until you shutdown
start_threads() 

for i in ('b','c'): put(i)

#get an element from output queue
print get() 

#put even more data in, 7 causes an error
for i in ('d','e',7): put(i)
#get whatever is available
for i in get_all(): print i

#stop_threads only returns when all threads have stopped
stop_threads()
print '__threads finished last data available__'
for i in get_all(): print i
for i in get_errors(): print i
#starting up threads again
start_threads()
put('f')
stop_threads()
print '__threads finished(again) last data available__'
for i in get_all(): print i
for i in get_errors(): print i
