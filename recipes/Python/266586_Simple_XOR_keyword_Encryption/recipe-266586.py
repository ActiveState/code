#PEcrypt - use a string key to encrypt/decrypt another string
#        - Simon Peverett - January 2004

class PEcrypt:
    """
    PEcrypt - very, very simple word key encryption system
              uses cyclic XOR between the keyword character
              bytes and the string to be encrypted/decrypted.
              Therefore, the same function and keyword will
              encrypt the string the first time and decrypt
              it if called on the encrypted string.
    """

    def __init__(self, aKey):
        """
        Initialise the class with the key that
        is used to encrypt/decrypt strings
        """
        self.key = aKey

        # CRC can be used to validate a key (very roughly)
        # if you store the CRC from a previous keyword
        # and then compare with a newly generated one and
        # they are the same then chances are the keyword
        # is correct - only a single byte so not that reliable
        self.crc = 0    
        for x in self.key:
            intX = ord(x)
            self.crc = self.crc ^ intX


    def Crypt(self, aString):
        """
        Encrypt/Decrypt the passed string object and return
        the encrypted string
        """
        kIdx = 0
        cryptStr = ""   # empty 'crypted string to be returned

        # loop through the string and XOR each byte with the keyword
        # to get the 'crypted byte. Add the 'crypted byte to the
        # 'crypted string
        for x in range(len(aString)):
            cryptStr = cryptStr + \
                       chr( ord(aString[x]) ^ ord(self.key[kIdx]))
            # use the mod operator - % - to cyclically loop through
            # the keyword
            kIdx = (kIdx + 1) % len(self.key)

        return cryptStr

if __name__ == "__main__":

    def strToHex(aString):
        hexStr = ""
        for x in aString:
            hexStr = hexStr + "%02X " % ord(x)

        return hexStr
    
    # self test routine

    print "\nTesting PEcrypt!"
    print "----------------\n"

    keyStr = "This is a key"
    testStr = "The quick brown fox jumps over the lazy dog!"

    print "\nString : ", testStr
    print "in hex : ", strToHex(testStr)
    print "key    : ", keyStr

    pe = PEcrypt(keyStr)  # generate the PEcrypt instance
    
    print "\nPEcrypt CRC = %02X" % pe.crc

    testStr = pe.Crypt(testStr)
    print "\nEncrypted string"
    print "Ascii  : ", testStr
    print "Hex    : ", strToHex(testStr)

    testStr = pe.Crypt(testStr)
    print "\nDecrypted string"
    print "Ascii  : ", testStr
    print "Hex    : ", strToHex(testStr)
            
    
