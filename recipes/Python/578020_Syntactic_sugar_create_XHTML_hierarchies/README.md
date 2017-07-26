## Syntactic sugar to create XHTML hierarchies with ElementTree  
Originally published: 2012-01-18 21:58:04  
Last updated: 2012-01-18 22:15:58  
Author: Alain Mellan  
  
Simplify the code when creating XHTML or XML hierarchies with ElementTree.

Usually, I have code like this:

    table = ET.SubElement(body, 'table')
    table.attrib['border'] = '1'
    
    tr = ET.SubElement(table, 'tr')
    ET.SubElement(tr, 'td').text = 'some text'

Using Python's __getattr__ and partial function evaluation allows to create an
object that will yield a much simplified syntax.