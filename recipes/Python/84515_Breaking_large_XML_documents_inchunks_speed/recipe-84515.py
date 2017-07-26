import re
from xml.dom.ext.reader import Sax

def tinyDom(xmlStr,tagname, start=0):
	
	# This builds a regex of the opening and the closing tag
        # Note that it doesn't handle singleton tags
	begStr = "<%s.*" %tagname
	endStr = "</%s.*" %tagname


	# find the beginning and ending tag
        begTag=re.search(begStr,xmlStr[start:])
	endTag=re.search(endStr,xmlStr[start:])

	if begTag:
		beg = begTag.start() 
	else:
		return None, start

	if endTag:
		end = endTag.end() 
	else:
		return None, start

        if beg > end:
             return None, start

	return Sax.FromXml(begTag.string[beg:end]),end+start
