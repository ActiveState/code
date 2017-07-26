import sys, string

# returns a signature that will be the same
# for a whole class of anagrams
def getSignature( item ):
	item_chars = []
	for i in range(len(item)):
		item_chars.append(item[i])
	item_chars.sort()
	return string.join(item_chars, "")

# goes through a list of strings and strips
# away the new lines at the end
def stripNewLines( list ):
	for i in range(len(list)):
		list[i] = list[i][0:len(list[i])-1]
		return list

# sort a list by a given field
def sortBy(list, n):
	nlist = map(lambda x, n=n: (x[n], x), list)
	nlist.sort()
	return map(lambda (key, x): x, nlist)  
 
if ( len(sys.argv) != 2 ):
	print "You must pass one input file to this program. That file"
	print "should contain lowercase words seperated by new lines."
	print "Example: python dict.txt"
	sys.exit()
 
# prepare our file
inFile = ""
try: 
	inFile = open(sys.argv[1], "r" )
except IOError:
	print "Error opening input file"
	sys.exit()

# read the dictionary and make a new one
# with each word and its signature 
dict = stripNewLines(inFile.readlines())
newDict = []

# go through the dictionary and and make
# a new one with signatures
for item in dict:
	newDict.append([item, getSignature(item)])
 
# sort the new dictionary by signature
newDict = sortBy(newDict, 1)

finalDict = {}

# group the dictionary entries by anagram
for item in newDict:
	if not (finalDict.has_key(item[1])):
		finalDict[item[1]] = [] 
		finalDict[item[1]].append(item[0])

# output only the anagrams
print "Anagrams Found:"

for group in finalDict.values():
	if ( len(group) > 1 ):
        	print group
