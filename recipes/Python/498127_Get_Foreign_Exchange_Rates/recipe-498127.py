# fxRates.py - M.Keranen (mksql@yahoo.com) - 03/17/2006
# -----------------------------------------------------
# Query NY Federal Reserve for currency exchange rates

import sys, string, time, urllib
from xml.dom import minidom, Node

def walk(parent, rates, level = 0, data = ''):
    global unit
    unit = data
    for node in parent.childNodes:
        if node.nodeType == Node.ELEMENT_NODE:
            # Element name
            nodeName = node.nodeName.split(':')[-1]

            attrs = node.attributes
            for attrName in attrs.keys():
                attrNode = attrs.get(attrName)
                attrValue = attrNode.nodeValue
                if attrName == 'UNIT':
                   unit = attrValue
                   #print '%s:%s' % (attrName, unit)

            content = []
            for child in node.childNodes:
                if child.nodeType == Node.TEXT_NODE:
                    content.append(child.nodeValue)
            if content:
                strContent = string.join(content)
                if nodeName == 'CURR':
                    unit = unit + ' ' + strContent
                if nodeName == 'TIME_PERIOD':
                    rates[unit] = strContent
                if nodeName == 'OBS_VALUE':
                    rates[unit] = rates[unit] + ' ' + strContent

            walk(node, rates, level+1, unit)

date = time.strftime('%Y-%m-%d',time.localtime())

url = 'http://www.newyorkfed.org/markets/fxrates/FXtoXML.cfm?FEXdate=%s&FEXtime=1200' % date
doc = minidom.parseString(urllib.urlopen(url).read())

rates = {}
rootNode = doc.documentElement
walk(rootNode, rates)

outFile = open('NYFEX_%s.txt' % date,'w')
outFile.write('USD to Currency Multiplier (%s) \n' % url)

for unit in rates:
    rate = rates[unit]
    if unit.split()[0] == 'USD':
        unit = unit.split()[1]
        rate = '%s %s' % ( rate.split()[0] , round(1/float(rate.split()[1]),4) )
    else: unit = unit.split()[0]
    outFile.write('%s %s\n' % (unit,rate))

outFile.close()

print rates
print list(rates)
