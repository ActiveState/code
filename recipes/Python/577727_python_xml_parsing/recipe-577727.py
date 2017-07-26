# -*- coding: utf-8 -*-
from xml.dom import minidom
fsock = open('parse.xml')
xmldoc = minidom.parse(fsock)
print xmldoc.toxml()
print '\n'

print "*************** Parse Child Node first ***************"
grammarNode = xmldoc.firstChild
grammarNode.childNodes  
print grammarNode.childNodes[1].toxml() 
print "*************** Parse Child Node Second***************"
print grammarNode.childNodes[3].toxml()
print "*************** Parse Child Node Third***************"
print grammarNode.childNodes[5].toxml()

print "\n**************** Extracting Data ******************** "

for i in range(1,6,2):
  refNode = grammarNode.childNodes[i]
  print "child Node"+" "+str(i)
  pNode = refNode.childNodes[1]
  print "Name:"+ pNode.firstChild.data 
  pNode = refNode.childNodes[3]
  print "Age:"+ pNode.firstChild.data 
  pNode = refNode.childNodes[5]
  print "Year:"+ pNode.firstChild.data 
  print "\n"
  

parse.xml:
"""<?xml version="1.0" ?>
<result>
  <value>
     <name> Abhijeet Vaidya </name>
     <age>  21 </age>
     <year> 1990 </year>
  </value>
  <value>
     <name> Keerthan Pai </name>
     <age>  21 </age>
     <year> 1990 </year>
  </value>
  <value>
     <name> Krishnaraj </name>
     <age>  21 </age>
     <year> 1990 </year>
  </value>
</result>
"""
