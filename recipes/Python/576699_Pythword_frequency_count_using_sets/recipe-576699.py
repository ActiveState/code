import re

def wordList(text, wordChars = None, ignoreCase = True):
    """converts string simple-mindedly to a list of words"""
    if wordChars is None:
        lcLetters = "abcdefghijklmnopqrstuvwxyz"
        ucLetters = lcLetters.upper()
        otherLegalChars = """-"""
        wordChars = set(lcLetters + ucLetters + otherLegalChars)
    # make sure spaces are always allowed-- they are word boundaries
    wordChars.add(" ")
    # while still a string, convert word boundaries to spaces
    whiteSpace = "\n\r\f\t\v"
    wordBoundaries = whiteSpace + ".,"
    if ignoreCase: text = text.lower()
    li = list(text)
    # drop unwanted chars
    li = [x for x in li if x in wordChars]
    # convert back to string
    text = "".join(li)
    for s in wordBoundaries: text = text.replace(s, " ")
    # need to retain at least one space for word boundaries
    # collapse groups of spaces to a single space
    # Method: replace 64 spaces with a space, 32 spaces with a space, ..., 2 spaces with a space
    for i in [x*x for x in [6,5,4,3,2,1]]: text = text.strip(" " * i)
    # split into list again at word boundaries
    text = text.split(" ")
    # if any "empty words" have been manufactured by previous processes, drop them
    text = [x for x in text if x != ""]
    return text

def reWordList(text, wordChars = None, ignoreCase = True):
    """converts string simple-mindedly to a list of words"""
    if wordChars is None:
        lcLetters = "abcdefghijklmnopqrstuvwxyz"
        ucLetters = lcLetters.upper()
        wordChars = lcLetters + ucLetters
    # make sure spaces are always allowed-- they are word boundaries
    extraWordBoundaries = """.","""
    # convert all word boundaries (white spaces and additional chars specified above) to "spaces"
    rx = re.compile('[\s' + extraWordBoundaries + ']')
    text = rx.sub(" ", text)
    # collapse groups of spaces to a single "space"
    # Method: replace 64 spaces with a space, 32 spaces with a space, ..., 2 spaces with a "space"
    for i in [x*x for x in [6,5,4,3,2,1]]: text = text.strip(" " * i)
    if ignoreCase: text = text.lower()
    li = list(text)
    # drop unwanted chars (which do not delimit words or form a part of them)
    # note "space" is retained
    rx = re.compile("[^" + wordChars + " ]")
    text = rx.sub("", text)
    # split into list at word boundaries
    text = text.split(" ")
    # if any "empty words" have been manufactured by previous processes, drop them
    text = [x for x in text if x != ""]
    return text

def wordFreqs(text, wordChars = None):
    """takes a list of words and returns list of unique words and their frequencies"""
    words = wordList(text, wordChars)
    uniqueWords = set(words)
    return sorted([(word, words.count(word)) for word in uniqueWords])

if __name__ == "__main__":
    # to load a string from a file here, loadFile = True
    loadFile = True
    if loadFile:
        a = list(file(r"d:\partdb.sql"))
        a = "\n".join(a)
    else:
        a = """ Nor again is there anyone who loves or pursues or desires to obtain pain of itself
                because it is pain, but because occasionally circumstances occur in which toil and pain can
                procure him some great pleasure. To take a trivial example, which of us ever undertakes
                laborious physical exercise, except to obtain some advantage from it?"""
    b = wordFreqs(a)
    # example: find integers only
    #b = wordFreqs(a, wordChars = "0123456789")
    print b
    print "\n" * 5
    print "number of words in original: ", len(wordList(a))
    print "Number of unique words: ", len(b)
