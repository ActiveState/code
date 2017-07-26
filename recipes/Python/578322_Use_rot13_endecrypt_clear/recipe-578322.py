'''
Encryption.Using your solution to the previous problem, and create a "rot13" translator.
"rot13" is an old and fairly simplistic encryption routine where by each letter of the alphabet is
rotated 13 characters. Letters in the first half of the alphabet will be rotated to the equivalent
letter in the second half and vice versa, retaining case. For example, 'a' goes to 'n' and 'X' goes
to 'K'. Obviously, numbers and symbols are immune from translation.
Created on 2012-11-7

@author: aihua.sun
'''
#initialize letters list
LOWER_LETTERS = [chr(x) for x in range(97, 123)];
UPPER_LETTERS = [chr(x) for x in range(65, 91)];

def rot13():
    sourceString = input("Enter string to rot13:");
    resultString = "";
    for char in sourceString:
        if char.isupper():
            resultString += encrypt(char, UPPER_LETTERS);
        elif char.islower():
            resultString += encrypt(char, LOWER_LETTERS);
        else:
            resultString += char;
    print("The rot13 string is:%s" % (resultString));
            
def encrypt(char, letterList):
    resultchar = '';
    originalIndex = letterList.index(char)
    newIndex = originalIndex + 13
    resultchar += letterList[newIndex % len(letterList)]
    return resultchar
    

if __name__ == '__main__':
    rot13();
