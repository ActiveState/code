def main(index, links, key):
    try:
        index = file(index, 'rU', 0).read()
        try:
            links = file(links, 'rU', 0).read()
            try:
                source = build(index, links, key)
                try:
                    html(source)
                except:
                    plain('ERROR: the source could not be displayed.')
            except:
                plain('ERROR: the source could not be built.')
        except:
            plain('ERROR: %s (LINKS) cannot be found.' % links)
    except:
        plain('ERROR: %s (INDEX) cannot be found.' % index)

def build(index, links, key):
    links = parse(links)
    links = check(links)
    links = write(links)
    index = final(index, links, key)
    return index

def parse(links):
    links = links.splitlines()
    for index in range(len(links)):
        links[index] = links[index].split(' ', 1)
    return links

def check(links):
    from socket import socket
    for index in range(len(links)):
        try:
            test = socket()
            test.settimeout(0.05)
            test.connect((links[index][0], 80))
        except:
            links[index][0] = None
    return links

def write(links):
    string = str()
    for link in links:
        string += '\t<h3>\n\t\t'
        if link[0] is None:
            string += link[1]
        else:
            string += '<a href="http://' + link[0] + '/">' + link[1] + '</a>'
        string += '\n\t</h3>\n'
    return string [:-1]

def final(index, links, key):
    key = '<!--' + key + '-->'
    index = index.replace(key, links)
    return index

def html(string):
    print 'Content-type: text/html'
    print
    print string

def plain(string):
    print 'Content-type: text/plain'
    print
    print string

if __name__ == '__main__':
    main('index.txt', 'links.txt', 'Python: Insert Links')
