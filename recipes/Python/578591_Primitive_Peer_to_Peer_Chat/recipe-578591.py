#!usr/bin/env python

import socket
import threading
import select
import time

def main():

    class Chat_Server(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None
            def run(self):
                HOST = ''
                PORT = 1776
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                s.listen(1)
                self.conn, self.addr = s.accept()
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready \
                      = select.select ([self.conn],[self.conn],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.conn.recv(1024)
                        if data:
                            print "Them: " + data
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0
     
    class Chat_Client(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1
            def run(self):
                PORT = 1776
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, PORT))
                # Select loop for listen
                while self.running == True:
                    inputready,outputready,exceptready \
                      = select.select ([self.sock],[self.sock],[])
                    for input_item in inputready:
                        # Handle sockets
                        data = self.sock.recv(1024)
                        if data:
                            print "Them: " + data
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0
                
    class Text_Input(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
            def run(self):
                while self.running == True:
                  text = raw_input('')
                  try:
                      chat_client.sock.sendall(text)
                  except:
                      Exception
                  try:
                      chat_server.conn.sendall(text)
                  except:
                      Exception
                  time.sleep(0)
            def kill(self):
                self.running = 0

    # Prompt, object instantiation, and threads start here.

    ip_addr = raw_input('What IP (or type listen)?: ')

    if ip_addr == 'listen':
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_server.start()
        text_input = Text_Input()
        text_input.start()
        
    elif ip_addr == 'Listen':
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_server.start()
        text_input = Text_Input()
        text_input.start()
        
    else:
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_client.host = ip_addr
        text_input = Text_Input()
        chat_client.start()
        text_input.start()

if __name__ == "__main__":
    main()



            
