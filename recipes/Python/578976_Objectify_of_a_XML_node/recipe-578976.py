"""
Tool for converting an XML node into an object instance.

.. module:: objectify
    :platform: Unix, Windows
    :synopsis: providing conversion for XML nodes.

.. moduleauthor:: Thomas Lehmann

License
=======
Copyright (c) 2014 Thomas Lehmann

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re


def objectify(node, attributes=None):
    """
    Converting XML node into an object instance.

    Taking the tag name with first letter as upper case
    as the name forgenerating a class derived from object
    with the node attributes as fields and the values as 'default'.

    >>> import xml.etree.ElementTree as ET
    >>> document = ET.fromstring('<test-obj int-val="1" str-val="hello" float-val="1.23"/>')
    >>> instance = objectify(document, {"object-id": "1234"})
    >>> print(instance.__class__.__name__)
    TestObj
    >>> print(instance.object_id)
    1234
    >>> print(instance.int_val)
    1
    >>> print(instance.str_val)
    hello
    >>> print(instance.float_val)
    1.23

    :param node: xml node (from lxml.etree or xml.etree)
    :param attributes: allows providing fields and default values
                       which might be overwritten by the XML node attributes.
    :returns: instance with node attributes as fields
    """
    def convert(attribute_value):
        """
        Convert string to float or int were possible.

        :param attribute_value: string value
        :return: depend on re.match a string, a float or an int value.
        """
        if re.match(r"\d+\.\d+", attribute_value):
            return float(attribute_value)
        if re.match(r"\d+", attribute_value):
            return int(attribute_value)
        return attribute_value

    if None == attributes:
        attributes = {}
    else:
        attributes = (dict([(key.replace("-", "_"), convert(value))
                            for key, value in attributes.items()]))

    attributes.update(dict([(key.replace("-", "_"), convert(value))
                            for key, value in node.attrib.items()]))
    class_name = "".join([entry.title() for entry in node.tag.split("-")])
    return type(class_name, (object,), attributes)()
