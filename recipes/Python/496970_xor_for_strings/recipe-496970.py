class Xor:
    def __init__(self, key):
        self.__key = key
        
    def __xor(self, s):
        res = ''
        for i in range(len(s)):
            res += chr(ord(s[i]) ^ ord(self.__key[i]))
        return res
            
        
    def __normkey(self, s):
        self.__key = self.__key * (len(s) / len(self.__key))
        
    def encrypt(self, s):
        self.__normkey(s)
        return self.__xor(s)
        
    decrypt = encrypt
