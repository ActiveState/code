## Syntactic sugar to create XHTML hierarchies with ElementTree  
Originally published: 2012-01-18 21:58:04  
Last updated: 2012-01-18 22:15:58  
Author: Alain Mellan  
  
Simplify the code when creating XHTML or XML hierarchies with ElementTree.\n\nUsually, I have code like this:\n\n    table = ET.SubElement(body, 'table')\n    table.attrib['border'] = '1'\n    \n    tr = ET.SubElement(table, 'tr')\n    ET.SubElement(tr, 'td').text = 'some text'\n\nUsing Python's __getattr__ and partial function evaluation allows to create an\nobject that will yield a much simplified syntax.