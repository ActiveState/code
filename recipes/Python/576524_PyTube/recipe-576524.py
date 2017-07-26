import webbrowser
while 1:
    message = "You searched:"
    s = raw_input('Search: ')
    url_tube = 'http://uk.youtube.com/results?search_query='
    url_add1 = ''
    s = '+'.join((s.split(' ')))
    print message,s
    webbrowser.open(url_tube+s)
