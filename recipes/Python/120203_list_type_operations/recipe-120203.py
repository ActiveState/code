#This class can be used to call list methods reverse/sort/extend/append/remove etc
#on list/tuple/strings. As the function of this class return the
#modified sequence instead of modifying them(that anyway it can't do)
#it may be used in map/reduce functions
#functions can be called 
#directly from module NIPSeqMethods (or whatever name u give to this file , btw NIP is not in place)
# e.g NIPSeqMethods.reverse('python')
#or user can import rquired functions e.g
#from NIPSeqMethods import reverse,intersperse,sort
class SeqMethods:
    def __init__(self,funcName=None):
        self.funcName = funcName

    def __call__(self,*args):
        if args:
            #convert to list
            l,t = self.SeqToList(args[0])

            #do list operation                
            ret = apply(getattr(l,self.funcName),args[1:])
            if ret:
                return ret
            
            #convert to seq
            return self.ListToSeq(l,t)
        
    def SeqToList(self,o):
        t = type(o)
        if t in [type(''),type(()),type([])]:
            return list(o),t
        return [],t
    
    def ListToSeq(self,l,t):    
        if t == type(''):
            return ''.join(l)
        if t == type(()):
            return tuple(l)
        return l
    
    def __getattr__(self,name):
        return SeqMethods(name)

    #additional methods
    #this will mix to sequences and create a new sequence
    #whose 1st element is from first list,2nd elem from second list
    #3rd from first and 4th from second list and so on...
    #type of returned seq. = type of first sequence
    def intersperse(self,seq1,seq2):
        l1,t1 = self.SeqToList(seq1)
        l2,t2 = self.SeqToList(seq2)
        if len(l1) < len(l2):
            length = len(l1)
        else:
            length = len(l2)
        #get mixed list
        l = []
        for i in xrange(length):
            l.append(l1[i])
            l.append(l2[i])
        l.extend(l1[length:])
        l.extend(l2[length:])
        return self.ListToSeq(l,t1)
    
thisMod =  __import__(__name__)
sm = SeqMethods()
listMethods = [].__methods__
myMethods = ['intersperse']
#this will add all list type methods and other
#additional methods to module dictionary
for method in listMethods + myMethods:
    thisMod.__dict__[method] = getattr(sm,method)
    
if __name__ == '__main__':
    #examples
    print reverse(intersperse(('a','c','e','g','i'),'bdfh'))
    print map(sort,((2,1,3),(4,3,5)))
    print extend((2,1,3),(4,3,5))
    print remove('python','p')
    print insert('python',1,'A')
