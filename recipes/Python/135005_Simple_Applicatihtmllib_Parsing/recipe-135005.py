>>> from formatter import AbstractFormatter , NullWriter
>>> from htmllib import HTMLParser
>>> from string import join
>>> class myWriter ( NullWriter ):
...     def send_flowing_data( self, str ):
...         self . _bodyText . append ( str )
...     def __init__ ( self ):
...         NullWriter.__init__ ( self )
...         self . _bodyText = [ ]
...     def _get_bodyText ( self ):
...         return join ( self . _bodyText, " " )
...     bodyText = property ( _get_bodyText, None, None, "plain text from body" )
...
>>> class MilenaHTMLParser (HTMLParser):
...     def do_meta(self, attrs):
...         self . metas = attrs
...
>>> mywriter = myWriter ( )
>>> abstractformatter = AbstractFormatter ( mywriter )
>>> parser = MilenaHTMLParser( abstractformatter )
>>> parser . feed ( open ( r'c:\temp.htm' ) . read ( ) )
>>> parser . title
'Astronomical Summary: Hamilton, Ontario'
>>> parser . metas
[('http-equiv', 'REFRESH'), ('content', '1800')]
>>> parser.formatter.writer.bodyText
'Hamilton, Ontario Picture of Earth Local Date 31 October 2001 Temperature 10.8 \xb0C Observation Location 43.17 N, 79.93 W Sunrise: Sunset: 6:53 am 5:13 pm The Moon is Waxing Gibbous (98% of Full) Image created with  xearth [1] . Page inspired by design at AUSOM.'
