class Obfuscator:
	""" A simple obfuscator class using repeated xor """

    def __init__(self, data):

        self._string = data

    def obfuscate(self):
        """Obfuscate a string by using repeated xor"""

        out = ""
        
        data = self._string
        
        a0=ord(data[0])
        a1=ord(data[1])
        
        e0=chr(a0^a1)
        out += e0
        
        x=1
        eprev=e0
        while x<len(data):
            ax=ord(data[x])
            ex=chr(ax^ord(eprev))
            out += ex
            #throw some chaff
            chaff = chr(ord(ex)^ax)
            out += chaff
            eprev = ex
            x+=1

        return out
        
    def unobfuscate(self):
        """ Reverse of obfuscation """

        out = ""
        data = self._string
        
        x=len(data) - 2
        
        while x>1:
            apos=data[x]
            aprevpos=data[x-2]

            epos=chr(ord(apos)^ord(aprevpos))
            out += epos
        
            x -= 2

        #reverse string
        out2=""
        x=len(out)-1
        while x>=0:
            out2 += out[x]
            x -= 1

        out=out2
    
        #second character
        e2=data[2]
        a2=data[1]
        
        a1=chr(ord(a2)^ord(e2))
        a1 += out
        out = a1
    
        #first character
        e1=out[0]
        a1=data[0]
        
        a0=chr(ord(a1)^ord(e1))
        a0 += out
        out = a0
        
        return out

def main():
   
    testString="Python obfuscator"
    obfuscator = Obfuscator(testString)
    testStringObf = obfuscator.obfuscate()
    print testStringObf

    obfuscator = Obfuscator(testStringObf)
    testString = obfuscator.unobfuscate()
    
    print testString
    

if __name__=="__main__":
    main()
