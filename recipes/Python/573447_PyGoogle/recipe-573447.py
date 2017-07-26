#PyGoogle searches Google
#Just prompts user input, replaces spaces with +'s, and opens the new URL w/ #the webbrowser module
#Could possibly add other search engines. I attempted with Ask.com but I think
#the search engine requires a cookie
import webbrowser
while 1:
    s = raw_input('Search: ')
    url_goog = 'http://www.google.com/search?hl=en&q='
    url_add1 = ''
    s = '+'.join((s.split(' ')))
    print s
    webbrowser.open(url_goog+s)
