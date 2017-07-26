import urllib.request
import urllib.parse
import xml.dom.minidom

################################################################################

INFO = 'http://utilitymill.com/api/{API}/utility/{NAME}/info'
RUN = 'http://utilitymill.com/api/{API}/utility/{NAME}/{VERSION}/run?{QUERY}'

################################################################################

def run_latest(name, **query):
    version = get_version(name)
    results = get_results(name, version, query)
    return results

################################################################################

def get_version(name):
    string = fix(info('xml', name))
    dom = xml.dom.minidom.parseString(string)
    value = extract(dom, 'number', 'TEXT_NODE')
    dom.unlink()
    return value

def get_results(name, version, query):
    string = fix(run('xml', name, version, query))
    dom = xml.dom.minidom.parseString(string)
    value = extract(dom, 'output', 'CDATA_SECTION_NODE')
    dom.unlink()
    return value

################################################################################

def info(api, name):
    url = INFO.format(API=api, NAME=name)
    return urllib.request.urlopen(url).read().decode()

def run(api, name, version, query):
    query = urllib.parse.urlencode(query)
    url = RUN.format(API=api, NAME=name, VERSION=version, QUERY=query)
    return urllib.request.urlopen(url).read().decode()

################################################################################

fix = lambda xml: '<' + xml.split('<', 1)[1].rsplit('>', 1)[0] + '>'

def extract(dom, tag_name, node_type):
    elements = dom.getElementsByTagName(tag_name)
    assert len(elements) == 1, 'XML Error'
    element = elements[0]
    if element.childNodes:
        assert len(element.childNodes) == 1, 'XML Error'
        child = element.childNodes[0]
        assert child.nodeType == getattr(child, node_type), 'XML Error'
        return child.nodeValue
    return ''
