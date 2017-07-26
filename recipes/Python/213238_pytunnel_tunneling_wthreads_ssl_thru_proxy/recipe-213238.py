import threading,socket,traceback,sys,httplib,pprint,select,base64,time
 
def recv_all(the_socket,timeout=''):
    #setup to use non-blocking sockets
    #assume proxy network connection is worse than locahost
    #if no data arrives it assumes transaction is done
    #recv() returns a string; it's an upper bound on len(sock.recv())
    the_socket.setblocking(0)
    total_data=[];data=''
    begin=time.time()
    if not timeout:
        timeout=1
    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break
        wait=0
        try:
            data=the_socket.recv(4096)
            if data:
                total_data.append(data)
                begin=time.time()
                data='';wait=0
            else:
                time.sleep(0.1)
        except:
            pass
        #When a recv returns 0 bytes, other side has closed
    result=''.join(total_data)
    return result
 
class thread_it ( threading.Thread ) :
    done=0
    def __init__(self,tid='',proxy='',server='',tunnel_client='',\
                 port=0,ip='',timeout=0,slow=0):
        threading.Thread.__init__(self)
        self.tid=tid
        self.proxy=proxy
        self.port=port
        self.server=server
        self.tunnel_client=tunnel_client
        self.ip=ip;self._port=port
        self.data={} #store data here to get later
        self.timeout=timeout
    def run ( self ): #overridden from threading library
        try:
            if self.proxy and self.server:
                ins=[self.server,self.proxy]
                ous=[];data={};adrs={}
                new_socket=0
                while not thread_it.done:
                    if not new_socket:
                        new_socket,address=self.server.accept()
                    else:
                        self.proxy.sendall(
                                  recv_all(new_socket,timeout=self.timeout))
                        new_socket.sendall(
                                  recv_all(self.proxy,timeout=self.timeout))
            elif self.tunnel_client:
                self.tunnel_client(self.ip,self.port)
                thread_it.done=1
        except Exception,error:
            print traceback.print_exc(sys.exc_info()),error
            thread_it.done=1
class build:
    def __init__(self,host='',port=443,proxy_host='',proxy_port=80,
                 proxy_user='',proxy_pass='',proxy_type='',timeout=0):
        #initialize variables
                                                                                
        self._port=port;self.host=host;self._phost=proxy_host;self._puser=proxy_user
        self._pport=proxy_port;self._ppass=proxy_pass;self._ptype=proxy_type
        self.ip='127.0.0.1';self.timeout=timeout
        #setup variables
        self._server,self.server_port=self.get_server()
    def get_proxy(self):
        if not self._ptype:
            proxy=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            proxy.connect((self._phost,self._pport))
            proxy_authorization=''
            if self._puser:
                proxy_authorization='Proxy-authorization: Basic '+\
                base64.encodestring(self._puser+':'+self._ppass).strip()+'\r\n'
            proxy_connect='CONNECT %s:%sHTTP/1.0\r\n'%(self.host,self._port)
            user_agent='User-Agent: pytunnel\r\n'
            proxy_pieces=proxy_connect+proxy_authorization+user_agent+'\r\n'
            proxy.sendall(proxy_pieces+'\r\n')
            response=recv_all(proxy,timeout=0.5)
            status=response.split()[1]
            if int(status)/100 !=2:
                print 'error',response
                raise status
            return proxy
    def get_server(self):
        port=2222
        server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #localhost = only visible to this machine
        server.bind(('localhost',port))
        server.listen(5)
        return server,port
    def run(self,func):
        Threads=[]
        Threads.append( thread_it(tid=0,proxy=self.get_proxy(),\
                                  server=self._server,timeout=self.timeout))
        Threads.append( thread_it(tid=1,tunnel_client=func,ip=self.ip,\
                                  port=self.server_port,timeout=0.5))
 
        for Thread in Threads: #now go thru list and start threads running
            Thread.start() #call the run function
                print 'error',response
                raise status
            return proxy
    def get_server(self):
        port=2222
        server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #localhost = only visible to this machine
        server.bind(('localhost',port))
        server.listen(5)
        return server,port
    def run(self,func):
        Threads=[]
        Threads.append( thread_it(tid=0,proxy=self.get_proxy(),\
                                  server=self._server,timeout=self.timeout))
        Threads.append( thread_it(tid=1,tunnel_client=func,ip=self.ip,\
                                  port=self.server_port,timeout=0.5))
 
        for Thread in Threads: #now go thru list and start threads running
            Thread.start() #call the run function
        for Thread in Threads: #make main thread wait for all in list to 
            Thread.join()
