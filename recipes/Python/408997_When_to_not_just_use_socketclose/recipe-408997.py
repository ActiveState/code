def recv_end(the_socket):
    End='SERVER WRONG MARKER'
    total_data=[];data='';got_end=False
    while True:
            data=the_socket.recv(8192)
            if not data: break
            if End in data:
                total_data.append(data[:data.find(End)])
                got_end=True
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if End in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(End)]
                    total_data.pop()
                    got_end=True
                    break
    return (got_end,''.join(total_data))
         
def basic_server(sock):
    got=[]
    got_end,data = recv_end(sock)
    if not got_end:  
        sock.send('ERROR:no end!') #<--- not possible w/close()
    else: sock.sendall(data*2)
    sock.shutdown(1)
    sock.close()
    
import socket
Port=4444
def start_server():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('',Port))
    sock.listen(5)
    print 'started on',Port
    while True:
        newsock,address=sock.accept()
        basic_server(newsock)

def send_data(data):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('localhost',Port))
    print 'connected'
    sock.sendall(data+'CLIENT WRONG MARKER')
    print 'sent',data
    sock.shutdown(1)
    print 'shutdown'
    result=[]
    while True:
       got=sock.recv(2)
       if not got: break
       result.append(got)
    sock.close()
    return ''.join(result)
        
if __name__=='__main__':
    start_server()
