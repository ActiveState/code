import re

def chunker(data, size):
    m = re.compile(r'.{%s}|.+' % str(size),re.S)
    return m.findall(data)

if __name__ == "__main__":
    t = 'some sample text is all that i want'
    chunker(t, 10)
