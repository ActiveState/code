# wikipedia_orange.py

# Author: Vasudev Ram

import wikipedia

# First, try searching Wikipedia for a keyword - 'Orange':
# It works, but if there are multiple pages with that word
# in the title, you get them all back.

print "1: Searching Wikipedia for 'Orange'"
try:
    print wikipedia.page('Orange')
    print '-' * 60
except wikipedia.exceptions.DisambiguationError as e:
    print str(e)
    print '+' * 60
    print 'DisambiguationError: The page name is ambiguous'
print

# Next, select one of the results from the search above,
# such as the orange fruit, and search for it,
# replacing spaces in the search term with underscores:
print "2: Searching Wikipedia for 'Orange (fruit)'"
print wikipedia.page('Orange_(fruit)')
print

# The output is:
# <WikipediaPage 'Orange (fruit)'>

# That is because the return value from the above call is a 
# WikipediaPage object, not the content itself. To get the content 
# we want, we have to access the 'content' attrbute of the 
# WikipediaPage object:

#print wikipedia.page('Orange_(fruit)').content

# However, if we access it directly, we may get a Unicode error, so
# we encode it to UTF-8:

result = wikipedia.page('Orange_(fruit)').content.encode('UTF8')
print "3: Result of searching Wikipedia for 'Orange_(fruit)':"
print result
print

orange_count = result.count('orange')
print

# And find the number of occurrences of our original search keyword,
# 'orange', within the resulting content:
print "The Wikipedia page for 'Orange_(fruit)' has " + \
    "{} occurrences of the word 'orange'".format(orange_count)
print
