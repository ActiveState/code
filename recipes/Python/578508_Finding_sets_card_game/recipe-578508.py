import random

class Table:

    # a random table of n different cards
    def __init__(self,n=12):
        self.cards = random.sample(Card.allcards(),n)
    
    ###############################################
    # four different algorithms that list all sets
    # on the table, from slow to fast
    
    def findsets_gnt(self):     # generate and test
        found = []
        for i,ci in enumerate(self.cards):
            for j,cj in enumerate(self.cards[i+1:],i+1):
                for k,ck in enumerate(self.cards[j+1:],j+1):
                    if ci.isset(cj,ck):
                        found.append((ci,cj,ck))
        return found

    def findsets_gnt_mod(self):   # generate and test (faster)
        found = []
        for i,ci in enumerate(self.cards):
            for j,cj in enumerate(self.cards[i+1:],i+1):
                for k,ck in enumerate(self.cards[j+1:],j+1):
                    if ci.isset_mod(cj,ck):
                        found.append((ci,cj,ck))
        return found
    
    def findsets_simple(self):  # using thirdcard_simple
        found = []
        have = {}
        for pos,card in enumerate(self.cards):
            have[card]=pos
        for i,ci in enumerate(self.cards):
            for j,cj in enumerate(self.cards[i+1:],i+1):
                k = have.get(ci.thirdcard_simple(cj))
                if k > j:  # False if k is None
                    found.append((ci,cj,self.cards[k]))
        return found
        
    def findsets_fast(self):  # using thirdcard_fast
        found = []
        have = [None for _ in range(256)]
        for pos,card in enumerate(self.cards):
            have[card.bits]=pos
        for i,ci in enumerate(self.cards):
            for j,cj in enumerate(self.cards[i+1:],i+1):
                k = have[ci.thirdcard_fast(cj)]
                if k > j:  # False if k is None
                    found.append((ci,cj,self.cards[k]))
        return found
            
class Card:
    
    def __init__(self,*attrs):
        # a card is a simple 4-tuple of attributes
        # each attr is supposed to be either 0, 1 or 2
        self.attrs = attrs
        # alternative representation of attrs, in 8 bits:
        # 2 bits per attr, highest bits represent first attr
        self.bits = sum(a<<(2*i) for i,a in enumerate(attrs[::-1]))
    
    def __eq__(self,other):
        return self.attrs == other.attrs
    
    def __hash__(self):
        return hash(self.attrs)
    
    def __repr__(self):
        return 'Card({})'.format(','.join(self.attrs))
    
    # most readable way to express what a SET is
    def isset(self,card1,card2):
        def allsame(v0,v1,v2):
            return v0==v1 and v1==v2
        def alldifferent(v0,v1,v2):
            return len(set((v0,v1,v2)))==3
        return all(allsame(v0,v1,v2) or alldifferent(v0,v1,v2)
                   for (v0,v1,v2) in zip(self.attrs,card1.attrs,card2.attrs))
    
    # a more mathy (and slightly faster) way
    def isset_mod(self,card1,card2):
        return all((v0+v1+v2)%3==0 for (v0,v1,v2) in zip(self.attrs,card1.attrs,card2.attrs))
    
    # which third card is needed to complete the set
    def thirdcard_simple(self,other):
        def thirdval((v0,v1)):
            return (-v0-v1)%3
        return Card(*map(thirdval,zip(self.attrs,other.attrs)))
    
    # same thing, but using the 8-bit representation
    def thirdcard_fast(self,other):
        # NB returns bits
        x,y = self.bits,other.bits
        xor = x^y
        swap = ((xor & mask1) >> 1) | ((xor & mask0) << 1)
        return (x&y) | (~(x|y) & swap)

    # all 81 possible cards
    @staticmethod
    def allcards():
        return [ Card(att0,att1,att2,att3)
                   for att0 in (0,1,2)
                   for att1 in (0,1,2) 
                   for att2 in (0,1,2)
                   for att3 in (0,1,2)
               ]
               
# bit masks for low and high bits of the attributes        
mask0 = sum(1<<(2*i) for i in range(4))    # 01010101
mask1 = sum(1<<(2*i+1) for i in range(4))  # 10101010
