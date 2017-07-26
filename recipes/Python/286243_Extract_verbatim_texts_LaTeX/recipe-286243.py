import re
import sys

def make_vgetter():
    def counter():
        i = 0
        while True:
            i += 1
            yield i
    cnt = counter()
    def get_verbatim(m):
        i = cnt.next()
        name = 'verbout%03d.txt' % i
        f = file(name, 'w')
        f.write(m.group(1))
        f.close()
        return '\\verbatiminput{%s}' % name
    return get_verbatim

if __name__ == "__main__":
    verbatim = re.compile(r'\\begin\{verbatim\}\n(.+?)\n\\end\{verbatim\}',
                          re.S)
    f = file(sys.argv[1])
    s = f.read()
    f.close()
    print verbatim.sub(make_vgetter(), s)
