import urllib.request
import urllib.parse
import xml.dom.minidom

def test_latest(name, **query):
    revision = get_revision(name)
    output = get_output(name, revision, query)
    return output

def get_output(name, revision, query):
    string = run_utility('xml', name, revision, query)
    middle = string.split('<', 1)[1].rsplit('>', 1)[0]
    dom = xml.dom.minidom.parseString('<' + middle + '>')
    value = extract_output(dom)
    dom.unlink()
    return value

def run_utility(api, name, revision, query):
    url = 'http://utilitymill.com/api/{0}/utility/{1}/{2}/run?{3}'
    params = urllib.parse.urlencode(query)
    file = urllib.request.urlopen(url.format(api, name, revision, params))
    # dom = xml.dom.minidom.parse(file)
    return file.read().decode()

def extract_output(dom):
    elements = dom.getElementsByTagName('output')
    assert len(elements) == 1, 'XML Error'
    output = elements[0]
    assert len(output.childNodes) == 1, 'XML Error'
    child = output.childNodes[0]
    assert child.nodeType == child.CDATA_SECTION_NODE, 'XML Error'
    return child.nodeValue

def get_revision(name):
    string = info_utility('xml', name)
    middle = string.split('<', 1)[1].rsplit('>', 1)[0]
    dom = xml.dom.minidom.parseString('<' + middle + '>')
    value = extract_number(dom)
    dom.unlink()
    return value

def info_utility(api, name):
    url = 'http://utilitymill.com/api/{0}/utility/{1}/info'
    file = urllib.request.urlopen(url.format(api, name))
    return file.read().decode()

def extract_number(dom):
    elements = dom.getElementsByTagName('number')
    assert len(elements) == 1, 'XML Error'
    number = elements[0]
    assert len(number.childNodes) == 1, 'XML Error'
    child = number.childNodes[0]
    assert child.nodeType == child.TEXT_NODE, 'XML Error'
    return child.nodeValue

################################################################################

import random
import spice
import time

# Python 2.5 Hack
__builtins__.xrange = __builtins__.range
def hack1(*args):
    return list(xrange(*args))
__builtins__.range = hack1
__builtins__.xmap = __builtins__.map
def hack2(*args):
    return list(xmap(*args))
__builtins__.map = hack2
def _decode(string, map_1, map_2):
    'Private module function.'
    cache = ''
    iterator = iter(string)
    for byte in iterator:
        bits_12 = map_1[ord(byte)] << 6
        bits_34 = map_1[ord(next(iterator))] << 4
        bits_56 = map_1[ord(next(iterator))] << 2
        bits_78 = map_1[ord(next(iterator))]
        cache += map_2[bits_12 + bits_34 + bits_56 + bits_78]
    return cache
spice._decode = _decode
# END

def main():
    try:
        while True:
            print('Testing', end=' ')
            choice = random.randrange(3)
            if choice == 1:
                # Test "Create Keys" Action
                print('Create', end=' ')
                choice = random.randrange(4)
                if choice == 1:
                    # Test No Names
                    print('No Names', end=' ... ')
                    test_create()
                elif choice == 2:
                    # Test Major Name
                    print('Major Name', end=' ... ')
                    n1 = verse()
                    major, minor = test_create(MAJOR_NAME=n1)
                    assert major == spice.named_major(n1)
                elif choice == 3:
                    # Test Minor Name
                    print('Minor Name', end=' ... ')
                    n2 = verse()
                    major, minor = test_create(MINOR_NAME=n2)
                    assert minor == spice.named_minor(n2)
                else:
                    # Test Both Names
                    print('Both Names', end=' ... ')
                    n1, n2 = verse(), verse()
                    major, minor = test_create(MAJOR_NAME=n1, MINOR_NAME=n2)
                    assert major == spice.named_major(n1)
                    assert minor == spice.named_minor(n2)
            elif choice == 2:
                # Test "Encode Input" Action
                print('Encode', end=' ... ')
                major = spice.crypt_major()
                minor = spice.crypt_minor()
                data = verse()
                encoded = test_encode(major, minor, data)
                decoded = spice.decode_string(encoded, major, minor)
                assert decoded == data
            else:
                # Test "Decode Input" Action
                print('Decode', end=' ... ')
                major = spice.crypt_major()
                minor = spice.crypt_minor()
                data = verse()
                encoded = spice.encode_string(data, major, minor)
                decoded = test_decode(major, minor, encoded)
                assert decoded == data
            print('PASS')
            time.sleep(60)
    except:
        print('FAIL')

def test_create(**query):
    output = test_latest('SPICE_Text', ACTION='Create Keys', **query)
    x, x, major, x, x, x, minor = output.split('\n')
    major = hex2bin(major)
    minor = hex2bin(minor)
    spice._check_major(major)
    spice._check_minor(minor)
    return major, minor

def test_encode(major, minor, data):
    hma = bin2hex(major)
    hmi = bin2hex(minor)
    output = test_latest('SPICE_Text', ACTION='Encode Input',
                         MAJOR_KEY=hma, MINOR_KEY=hmi, INPUT=data)
    encoded = hex2bin(output.replace('\r', '').replace('\n', ''))
    return encoded

def test_decode(major, minor, data):
    hma = bin2hex(major)
    hmi = bin2hex(minor)
    hda = bin2hex(data)
    decoded = test_latest('SPICE_Text', ACTION='Decode Input',
                         MAJOR_KEY=hma, MINOR_KEY=hmi, INPUT=hda)
    return decoded

def bin2hex(x):
    return ''.join('%02X' % ord(y) for y in x)

def hex2bin(x):
    return ''.join(chr(int(x[y:y+2], 16)) for y in range(0, len(x), 2))

################################################################################

def verse():
    return random.choice(random.choice(random.choice(BIBLE)))

def load_bible():
    global BIBLE
    try:
        bible = open('bible13.txt', 'r').read()
    except:
        bible = get_bible()
        open('bible13.txt', 'w').write(bible)
    win_fix = bible.replace('\r\n', '\n')
    mac_fix = win_fix.replace('\r', '\n')
    BIBLE = parse_bible(mac_fix)

def get_bible():
    url = 'http://www.gutenberg.org/dirs/etext92/bible13.txt'
    file = urllib.request.urlopen(url)
    return file.read().decode()

def parse_bible(string):
    'Parse Bible and return 3D array.'
    book = chap = vers = 1
    form = '%02u:%03u:%03u'
    book_s, chap_s, vers_s = [], [], []
    start = 0
    while True:
        try:
            start = string.index(form % (book, chap, vers), start) + 11
            end = string.index('\n\n', start)
            vers_s.append(' '.join(string[start:end].replace('\n', '').split()))
            start = end
            vers += 1
        except:
            if vers != 1:
                chap_s.append(vers_s)
                vers_s = []
                chap += 1
                vers = 1
            elif chap != 1:
                book_s.append(chap_s)
                chap_s = []
                book += 1
                chap = 1
            elif book != 1:
                return book_s
            else:
                raise EOFError

################################################################################

if __name__ == '__main__':
    load_bible()
    main()
