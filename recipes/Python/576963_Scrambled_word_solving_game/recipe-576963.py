print "Rules"
print "\n"
print "This is how the game works..."
print "The game will give you a scrambled word. Then you 'guess' the original."
print "\n"
print "A couple of notes."
print "______________________________"
print "1: all words are never plural."
print "2: c() gives you the first letter."
print "3: s() surrenders. This also gives you the answer."

import random
def eq(str1, str2):
    str1=list(str1)
    str1.sort()
    str2=list(str2)
    str2.sort()
    if str1==str2:
        return True
    else:
        return False

word=["jazz", "quiz", "cozy", "whizz", "audio", "dark", "age", "sage", "silly", "fight", "flight", "kill", "queue", "queen", "crazy", "cab", "back", "stop", "ale", "soup", "pea", "mourn", "gym"]
while word==True:
    num=0
    printfa=True
    pick=random.choice(word)
    correct=pick
    pick=list(pick)
    while word==True: 
        random.shuffle(pick)
        if pick not in word:
            break
    a=len(correct)-2
    while True:
        print "\n"
        answer=raw_input("".join(pick)+": ")
        if eq(answer, correct) and answer in word:
            print "\n"
            print "You Win!"
            printfa=False
            break
        elif answer=="s()":
            break
        elif answer=="c()":
            print "\n"
            print "first letter: "+correct[0]
        else:
            print "\n"
            print "incorrect!"
            num+=1
            if num==a:
                break
            else:
                continue
    word.remove(correct)
    if printfa==True:
        print "________________"
        print "Ran out of tries"
        print "The correct answer was: "+correct
print "\n"
print "Sorry, no more words left!"
time.sleep(4)
