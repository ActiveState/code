import re
from elementtree import ElementTree as ET

def main():

# Some sample data from http://developer.yahoo.com/maps/rest/V1/geocode.html
    yahoo_geocode_test = """\
<?xml version="1.0" encoding="UTF-8"?>
<ResultSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns="urn:yahoo:maps"
xsi:schemaLocation="urn:yahoo:maps http://api.local.yahoo.com/MapsService/V1/GeocodeResponse.xsd">
  <Result precision="address">
    <Latitude>37.416384</Latitude>
    <Longitude>-122.024853</Longitude>
    <Address>701 FIRST AVE</Address>
    <City>SUNNYVALE</City>
    <State>CA</State>
    <Zip>94089-1019</Zip>
    <Country>US</Country>
  </Result>
</ResultSet>
    """

    # The "ResultSet" element should be treated like a list
    # The "Result" element should be treated like a map, with the
    # child elements converted to key/value pairs
    tag_convert = {"ResultSet": list_of_children,
                   "Result": children_are_mapping}

    doc = ET.fromstring(yahoo_geocode_test)
    
    xdata = XMLDataExtractor(tag_convert,
                             no_ns=True, downcase=True)

    result = xdata.from_elem(doc)

    from pprint import pprint
    pprint(result)


"""
Result:

[{'address': '701 FIRST AVE',
  'city': 'SUNNYVALE',
  'country': 'US',
  'latitude': '37.416384',
  'longitude': '-122.024853',
  'state': 'CA',
  'zip': '94089-1019'}]
"""


def identity(trans, elem):
    """Return 'elem' unchanged"""
    return elem

def attr_are_mapping(trans, elem):
    """The attributes of 'elem' contain it's key/value pairs"""
    return dict(elem.attrib)


def list_of_children(trans, elem):
    """Child elements of 'elem' are returned as a list"""
    return map(trans.from_elem, elem)

def children_are_mapping(trans, elem):
    """Child elements of elem are the key/value pairs.  tag name is
    key, value is inner text"""
    
    res = {}
    for i in elem:
        key = trans.tagnorm(i)
        if len(i):
            value = trans.from_elem(i)
        else:
            value = i.text

        res[key] =  value
        
    return res

def children_and_attr(trans, elem):
    """Child elements of 'elem', as well as it's attributes, as the
    resulting key/value pairs"""
    res = children_are_mapping(trans, elem)
    res.update(elem.attrib)
    return res


class XMLDataExtractor:

    STRIP_NS = re.compile(r"{.*}")
    
    def __init__(self, tag_convert, no_ns=False, downcase=False):
        """
        tag_convert: a map from tag names to conversion functions
        no_ns: if True, ignore namespaces
        downcase: downcase all resulting tag names
        """
        
        self.no_ns = no_ns
        self.downcase = downcase

        tag_convert_norm = {}
        for k,v in tag_convert.items():
            tag_convert_norm[self.tagnorm(k)] = v
        self.tag_convert = tag_convert_norm

    def from_elem(self, elem):
        "Convert this element to a useful datastructure"
        fn = self.tag_convert.get(self.tagnorm(elem), identity)
        return fn(self, elem)

    def tagnorm(self, tag_or_elem):
        """Normalize the tag name, optionally stripping namespaces and
        downcasing.  'elem' may be an Element or a string"""

        if ET.iselement(tag_or_elem):
            tag = tag_or_elem.tag
        else:
            tag = tag_or_elem
            
        if self.no_ns:
            res = self.STRIP_NS.sub('', tag)
        else:
            res = tag

        if self.downcase:
            res = res.lower()

        return res

        


if __name__ == "__main__": main()
