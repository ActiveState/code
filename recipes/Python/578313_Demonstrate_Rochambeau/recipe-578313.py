'''
demonstrate Stone, Stainless, Paper game
Created on 2012-11-1

@author: Eric
'''
import random;
                          #elementA-->DRAW  WIN      LOST  
COMPETE_RESULT = {"Stone":["Stone", "Stainless", "Paper"],
                                "Stainless":["Stainless", "Paper", "Stone"],
                                "Paper":["Paper", "Stone", "Stainless"]};
SIGN = {0:"Stone", 1:"Stainless", 2:"Paper"}
RESULTS = {0:"DRAW", 1:"WIN", 2:"LOST"};

def rochambeauGame():
    print('''0:STONE
1:STAINLESS
2:Paper
3:quit
''');
    while True:
        userSign = input("please input your userSign number:");
        if int(userSign) in (0,1, 2, 3):
            if int(userSign) == 3:
                exit();
            else:
                userSignResults = COMPETE_RESULT[SIGN[int(userSign)]];
                pcSign = SIGN[int(genereteRandomPCSign())];
                print("User Sign:" + SIGN[int(userSign)] + " PC Sign:" + pcSign + " \n####result is: user " + RESULTS[userSignResults.index(pcSign)]);
        else:
            print("please input correctly order");
#generate a random number,[0,2]
def genereteRandomPCSign():
    return random.randrange(3);

if __name__ == '__main__':
    rochambeauGame();
