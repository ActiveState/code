import time, hashlib, base64
from array import array
from SimpleCrypt import SimpleCrypt

"""
SimpleCryptSockeExt

Author: AJ Mayorga            
Date:   4/30/2010

Having posted SimpleCrypt http://code.activestate.com/recipes/577174/ I wanted
to follow with an implementation example, specifically for use in Client/Server
solutions and keep it simple and as close to a drop-in solution as possible.

Design Goals:
    - Create a generic SimpleCrypt wrapper for use in solutions such as:
        - HTTP,RAW,FTP,DNS,etc
        
    - Support TCP or UDP 
        - Internal checking of data integrity and error recovery
        
    - Demonstrate various implementations for SALTing encrypted data streams
        - SimpleCrypt allows for not only SALTing key values
          but algorithm configuration as well

Enjoy, as always feedback welcome

"""
class SimpleCryptSocketExt(SimpleCrypt):
    
    def __init__(self, kwargs):
        SimpleCrypt.__init__(self, **kwargs)
        self.name  = str(self.__class__).split(".")[1]
                    
        self.SeedValues      = ["Iliana","Chandra","Elspeth", "Sorrin", "Bob"]
        self.SeedData        = ""
        self.salt_method     = None
        self.idx             = 0
        self.Counter         = 0
        self.Debug           = False
        self.Errors          = 0
        self.MaxRetries      = 3
        self.HMAC            = ""
        self.BlockEndMarker  = "ZZ"
    
          
    def Encode(self, data, mode="Hex"):
        if mode == "Hex":
            return data.encode('hex')
        elif mode == "B64":
            return base64.b64encode(data)
        

    def Decode(self, data, mode="Hex"):
        if mode == "Hex":
            return data.decode('hex')
        elif mode == "B64":
            return base64.b64decode(data)
        
        
    def ShowInitVars(self, label):
        label = label.upper()
        print "\n","#"*80,"\n"
        print label," Key:      ",self.key.encode('hex')
        print label," Cycles:   ",self.cycles
        print label," BlockSz:  ",self.block_sz
        print label," KeyAdv:   ",self.key_advance
        print label," KeyMag:   ",self.key_magnitude
        print label," SeedData: ",self.Encode(self.SeedData),"\n"
    
        if label.find("ENCRYPT") != -1:
            for idx in range(len(self.eKeys)):
                print label," eKey",idx,":  ",self.eKeys[idx].tostring().encode('hex')
        elif label.find("DECRYPT") != -1:
            for idx in range(len(self.dKeys)):
                print label," dKey",idx,":  ",self.dKeys[idx].tostring().encode('hex')
        print label," HMAC   :  ",self.HMAC     
        print "\n","#"*80,"\n"
        
        
    
    """
    Method that salts SimpleCrypt vars according to preset
    seed values and preset routines, overtime this implementation can prove
    predictable.
    """    
    def SimpleSalt(self):
        self.idx        = (self.idx+1,0)[self.idx>=len(self.SeedValues)-1]
        key             = self.key+self.SeedValues[self.idx]+str(self.Counter)
        ARGS            = dict()
        ARGS['Key']     = sha1(key).digest()
        self.Counter    += 21+len(self.SeedValues[self.idx])
        self.ReInit(ARGS)

    """
    Implementation that salts the SimpleCrypt vars according to time values
    this demo is set to change keys every min, for everyday of the year.
    this implementation works really well, but only if you have a good NTP setup
    """    
    def NTPSalt(self):
        year,month,day,hour,minute,sec,wday,yday,dst = time.localtime()
        key             = self.key+str(self.Counter)
        ARGS            = dict()
        ARGS['Key']     = ''.join([str(x) for x in (self.key,year,month,day,hour,min)])
        ARGS['Cycles']  = max(wday+1, 3)
        ARGS['BlockSz'] = month*128
        ARGS['KeyAdv']  = yday    
        ARGS['KeyMag']  = min(int(ARGS['Cycles']/2)+1, ARGS['Cycles'])
        self.Counter    += 21+sec+yday-min
        self.ReInit(ARGS)
              
    """
    Method to salt SimpleCrypt vars using previous data, this definately is the
    most ideal way (IMHO) 
    """   
    def PreviousDataSalt(self):
        SeedHash = sha1(self.SeedData).hexdigest()
        
        idx = 2
        v1 = ord(SeedHash[idx-2:idx].decode('hex')); idx += 10
        v2 = ord(SeedHash[idx-2:idx].decode('hex')); idx += 2
        v3 = ord(SeedHash[idx-2:idx].decode('hex')); idx += 1
        v4 = ord(SeedHash[idx-2:idx].decode('hex')); idx += 15
        v5 = ord(SeedHash[idx-2:idx].decode('hex')); idx += 3

        key             = self.key+str(self.Counter)
        ARGS            = dict()
        ARGS['Key']     = sha1(''.join([str(x) for x in (v1,v2,v3)])).digest()
        ARGS['Cycles']  = min(6,v1)
        ARGS['BlockSz'] = max(128,v2)
        ARGS['KeyAdv']  = v4    
        ARGS['KeyMag']  = min(int(ARGS['Cycles']/2)+1, ARGS['Cycles'])
        self.Counter    += 16*(v1*4)-(v3*5)
        self.ReInit(ARGS)
        

    def _Salt(self):
        if self.salt_method == "Simple":
            self.SimpleSalt()
        elif self.salt_method == "NTP":
            self.NTPSalt()
        elif self.salt_method == "PrevData":
            self.PreviousDataSalt()
        elif self.salt_method == None:
            return
        else:
            print "Salt Method Invalid Choose Simple, NTP, PrevData"
   
    """
    Method to override SimpleCrypt Encrypt method so we can
    make it more refined for sockets  
    """           
    def Encrypt(self, plain):
        if self.Debug:
            print "\n\n",self.name," Encrypting :",plain
            self.ShowInitVars("ENCRYPT")
               
        data  = array('B', plain)
        for cycle in range(self.cycles):
            params  = ("Encrypt", cycle)
            data    = self.Cycle(self.SetDataVector(data, params), params)      
      
        ret = data.tostring()
        if self.Debug:
            print "Cipher: ",ret.encode('hex')
    
        self.SeedData = self.MShaHex(plain)
        self.HMAC = self.GenHMAC(ret)
        self._Salt()
            
        return ret
   
       
    """
    override SimpleCrypt Decrypt
    """   
    def Decrypt(self, data):
        if self.Debug:
            print "\n\n",self.name," Decrypting :",self.Encode(data)
            self.ShowInitVars("DECRYPT")
            
        data  = array('B', data)
        for cycle in range(self.cycles):
            params  = ("Decrypt", cycle)
            data    = self.SetDataVector(self.Cycle(data, params), params)
    
        ret = data.tostring()
        if self.Debug:
            print "Plain:  ",ret
            
        self.SeedData = self.MShaHex(ret)
        self._Salt()
        return ret
   
    """
    method to handle receiving blocks of cipher data through
    the passed in socket Object, also checks HMAC
    to ensure data arrived unaltered, bad HMAC prompts
    for resend up to MaxRetries
     
    """
    def RecvData(self, socketObject):
        ret      = False
        data     = socketObject.recv(1024)
        data     = self.Decode(data)
        dataHash = self.GenHMAC(data)
        
        if data.find(self.BlockEndMarker) == -1 or len(data) > 2:   
            data     = self.Decrypt(data)
        else:
            dataHash = self.GenHMAC(data)
      
        socketObject.send(dataHash)
        response = socketObject.recv(1024)
        
        if response == dataHash:
            ret = data
            self.Errors = 0
        else:
            self.Errors += 1
              
        return ret 
       
    """
    handles sending blocks of cipher data confirms receipt via HMAC &
    resend if necessary
    """
    def SendData(self, socketObject, data):
        ret      = False
        dataHash = self.HMAC
        socketObject.send(self.Encode(data))
        response = socketObject.recv(1024)
        
        while self.Errors <= self.MaxRetries:
            if response == dataHash:
                socketObject.send(dataHash)
                ret = True
                break
            else:
                print "BAD HMAC:",response," EXPECTING: ",dataHash
                socketObject.send(data)
                response = socketObject.recv(1024)
                self.Errors += 1
                continue
        self.Errors = 0
        print "SENT:   ",dataHash,"  RECV: ",response
        return ret 
   
   
    """
    Handles receiving messages and reassembles them block by block
    from RecvData 
    """        
    def DataInBound(self, socketObject):
        self.InBoundData = ''
        while True:
            data = self.RecvData(socketObject)
            if data == False:
                continue
            if data.find(self.BlockEndMarker) != -1:
                data = data.replace(self.BlockEndMarker,"")
                if len(data) > 1:
                    self.InBoundData += data
                break
            else:
                self.InBoundData += data
        return True
  
    """
    Disassembles messages and sends them via SendData
    """           
    def DataOutBound(self, socketObject):
        ret = False
        for CipherBlock in self.EncryptBlock(self.OutBoundData): 
            self.SendData(socketObject, CipherBlock)
        self.HMAC = self.GenHMAC(self.BlockEndMarker)
        self.SendData(socketObject, self.BlockEndMarker)
        self.OutBoundData = ''
        return True
    
#######################################################################################


#######################################################################################



import socket, SocketServer, threading

#######################################################################################
# A Class that hold some sort of functionality we will call from the Client
class MyFunctionalClass:
    def __init__(self):
        self.text   =  "\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do\n"
        self.text   += "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut\n"
        self.text   += "enim ad minim veniam, quis nostrud exercitation ullamco laboris\n"
        self.text   += "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor\n"
        self.text   += "in reprehenderit in voluptate velit esse cillum dolore eu fugiat\n"
        self.text   += "nulla pariatur. Excepteur sint occaecat cupidatat non proident,\n"
        self.text   += "sunt in culpa qui officia deserunt mollit anim id est laborum.\n"

    def Parse(self, msg):
        if msg.find("Greetings") != -1:
            return self.text
######################################################################################       


######################################################################################
#Configuration Class subclassing SimpleSocketExt with necesssary vars we will 
#need both the Server and Client will need a copy of this

class SocketCrypto(SimpleCryptSocketExt):
     def __init__(self):
        
        self.CryptoArgs =  dict()
        self.CryptoArgs['INITKEY']       = "My initial key"
        self.CryptoArgs['DEBUG']         = False
        self.CryptoArgs['CYCLES']        = 3
        self.CryptoArgs['BLOCK_SZ']      = 20
        self.CryptoArgs['KEY_ADV']       = 5
        self.CryptoArgs['KEY_MAGNITUDE'] = 1
        
        SimpleCryptSocketExt.__init__(self, self.CryptoArgs)
        
        self.InBoundData    = ""
        self.OutBoundData   = ""
        
        #self.salt_method  = "Simple"
        #self.salt_method  = "NTP"
        #self.salt_method  = "PrevData"
        
    
#####################################################################################            
   
    
#####################################################################################
#Class to handle Server coms overriding BaseRequestHandler handle method      
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler, SocketCrypto):
  
    def handle(self):
        self.name  = str(self.__class__).split(".")[1]
        SocketCrypto.__init__(self)
        self.Debug   = True
        
        MyFuncClass  = MyFunctionalClass()
       
        socketObject = self.request
        if self.DataInBound(socketObject):
            print "SERVER RECEIVED :",self.InBoundData
            self.OutBoundData = MyFuncClass.Parse(self.InBoundData)
            if self.DataOutBound(socketObject):
                print "\nTranfer Success!"
            else:
                print "\nERROR SENDING REPLY TO SENDER"
        else:
            print "\nERROR RECEIVING SENDER DATA"
        
        self.ShowInitVars("SERVER")
      
####################################################################################        


####################################################################################
#Multithreading TCP Server
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
####################################################################################




####################################################################################
####################################################################################
# Example Client Class Subclassing SocketCrypto

class MyClient(SocketCrypto):
    
    def __init__(self, Server, Port):
        SocketCrypto.__init__(self)
        
        self.name  = str(self.__class__).split(".")[1]
        self.Server = Server
        self.Port   = Port
        self.Debug  = True
      
       
    def CallServer(self, Messages):
        ret = ""
        for idx in range(0,len(Messages)):
            sock         = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.Server, self.Port))
            if self.MessagePump(Messages[idx], sock):
                print "Client Call#",idx," Received: ",self.InBoundData,"\n"
            else:
                print "Error Sending Message To Server"
            sock.close()
            SocketCrypto.__init__(self)
        return ret
     
            
    def MessagePump(self, Message, socketObject):
        ret = False
        self.OutBoundData = Message
        if self.DataOutBound(socketObject):
            if self.DataInBound(socketObject):
                print "\nCLIENT  RECV: ",self.InBoundData
                ret = True   
        self.ShowInitVars("CLIENT") 
        return ret    
    
        
####################################################################################
####################################################################################        

if __name__ == '__main__':
    
    HOST, PORT = "localhost", 0

    server          = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread   = threading.Thread(target=server.serve_forever)
    
    server_thread.setDaemon(True)
    server_thread.start()
    
    ip, port = server.server_address
    
    client   = MyClient(ip, port)
    messages = ["Greetings","Greetings","Greetings"]

    client.CallServer(messages)
      
    server.shutdown()
    
  
