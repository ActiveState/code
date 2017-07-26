## Generate a human readable 'random' password
## password  will be generated in the form 'word'+digits+'word' 
## eg.,nice137pass
## parameters: number of 'characters' , number of 'digits'
## Pradeep Kishore Gowda <pradeep at btbytes.com >
## License : GPL 
## Date : 2005.April.15
## Revision 1.2 
## ChangeLog: 
## 1.1 - fixed typos 
## 1.2 - renamed functions _apart & _npart to a_part & n_part as zope does not allow functions to 
## start with _

def nicepass(alpha=6,numeric=2):
    """
    returns a human-readble password (say rol86din instead of 
    a difficult to remember K8Yn9muL ) 
    """
    import string
    import random
    vowels = ['a','e','i','o','u']
    consonants = [a for a in string.ascii_lowercase if a not in vowels]
    digits = string.digits
    
    ####utility functions
    def a_part(slen):
        ret = ''
        for i in range(slen):			
            if i%2 ==0:
                randid = random.randint(0,20) #number of consonants
                ret += consonants[randid]
            else:
                randid = random.randint(0,4) #number of vowels
                ret += vowels[randid]
        return ret
    
    def n_part(slen):
        ret = ''
        for i in range(slen):
            randid = random.randint(0,9) #number of digits
            ret += digits[randid]
        return ret
        
    #### 	
    fpl = alpha/2		
    if alpha % 2 :
        fpl = int(alpha/2) + 1 					
    lpl = alpha - fpl	
    
    start = a_part(fpl)
    mid = n_part(numeric)
    end = a_part(lpl)
    
    return "%s%s%s" % (start,mid,end)
    
if __name__ == "__main__":
    print nicepass(6,2)      
