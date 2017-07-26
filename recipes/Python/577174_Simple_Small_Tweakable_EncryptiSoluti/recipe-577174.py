"""
SimpleCrypt.py REV 3
Author: A.J. Mayorga
Date: 04/2010

Changelog:
    - 04/30/2010    Added Reinitialization method for change crypto params on the fly
    - 04/30/2010    Added a HMAC method for help with socket coms

SimpleCrypt development goals:
    - Import as few modules as possible minimize dependecies
    - No importing of non native python (2.6) modules 
    - No ctype calls
    - Implement to be easy to understand.
    - Allow for an abundance of tweaking.
    - Keep the internals straight forward and as simple as possible
      while still providing a solid encryption framework.
    
     
Algorithm Features:
    - Keys:
        - User provided key is used to generate a series of internal keys the number
          of which depend on the number of encryption cycles desired more 
          cycles = more entropy

        - Key magnitude can be set to determine the complexity of internally
          derived cycle keys.
          
        - Cycle keys are applied to the cycle data in a ring buffer fashion
          rather than byte for byte
      
        - Each cycle key is initialized at a different start byte than the other
          cycle keys which is determined by a combination of the derived cycle key
          and the KEY_ADV value.

        
    - Cycles (a cycle is a single pass of encryption or decryption over the data)
        - Variable number of cycles allows for fine tuning of entropy vs. speed
        
        - Each cycle uses a different data shift (initialization vector) on the 
          cycle data to determine at what byte to start
          
    - Blocks
        - provided two different methods for handling larger volumes of data
    
    - Size and padding
        - Does not pad the cipher data, the resulting cipher is the same size
          as the plaintext data. Cipher data is in raw binary (hex values here
          are for easy viewing of samples)
      
      
Essentially SimpleCrypt gives you a framework in which to encrypt your data
options are easy to use and the algorithm is easy to recreate in other languages 
C/C++, .NET and others

so if you work with custom multi-languaged solutions, encrypt files, need to 
create your own encrypted sockets or just want the ability to tweak everything
without having to delve deep in the math this can be an easy single class 
solution for getting the job done.

As always constructive critiques are always welcomed and desired if anyone can 
point out a weakness in the algorithm Ive provided the below hexed
cipher, please show me how you would crack it, Id really love to see how you did
it. Enjoy!

CRACK ME:
d55eacd6fdee9543b1b30140a98d23f9c9e03fc66cbe8a8b17b07bade9b6d9dfa03ed2dda650412dbb14a256d86cbb41c4eda61f8cf2


"""



from hashlib import sha1
from array import array


class SimpleCrypt:
   
    
    def __init__(self, INITKEY, DEBUG=False, CYCLES=3, 
                 BLOCK_SZ=126, KEY_ADV=0, KEY_MAGNITUDE=1):
        
        self.cycles         = CYCLES
        self.debug          = DEBUG
        self.block_sz       = BLOCK_SZ
        self.key_advance    = KEY_ADV
        self.key_magnitude  = KEY_MAGNITUDE
        
        self.key            = self.MSha(INITKEY)
        self.eKeys          = list()
        self.dKeys          = list()
        self.GenKeys()

    
    """
    Short hash method
    """
    def MSha(self, value):
        try:
            return sha1(value).digest()
        except:
            print "Exception due to ", value
            return None

      
    """
    Short hexed hash method
    """
    def MShaHex(self, value):
        try:
            return sha1(value).digest().encode('hex')
        except:
            print "Exception due to ", value
            return None

      
    """
    Sets the start byte of a cycle key
    """
    def KeyAdvance(self, key):
        k = array('B', key)   
        for x in range(self.key_advance):
            k.append(k[0])
            k.pop(0)
        return k
     
    
    """
    Sets the complexity & size of a cycle key
    based off the hash of the original supplied key
    """  
    def SetKeyMagnitude(self, key):
        k = array('B', key)
        for i in range(self.key_magnitude):
            k += array('B', sha1(k).digest()) 
            k.reverse()
        k = self.KeyAdvance(k)
        
        return k
   
  
    """
    Generate our encryption and decryption cycle keys based off of the number 
    of cycles chosen & key magnitude
    """
    def GenKeys(self):
        k = array('B', self.key)
        self.eKeys  = list()
        self.dKeys  = list()
        
        for c in range(self.cycles):
            k = sha1(k).digest()
            self.eKeys.append(self.SetKeyMagnitude(k))
            self.dKeys.append(self.SetKeyMagnitude(k))
        self.dKeys.reverse()
       
    
    """
    Allow for reinitialization of parameters for on the fly changes
    """
    def ReInit(self, ARGS):
        #(Default,New Value)[ARGS.has_key('VALUE')] #True == 1

        self.key         = (self.key,self.MSha(ARGS.get('Key')))[ARGS.has_key('Key')]
        self.cycles      = (self.cycles,ARGS.get('Cycles'))[ARGS.has_key('Cycles')]
        self.block_sz    = (self.block_sz,ARGS.get('BlockSz'))[ARGS.has_key('BlockSz')]
        self.key_advance = (self.key_advance,ARGS.get('KeyAdv'))[ARGS.has_key('KeyAdv')]
        
        self.GenKeys()


  
    """
    Set a start vector (initialization vector) of our data in a cycle
    the iv is determined by the first byte of the cycle key and the cycle mode
    aka cmode and will be different each cycle since a different key is used each
    cycle.
    
    Also the direction of or rather how the iv value is set depends on the cmode
    as well forward for encryption and backward for decryption.  
    """  
    def SetDataVector(self, data, params):
        vdata   = array('B', data)
        cmode   = params[0]
        cycle   = params[1]
        iv      = 0
          
        if   cmode == "Encrypt":
            iv    = array('B', self.eKeys[cycle])[0]
        elif cmode == "Decrypt":
            iv    = array('B', self.dKeys[cycle])[0]
            
        for x in range(iv):
            if  cmode == "Encrypt":
                vdata.append(vdata[0])
                vdata.pop(0)
            elif cmode == "Decrypt":
                v = vdata.pop(len(vdata)-1)
                vdata.insert(0,v)
        
        if self.debug:
           print "IV: ",iv
           print "SetDataVector-IN:\t",data.tostring().encode('hex')
           print "SetDataVector-OUT:\t",vdata.tostring().encode('hex'),"\n"
        
        return vdata
    
      
    """
    Here the cycle key is rolled over the data(Xor). Should the 
    data be longer than the key (which most times will be the case) the the first
    byte of the cycle key is moved to the end the key and is used again 
    Think ring buffer
     
    """
    def Cycle(self, data, params):
        keyplaceholder  = 0 
        dataholder      = array('B')
        cycleKey        = array('B')
        cmode           = params[0]
        cycle           = params[1]
        
        if cmode == "Encrypt":
            cycleKey    = array('B', self.eKeys[cycle])
        elif cmode == "Decrypt":
            cycleKey    = array('B', self.dKeys[cycle])
        
        if self.debug:
            print "CYCLE-KEY        :\t",cycleKey.tostring().encode('hex')
        
        for i in range(len(data)):
            dataholder.append(data[i] ^ cycleKey[keyplaceholder])
            if keyplaceholder == len(cycleKey)-1:
                keyplaceholder = 0
                cycleKey.append(cycleKey[0])
                cycleKey.pop(0)       
            else:
                keyplaceholder += 1
        
        if self.debug:
            print cmode+"Cycle-"+str(cycle),"-IN :\t",data.tostring().encode('hex')
            print cmode+"Cycle-"+str(cycle),"-OUT:\t",dataholder.tostring().encode('hex'),"\n"
        
        return dataholder
    
  
    """
    Core element bring together all of the above for encryption
    *NOTE - trying to shove larger amounts of data in here wil give you issues
    call directly for strings or other small variable storage
    for large data blocks see below
    """
    def Encrypt(self, data):    
        data        = array('B', data)
        for cycle in range(self.cycles):
            params  = ("Encrypt", cycle)
            data    = self.Cycle(self.SetDataVector(data, params), params)      
            
        return data.tostring()
          
  
    """
    Generator using previous encrypt call, but in a sensible way for large
    amounts of data that will be broken into blocks according to the set
    BLOCK_SZ.  
    """
    def EncryptBlock(self, bdata):
        while True:            
            block = bdata[:(min(len(bdata), self.block_sz))]
            if not block:
                break
            bdata = bdata[len(block):]
            yield self.Encrypt(block)
       

    """
    Generator widget for easily encryption files
    """
    def EncryptFile(self, FileObject):
        while True:
            data = FileObject.read(self.block_sz)
            if not data:
                break
            yield self.Encrypt(data)
           
        
    """
    Core of decryption
    """
    def Decrypt(self, data):
        data        = array('B', data)

        for cycle in range(self.cycles):
            params  = ("Decrypt", cycle)
            data    = self.SetDataVector(self.Cycle(data, params), params)
        
        return data.tostring()
    
  
    """
    Generator decrypt large block data
    """  
    def DecryptBlock(self, bdata):
        while True:
            block = bdata[:(min(len(bdata), self.block_sz))]
            if not block:
                break
            bdata = bdata[len(block):]
            yield self.Decrypt(block)
          
        
    """
    Generator widget for file decryption
    """ 
    def DecryptFile(self, FileObject):
        while True:
            data = FileObject.read(self.block_sz)
            if not data:
                break
            yield self.Decrypt(data)
           
    
    """
    HMAC "ish" widget primarily for use with sockets, hashing key to data
    helps ensure data integrity and authentication, do it this way to stay
    lean rather than import another module
    """
    def GenHMAC(self, data):
        hmac = sha1(self.key.encode('hex')+data.encode('hex')).hexdigest()
        return hmac
 
 
if __name__ == '__main__':       
            
    
    ############################################################################
    # Usage Example this is not the crackme cipher in the above comment
    
    
    key     =  "My Secret Key Blah Blah Blah"
    plain   =  "THIS IS MY MESSAGE AND STUFF AND JUNK I WANT TO HIDE ABC123 "
    cipher  =  ""
    dcrypt  =  ""
    text    =  "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do"
    text    += " eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut"
    text    += " enim ad minim veniam, quis nostrud exercitation ullamco laboris"
    text    += " nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor"
    text    += " in reprehenderit in voluptate velit esse cillum dolore eu fugiat"
    text    += " nulla pariatur. Excepteur sint occaecat cupidatat non proident,"
    text    += " sunt in culpa qui officia deserunt mollit anim id est laborum."

    print "PLAIN TXT          :\t",plain,"  SZ:",len(plain)
    print "PLAIN KEY          :\t",key
   
    #Create Two Instances That Will Pass Back And Forth Data Must Have Same init values of course
    #Block_SZ wont matter unless your calling the larger data handling methods
    
    crypt1 =  SimpleCrypt(INITKEY=key, DEBUG=True, CYCLES=3, BLOCK_SZ=25, KEY_ADV=5, KEY_MAGNITUDE=1)
    crypt2 =  SimpleCrypt(INITKEY=key, DEBUG=True, CYCLES=3, BLOCK_SZ=25, KEY_ADV=5, KEY_MAGNITUDE=1)
    
    #SIMPLE DATA ENCRYPTION TEST ! NOT SUITABLE FOR LARGE VOLUMES -USE BELOW
    cipher = crypt1.Encrypt(plain) 
    dcrypt = crypt2.Decrypt(cipher)
    
    """
    #TEST FOR ENCRYPTING LARGER AMOUNTS OF DATA
    
    plain = text*20
    
    crypt.block_sz = 50
    for c in crypt1.EncryptBlock(plain):
        print "BLOCK:                \t",c.encode('hex')
        cipher += c

    #Here you could Base64 or Hex encode and pump through a socket
    #Careful Base64 is smaller than Hex but python base64.encodestring()
    #adds newline chars "\n", So use something like cipher = cipher[:-1]
    #before sending on socket else will corrupt the cipher on the otherside.
    
    for d in crypt2.DecryptBlock(cipher):
        dcrypt += d
        
    """
    
    """
    #TEST FOR ENCRYPTING FILES - VIEW ACTUAL FILES FOR RESULTS
    import os
    if not os.path.exists("test.txt"):
        fp = open("test.txt", "wb+") #Make sure to use rb or wb for binary files 
        fp.write(text*1024)
        fp.close()
        
    fp0 = open("test.txt", "rb+")
    fp1 = open("cipher.txt", "wb+")
    
    crypt.block_sz = 256
    for cipher in crypt1.EncryptFile(fp0):
        fp1.write(cipher)
    fp0.close()
    fp1.close()
    
    fp2 = open("cipher.txt", "rb+")
    fp3 = open("decrypted.txt", "wb+")
        
    for decrypt in crypt2.DecryptFile(fp2):
        fp3.write(decrypt)    
    
    fp2.close()
    fp3.close()
    """
    
    
    print "CIPHER TXT         :\t",cipher.encode('hex'),"  SZ:",len(cipher),"\n\n"
    print "#"*99,"\n\n"
    print "PLAIN TXT          :\t",plain,"\t",sha1(plain).digest().encode('hex')
    print "DECRYPT TXT        :\t",dcrypt,"\t",sha1(dcrypt).digest().encode('hex')
    
    
