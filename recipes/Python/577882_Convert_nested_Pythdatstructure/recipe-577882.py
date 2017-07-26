import lxml.etree as et

def data2xml(d, name='data'):
    r = et.Element(name)
    return et.tostring(buildxml(r, d))

def buildxml(r, d):
    if isinstance(d, dict):
        for k, v in d.iteritems():
            s = et.SubElement(r, k)
            buildxml(s, v)
    elif isinstance(d, tuple) or isinstance(d, list):
        for v in d:
            s = et.SubElement(r, 'i')
            buildxml(s, v)
    elif isinstance(d, basestring):
        r.text = d
    else:
        r.text = str(d)
    return r

print data2xml({'a':[1,2,('c',{'d':'e'})],'f':'g'})
# <data><a><i>1</i><i>2</i><i><i>c</i><i><d>e</d></i></i></a><f>g</f></data>
