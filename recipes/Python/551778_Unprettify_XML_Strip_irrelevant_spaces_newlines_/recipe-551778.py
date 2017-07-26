#!/bin/python
# works w/Jython also
import xml.dom.minidom as dom

input_xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd"
>
  <command>
    <login>
      <clID>username</clID>
      <pw>password</pw>
      <options>
        <version>1.0</version>
        <lang>en</lang>
      </options>
      <svcs>
        <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
        <objURI>urn:ietf:params:xml:ns:host-1.0</objURI>
      </svcs>
    </login>
    <clTRID>ABC-12345-XYZ</clTRID>
  </command>
</epp>"""

"""
Simple doctest:
>>> fromprettyxml(input_xml) 
<?xml version="1.0" ?><epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd"><command><login><clID>username</clID><pw>password</pw><options><version>1.0</version><lang>en</lang></options><svcs><objURI>urn:ietf:params:xml:ns:domain-1.0</objURI><objURI>urn:ietf:params:xml:ns:host-1.0</objURI></svcs></login><clTRID>ABC-12345-XYZ</clTRID></command></epp>
"""
def fromprettyxml(input_xml): #cool name, but not the opposite of dom.toprettyxml()
    _dom = dom.parseString(input_xml)
    output_xml = ''.join([line.strip() for line in _dom.toxml().splitlines()])
    _dom.unlink()
    return output_xml

def _test():
    import doctest, stripxml
    doctest.testmod(stripxml)

if __name__ == "__main__":
    _test()
    print fromprettyxml(input_xml)
