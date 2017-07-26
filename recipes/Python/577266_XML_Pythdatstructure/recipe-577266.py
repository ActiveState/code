'''
Sirius.py

This is a simple interface to a collection of classes which
serialize Python objects to XML and back.

The system is very lightweight and was not intended for complex XML

Usage:
  xmlString = Sirius.serialize( pythonObj )
  pythonObj = Sirius.deserialize( xmlString )
'''

from XML2Py import XML2Py
from Py2XML import Py2XML


def deserialize( xmlString ):
    deserializer = XML2Py()
    return deserializer.parse( xmlString )

def serialize( pyObject, root=None ) :
    serializer = Py2XML()
    return serializer.parse( pyObject, root )


def main():

    test_xml = '''
    <documents>
      <document date="June 6, 2009" title="The Newness of Python" author="John Doe">
        <copyright type="CC" url="http://www.creativecommons.org/" date="June 24, 2009" />
        <text>Python is very nice. Very, very nice.</text>
        <formats>
          <format type="pdf">
            <info uri="http://www.python.org/newness-of-python.pdf" pages="245" />
          </format>
          <format type="web">
            <info uri="http://www.python.org/newness-of-python.html" />
          </format>
        </formats>
      </document>
    </documents>
    '''

    # This is not for use, just to see how XML compares to Python
    data_output = '''
    {'documents': [
          { 'title': 'The Newness of Python',
            'date': 'June 6, 2009',
            'author': 'John Doe',
            'copyright': {
                'url': 'http://www.creativecommons.org/',
                'date': 'June 24, 2009',
                'type': 'CC'},
            'text': ['Python is very nice. Very, very nice.'],
            'formats': [
                {   'type': 'pdf',
                    'info': {
                        'uri': 'http://www.python.org/newness-of-python.pdf',
                        'pages': '245'}
                },
                { 'type': 'web',
                    'info': {
                        'uri': 'http://www.python.org/newness-of-python.html'}
                }
            ]
          }
      ]
    }

    '''

    print test_xml
    deserialized1 = deserialize( test_xml )
    #print deserialized1
    serialized1 = serialize( deserialized1 )
    #print serialized1
    deserialized2 = deserialize( serialized1 )
    print deserialized2
    serialized2 = serialize( deserialized2 )
    print serialized2

    # compare using Python data structures
    if deserialized1 == deserialized2:
        print "They are equal"


if __name__ == '__main__':
    main()
