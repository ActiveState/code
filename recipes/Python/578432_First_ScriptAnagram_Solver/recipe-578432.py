import sys
import Tkinter
from string import *
def Load_WordList():
    wordList = open("wordlist.txt", "r")
    wStr = wordList.read()
    wList = split(wStr,"\n")
    return wList
def compare(x,y):
    x1=0
    x2=0
    y1= []
    y2= []
    j = ''
    k = ''
    for i in x:
        x1 = ord(i)
        y1.append(x1)
    for i in y:
        x2 = ord(i)
        y2.append(x2)
    y1.sort(key=int)
    y2.sort(key=int)
    for a in y1:
        j += str(a)
    for a in y2:
        k += str(a)
    if j == k:
        return 1
    else:
        return 0
def Unscramble(Gword,Wlist):
    answer = str()
    for i in Gword:
        for wl in Wlist:
            Solved = compare(i,wl)
            if Solved == 1:
                answer += wl + ","
                break
    return answer       
#b = Load_WordList()
def Clipboard(CopyPaste):
    global winner
    if CopyPaste == 'Paste':
        words = []
        root = Tkinter.Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.destroy()
        text = split(text)
        return text
    if CopyPaste == 'Copy':
        root = Tkinter.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(winner)
        root.destroy
        
def main():
    global winner
    wordnn = Clipboard('Paste')
    wordnm = Load_WordList()
    winner = Unscramble(wordnn,wordnm)
    winner = winner[:-1]
    print "Succesfully Unscrambled and Automatically Coppied to Clipboard"
    Clipboard('Copy')
def intro():
    print "Welcome to Garen's Anagram Solver",
    print "\n\nPlease copy the words to the clipboard from Hackthissite and then press enter, \n\nThen the words will be unscrambled\n\n",
    print "Then Automatically coppied back onto your clipboard \n\nwhere you may paste them back into the site\n\nThank you for using Garen's Anagram Solver!\n\n"
    raw_input("<--Press any key to unscramble-->")
    main()
intro()
