def first2lines(): return str(('#' * 80) + '\n' + '#' + (' ' * 78) + '#') # first two lines
def leftSide(): return '# '                                               # left side of border
def rightSide(): return ' #'                                              # right side of border
def last2lines(): return str('#' + (' ' * 78) + '#' + '\n' + ('#' * 80))  # last two lines

# user entered comment goes here
uec = "This program will neatly format a programming comment block so that it's surrounded by pound signs (#). It does this by splitting the comment into a list and then concatenating strings each no longer than 76 characters long including the correct amount of right side space padding."

if len(uec) > 0:
    eosm = '<<<EOSM>>>'                                   # end of string marker
    comment = ' '.join((uec, eosm))
    wordList = comment.split()                            # load the comment into a list
    tmpString = ''                                        # temporarily holds loaded elements
    loadComment = ''                                      # holds the elements that will be printed
    counter = 0                                           # keeps track of the number of elements/words processed
    space = 0                                             # holds right side space padding
    last = wordList.index(wordList[-1])                   # numerical position of last element

    print first2lines()
    for word in wordList:
        tmpString += word + ' '                           # load the string until length is greater than 76

        # processes and prints all comment lines except the last one
        if len(tmpString.rstrip()) > 76:
            tmpList = tmpString.split()
            tmpString = tmpList[-1] + ' '                 # before popping last element load it for the beginning of the next cycle
            tmpList.pop()
            for tmp in tmpList:
                loadComment += tmp + ' '
            loadComment = loadComment.rstrip()
            space = 76 - len(loadComment)
            print leftSide() + loadComment + (space * ' ') + rightSide()
            loadComment = ''

        # processes and prints the last comment line
        elif len(tmpString.rstrip()) <= 76 and counter == last:
            tmpList = tmpString.split()
            tmpList.pop()
            for tmp in tmpList:
                loadComment += tmp + ' '
            loadComment = loadComment.rstrip()
            space = 76 - len(loadComment)
            print leftSide() + loadComment + (space * ' ') + rightSide()

        counter += 1
    print last2lines()

else:
    print first2lines()
    print leftSide() + "The length of your comment is zero, it must be at least one character long. " + rightSide()
    print last2lines()
