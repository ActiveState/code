from xml.parsers.xmlproc import xmlproc
from xml.parsers.xmlproc import xmlval
from xml.parsers.xmlproc import xmldtd

# code to handle XML parsing goes here
class MyApp(xmlproc.Application):
  def handle_start_tag(self,name,attrs):
    pass
  def handle_end_tag(self,name):
    pass
  def handle_data(self,data,start,end):
    pass
  def handle_comment(self,data):
    pass

# XML file and corresponding DTD definition
file = 'test.xml'
dtd  = 'test.dtd'

# standard XML parsing, without validation against DTD
print 'Start XML Parsing (No DTD)'
p = xmlproc.XMLProcessor()
p.set_application(MyApp())
p.parse_resource(file)
print 'End XML Parsing (No DTD)'
print

# XML parsing, with validation against external DTD
# Since you are referencing an external DTD from 
# test.xml, you'll need markers like:
# 
#  <?xml version="1.0"?>
#  <!DOCTYPE base SYSTEM "test.dtd">
#
# (where 'base' is the root element of the XML doc) 
# at the top of your XML doc

print 'Start XML Parsing (With DTD)'
d = xmldtd.load_dtd(dtd)
p = xmlval.XMLValidator()
p.set_application(MyApp())
p.parse_resource(file)
print 'End XML Parsing (With DTD)'
