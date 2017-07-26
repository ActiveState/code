import urllib.request
import xml.dom.minidom

def um_import(name, revision):
    url = 'http://utilitymill.com/api/xml/utility/{0}/{1}/code'
    file = urllib.request.urlopen(url.format(name, revision))
    out = file.read().decode()
    fix = out.split('<', 1)[1].rsplit('>', 1)[0]
    dom = xml.dom.minidom.parseString('<' + fix + '>')
    elements = dom.getElementsByTagName('code')
    assert len(elements) == 1, 'XML Error'
    code = elements[0]
    assert len(code.childNodes) == 1, 'XML Error'
    child = code.childNodes[0]
    assert child.nodeType == child.CDATA_SECTION_NODE, 'XML Error'
    module = child.nodeValue
    open(name + '.py', 'w').write(module)
    return __import__(name)

# TEST 1
SPICE = um_import('SPICE', 27)

# TEST 2
nysiis = um_import('nysiis', 20).nysiis
while True:
    print(nysiis(input('Name or Word: ')))
