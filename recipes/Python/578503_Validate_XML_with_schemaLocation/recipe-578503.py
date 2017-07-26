# coding: utf-8
"""
    XML Validation by schemaLocation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This snippet addresses the problem of validating XML documents that refer to
    schemas using xsi:schemaLocation with lxml. The problem has been brought up
    in the following locations:

    http://stackoverflow.com/questions/2979824/in-document-schema-declarations-and-lxml
    https://mailman-mail5.webfaction.com/pipermail/lxml/2011-September/006153.html

    :copyright: Copright 2013 Mathias Loesch
"""

from lxml import etree

XSI = "http://www.w3.org/2001/XMLSchema-instance"
XS = '{http://www.w3.org/2001/XMLSchema}'


SCHEMA_TEMPLATE = """<?xml version = "1.0" encoding = "UTF-8"?>
<xs:schema xmlns="http://dummy.libxml2.validator"
targetNamespace="http://dummy.libxml2.validator"
xmlns:xs="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
version="1.0"
elementFormDefault="qualified"
attributeFormDefault="unqualified">
</xs:schema>"""


def validate_XML(xml):
    """Validate an XML file represented as string. Follow all schemaLocations.

    :param xml: XML represented as string.
    :type xml: str
    """
    tree = etree.XML(xml)
    schema_tree = etree.XML(SCHEMA_TEMPLATE)
    # Find all unique instances of 'xsi:schemaLocation="<namespace> <path-to-schema.xsd> ..."'
    schema_locations = set(tree.xpath("//*/@xsi:schemaLocation", namespaces={'xsi': XSI}))
    for schema_location in schema_locations:
        # Split namespaces and schema locations ; use strip to remove leading
        # and trailing whitespace.
        namespaces_locations = schema_location.strip().split()
        # Import all found namspace/schema location pairs
        for namespace, location in zip(*[iter(namespaces_locations)] * 2):
            xs_import = etree.Element(XS + "import")
            xs_import.attrib['namespace'] = namespace
            xs_import.attrib['schemaLocation'] = location
            schema_tree.append(xs_import)
    # Contstruct the schema
    schema = etree.XMLSchema(schema_tree)
    # Validate!
    schema.assertValid(tree)
