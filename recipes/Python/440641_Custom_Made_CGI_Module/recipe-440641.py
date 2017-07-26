def execute(function, exception):
    if string == exception:
        self()
    else:
        function()

def html(string):
    print 'Content-Type: text/html\n\n' + string
    raise SystemExit(0)

def plain(string):
    print 'Content-Type: text/plain\n\n' + string
    raise SystemExit(0)

def self():
    from sys import argv
    print 'Content-Type: text/plain\n\n' + file(argv[0]).read()
    raise SystemExit(0)

def export():
    global string, dictionary, export, decode
    try:
        from os import environ
        string = environ['QUERY_STRING']
    except:
        string = None
    try:
        temp = string.replace('+', ' ').split('&')
        for index in range(len(temp)):
            temp[index] = temp[index].split('=')
        dictionary = dict()
        for parameter, value in temp:
            dictionary[decode(parameter)] = decode(value)
    except:
        dictionary = None
    del export, decode

def decode(string):
    index = string.find('%')
    while index is not -1:
        string = string[:index] + chr(int(string[index+1:index+3], 16)) + string[index+3:]
        index = string.find('%', index + 1)
    return string

if __name__ == '__main__':
    self()
else:
    export()
