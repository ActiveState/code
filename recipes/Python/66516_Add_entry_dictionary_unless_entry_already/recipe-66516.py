# say we're building a word->pagenumbers index -- a key piece of code might be:

theIndex = {}
def addword(word, pagenumber):
    if theIndex.has_key(word):
        theIndex[word].append(pagenumber)
    else:
        theIndex[word] = [pagenumber]

# incidentally, a good Pythonic instinct would be to substitute this
# "look before you leap" pattern with a "easier to get permission":

def addword(word, pagenumber):
    try: theIndex[word].append(pagenumber)
    except AttributeError: theIndex[word] = [pagenumber]

# but this is by the by -- just a minor simplification.  However,
# this meets the pattern "use the entry if already present, else
# add a new entry".  Here's how using setdefault simplifies this:

def addword(word, pagenumber):
    theIndex.setdefault(word,[]).append(pagenumber)
