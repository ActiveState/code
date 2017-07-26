# This program genereates very simple one dimensional cellular automata
# URL: http://www.stephenwolfram.com/publications/articles/ca/83-cellular/2/text.html
# ALGORITHM:
# Basic Initial List
# Loop:
#       Update the List
#       Print current List
# End


size = 50
list = [0]*size # creates list with all 0's 
list[size/2] = 1 # sets middle element in list to 1

def update(list):
    '''This function updates list based on rule ( left XOR right here )'''
    temp = len(list)*[0]
    n = len(list)
    for i in range(1,n-1):
        temp[i] = list[i-1]^list[i+1]  # list[i] = list[i-1] XOR list[i+1
    return temp

def p(list):
    '''This function prints list with 'A' for 1 and ' ' for 0 value.''' 
    print ''
    for each in list:
        if each ==1:
            print 'A',
        else:
            print ' ',

if __name__=='__main__':
    '''This program generates snoflake pattern'''
    for i in range(size/2):
        p(list)
        list = update(list)
        
