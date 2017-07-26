End='something useable as an end marker'

def send_to_end(sock,data): 
    #assume the data is appendable, may need to stringify the data
    sock.sendall(data+End) 
    
def recvall2(the_socket): 
    #instead of doing
    #data=the_socket.recv(8192) 
    #return data 
    total_data=[];data='' 
    while True: 
            #if recv returns 0 bytes, other side has closed 
            data=the_socket.recv(8192) 
            if End in data: 
                total_data.append(data[:data.find(End)]) 
                break 
            total_data.append(data) 
            if len(total_data)>1: 
                #check if end_of_data was split 
                last_pair=total_data[-2]+total_data[-1] 
                if End in last_pair: 
                    total_data[-2]=last_pair[:last_pair.find(End)] 
                    total_data.pop() 
                    break 
    result=''.join(total_data) 
    return result   
