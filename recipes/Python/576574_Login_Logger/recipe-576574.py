#!/usr/bin/python

############## Listenserver  Program 1 ################

import socket
import MySQLdb


class Server:


''' change your database parameters  '''
######################################## Create a default connection #####################################

    def createDefCon(self):

                try:
                        host = "127.0.0.1"
                        port = 3306         ### default mysql port, change if you know better
                        user = "krisk"      ### def parameters
                        passwd = "kish"     ### def parameters
                        db = "loginfo"      ### connection.user_info contains the autho users

                        ### Create a connection object, use it to create a cursor

                        con = MySQLdb.connect(host = host  ,port = port , user = user,passwd = passwd ,db = db)
                        return con ### returns a connection object

                except: 
                        return 0;



####################################### Test connection #######################################################



    def __init__(self, port):
        "Binds the server to the given port."

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(port)

        #Queue up to five requests before turning clients away.
        self.socket.listen(5)
	
	
    def run(self):
        "Handles incoming requests forever."
        con = self.createDefCon()
        cursor = con.cursor()
        
        while True:
            request, client_address = self.socket.accept()
            
            #Turn the incoming and outgoing connections into files.
        
            input = request.makefile('rb', 0)
            output = request.makefile('wb', 0)
            try:
    
                     l = input.readline().strip()
		     print l
		     sql='''insert into  log_info(`ip`,`uname`) values('%s','%s');''' % (client_address[0],l  )
		     print sql
		     cursor.execute(sql);
		      	
                     request.shutdown(2) #Shut down both reads and writes.
            
             except socket.error:
    	             #Most likely the client disconnected.
                     sys.exit(1)

if __name__ == '__main__':

    import sys
    if len(sys.argv) < 3:
        print 'Usage: %s [hostname] [port number]' % sys.argv[0]
        sys.exit(1)
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    Server((hostname, port)).run()



################## TellServer  Program 2 #######################
#!/usr/bin/python


import socket



class Client:



        "A client for the mirror server."
        def __init__(self, server, port):
            "Connect to the given mirror server."
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server, port))
       
        def mirror(self, s):
        	    "Sends the given string to the server, and prints the response."
        	    self.socket.send(s)


        def close(self):
    	    self.socket.send('\r\n') #We don't want to mirror anything else.
    	    self.socket.close()

if __name__ == '__main__':



    import sys


    if len(sys.argv) < 4:
        print 'Usage: %s [host] [port] [text to be mirrored]' % sys.argv[0]
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    toMirror = sys.argv[3]
    
    m = Client(hostname, port)
    m.mirror(toMirror)
    m.close()



##################### Infogather Script 1 ###########################
##!/bin/bash

##This program tells the server about the login
## It carries the timestamp and the user info


## change the localhost to the address of your server and the port as it may be
## the case

#python /usr/bin/infosendingclient.py localhost 2000 $USER 
