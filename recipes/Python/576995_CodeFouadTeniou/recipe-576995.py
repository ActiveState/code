#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 13/10/09
#version :2.6.1

"""
Code_Fouad_Teniou class uses a function made_key, to  generate a
random key every time you try to encrypt a text, by using FtEncrypt
function and it uses the same key to decrypt the same text by using
the FtDecrypt method.
The metaclass allows a special access to these methods.
"""
import random

class Code_Fouad_Teniou(object):
    """
    Class that represent a code of encryption and decryption
    using a made_key method
    """
    my_list = []
    my_key = []
    my_dict = {}
    
    def made_key(self):
        """
        A method to create a set of values
        and return a random' key 
        """
        
        # select a random number from 1 to infinity 
        ran_number = random.randint(1,99)

        # create a random set based on the first number you chose       
        set = xrange(ran_number,28*ran_number,ran_number)

        # increase the value of every number in the set        
        for item in set:
            item += 3
            Code_Fouad_Teniou.my_key.append(item)

        #return a random key         
        return Code_Fouad_Teniou.my_key

    def FtEncrypt(self,text):
        """ Encrypt a text into a list of values """
        
        self.text = text
        EncryptText = []
        characters = "abcdefghijklmnopqrstuvwxyz "

        #attempt to append my_list and update my_dict
        #using a random set of alphabet and a random made_key         
        try:
            for char in random.sample(characters,27):
                Code_Fouad_Teniou.my_list.append(char)
           
            Code_Fouad_Teniou.my_dict.update(zip(Code_Fouad_Teniou.my_key,Code_Fouad_Teniou.my_list))

            for item in text.lower():
                for i in Code_Fouad_Teniou.my_dict.items():
                    if item == i[1]:
                        EncryptText.append(i[0])
                    
            return EncryptText
        
        #Raise AttributeError if text is not a string 
        except AttributeError:
            raise AttributeError, "\n<Please re-enter your text as a 'string'"
        
    def FtDecrypt(self,EncryptText):
        """ Decript a list of values into the orginal text """
     
        self.EncryptText = EncryptText
        characters = "abcdefghijklmnopqrstuvwxyz "
        DecripText = ''

        #attempt to decrypt the text using the made_key and EncryptText        
        try:
            for item in self.EncryptText:
                DecripText += Code_Fouad_Teniou.my_dict[item]

            return DecripText
        
        #Raise KeyError if a different key was used to encrypt the text 
        except KeyError:
            print "\n<Please use the right code(made_key) to decrypt your text"
    
# Allowing Access of class Code_Fouad_Teniou Methods
def Method_Access(function):
    """ Attempted operation to access a function """
    
    pass

class AccessMeta(type):
  
    def __new__(cls,names,bases,namespaces):

        for item in bases:
            if isinstance(item,AccessMeta):
                pass 

            else:                
                for code in namespaces['code_steps']:
                    if code in namespaces:
                        pass
                    
                    else:
                        namespaces[code] = Method_Access(getattr(item,code))
        
        return super(AccessMeta,cls).__new__(cls,names,bases,namespaces)

class Access:
    __metaclass__ = AccessMeta

if __name__ == "__main__":
  
    class AccessAppend(Access,Code_Fouad_Teniou):
        cft = Code_Fouad_Teniou()
        code_steps = "made_key FtEncrypt FtDecrypt ".split()
  
    AccessAppend().cft.made_key()
    
    encrypt =  AccessAppend().cft.FtEncrypt('hello world')
    print encrypt
    
    decrypt = AccessAppend().cft.FtDecrypt(encrypt)
    print decrypt
    
#######################################################################
