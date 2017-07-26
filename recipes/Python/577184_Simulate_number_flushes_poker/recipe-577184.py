import time
import random
#deal poker hand and see if you get a flush
print "This simulates poker hands"

flush=0
n=int(raw_input("no of hands="))
t1=time.clock() #start the clock ticking
for i in range(n):#deal n hands
	count1=count2=count3=count4=0 # set counters to zero
	for i in range(0,5):#deal 5 cards
		card=random.choice(['ace',2,3,4,5,6,7,8,9,10,'jack','queen','king'])
		#but what suit is it?
		suit=random.choice(['spades','diamonds','hearts','clubs'])
		if suit=='spades':      
                        count1+=1
		elif suit=="diamonds":
                        count2+=1
                elif suit=="hearts":
                        count3+=1
                elif suit=="clubs":
                        count4+=1
		#print card, suit,count1,count2,count3,count4,flush
                #print "---------------------"		
                if count1==5 or count2==5 or count3==5 or count4==5:
                   flush=flush+1   
print "number of flushes=",flush
t2=time.clock()#stop the clock
process=round(t2-t1,2)#time it took to process commands

prob=float(flush)/float(n) #the probability of getting a flush
print "prob of flush=",prob

print "processor time=",process,
print "secs"
