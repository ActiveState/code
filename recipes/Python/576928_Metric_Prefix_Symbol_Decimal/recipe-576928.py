import random
def delete(L,n):
    """returns a list L with value of n deleted"""
    new = []
    for x in L:
    	new.append(x)
    new.remove(n)
    return new
symbol = ["p","n","mu","m","c","d","da","h","k","M","G","T"]
value = [".000000000001",".000000001",".000001",".001",".01",".1","10","100","1000","1000000","1000000000","1000000000000"]
prefix = ["pico","nano","micro","milli","centi","deci","deca","hecto","kilo","mega","giga","tera"]
#12 elements each
print"Please use quotations when entering answers!!!\n"
try:
    while(True):#main loop
        secList = [symbol,value,prefix]
        section = random.choice(secList)
        element = random.choice(range(len(symbol)))
        otherTwo = delete(secList,section)
        
        print "__"+section[element]+"__"

        if(section == symbol):
            print "Value:"
        elif(section == value):
            print "Symbol:"
        else:
            print "Symbol:"
        ansOne = input()
        if(str(ansOne) != otherTwo[0][element]):
            print "Right Answer is "+otherTwo[0][element]

        if(section == symbol):
            print "Prefix:"
        elif(section == value):
            print "Prefix:"
        else:
            print "Value:"    
        ansTwo = input()
        if(str(ansTwo) != otherTwo[1][element]):
            print "Right Answer is "+otherTwo[1][element]+"\n"

        else:
            print "\n"    
        del(symbol[element])
        del(value[element])
        del(prefix[element])
except(IndexError):
    print "Quiz Finished!!\n"
    
