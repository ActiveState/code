import urllib2
import re

page = 1
contrib = [] # each element of contrib is a tuple consisting of the name of the user and the number of submitted recipes.

while 1: # loop over pages
    print "Processing page %s" % (page)
    f=urllib2.urlopen("http://code.activestate.com/recipes/users/?page=%s" % (page))
    html = f.read()
    f.close()
    
    pattern = '<li><a href="/recipes/users/.*/">(.*)</a>\s*<span class="secondary">\((.*) recipe[s]?\)</span>'
    res = re.findall(pattern, html)
    if res:
        contrib.extend(res)

    if html.find('<span class="next disabled">') != -1: # found at the last page
        break
    else:
        page += 1

# Print users and number of recipes on screen 
#for p in contrib:
#    print p[0], p[1]

# Number of recipes as a list:
nrecipes = [int(p[1]) for p in contrib]

# Print the distribution
n = 1
while n <= max(nrecipes):
    c = nrecipes.count(n)
    if c:
        print "%s people contribute %s recipes each" % (c,n)
    n += 1
