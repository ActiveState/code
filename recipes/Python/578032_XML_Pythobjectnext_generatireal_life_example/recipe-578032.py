# Copyright (C)  Boris Kats 2011 - 2012.

import sys, string
from xml.dom import minidom, Node
from datetime import date
from datetime import datetime as dt
#import types
from types import *
import collections
from keyword import iskeyword as iskeyword

__xmlspecial__= collections.OrderedDict([("&","&amp"),("<","&lt;"),(">","&gt;"),('"',"&quot;")])

__TupleLimit__ = 5

def strToXMLstr(word,table = __xmlspecial__):
    for i, j in table.items() : 
       word = word.replace(i,j)
    return word

def XMLstrTostr(word,table = __xmlspecial__):    
    for i, j in table.items() : 
       word = word.replace(j,i)
    return word

def make_date(d):
   ''' ugly fuction to handle all kind of date formats
       as ("02-03-2012","01-FEB-12","01/23/12","11/28/06")
       which are used simultaneously by US Department of Treasure '''
   index = d.find('T')
   if index != -1:
     d = d[:index]
   if '-' in d: 
      parts = d.split('-')
      dt_type='-'
   else:
      parts = d.split('/')
      dt_type = '/'
   if parts[1].isalpha():
      month_f ='%b' if len(parts[1])==3 else '%B'
      first_f ='%d'
      second_f = '%Y' if len(parts[2])==4 else '%y'
   else:
      if int(parts[0])<=12:
         first_f = '%m'
         month_f = '%d'
         second_f = '%Y' if len(parts[2])==4 else '%y'
      else:
         if int(parts[0]) > 1000:
             first_f = '%Y'
             month_f = '%m'
             second_f = '%d'            
         else:
             first_f = '%m'
             month_f = '%d'
             second_f = '%Y' if len(parts[2])==4 else '%y'
   d_format = dt_type.join([name for name in [first_f,month_f,second_f] ])
   return dt.strptime(d,d_format).date()

def make_bool(boolean):
   if boolean.isalpha():
      return boolean.upper()=='TRUE'
   else: 
      return  boolean !='0'

class anyxml(object):
   '''The class, which populate himself from xml recursivly into ready to use python class.
       The types of primitives will be deduced from xml as string representation of primitive. 
       For example in xml: 
       <Address><HomeNumber>27</HomeNumber><Street>Mystreet<Street><isSingleFamily>True</isSingleFamily>
       <whenBought>2012-01-12</whenBought><totalArea>0.75></totalArea>...</Address> 
       "27" will became "int"; "0.75" => "float; "Mystreet" => str, "True" => bool and "2012-01-12" => date.
       All attempts are made to preserve information about tags (names) from xml.
       For example above the resultant python class will have var Address as namedtuple  
       with members HomeNumber, Street ... and each of those members in turn will be instances of proper 
       type and ready to use.
       The couple of other samples:
       xml: <myVector><element>0.1</element> .... <element>0.9</element></MyVector>
       will came out in python class as MyVector as list of floats;
       xml:  <myMap><1Month>0.25</1Month><2Month>0.35</2Month>.... </myMap>
       will be translated into var myMap as dictionary of string and float or into namedtuple,
       based by length of array.
       The class will accept any  xml with simple rules ( nothing unreasonable):
          a) All elements should be valid xml : 
             <member>I am string</member>  or <member value="I am string"/>
          b) Empty elements as <MyElement/> will be ignored
          c) Empty wrappers as <MyElement><member value="I am string"/></MyElement/> will be ignored 
             as well - tag "MyElement" in that context does not carry any usefull information.
          d) Elements of collection types should be bracked; otherwise the name of collection is unknown: 
             <myVector><element>0.5</element> <element>0.6</element> .... <element>0.7</element></MyVector>
             The name myVector (type of list) will come to python class; however tag names for elements 
             of containers are irrelevant: they are nameless and accessible by [] operator. 
       The containers with distinguished tags will be translated into dict or namedtuple to preserve
       these names. The types of dict and namedtuple are interchangeable; however if the sequence is
       homogeneous(all elements have the same type), it will translated into the dict.
       Sequences with mixed types of elements will be accepted in pythonic style.
       If for some irregularity in xml, names of elements were lost in translation process,
       the warning message will be produced. 
       Often xml is coming from thrird party application with it's own namespaces and problems. 
       It is not practical to deal with unreasonable of xml in that class. That problem can be addressed 
       with pre-processing of input xml as :
         1. make the special dictionary to translate input xml into something reasonable:
         2. read xml into single string and translate it with function strToXMLstr(xml,table= translator)
         3. feed minidom parser with that string instead of file ( use doc = minidom.parseString(data) ).
       Hopefully, this pre-processing procedure will help. 

       In the real life example the xml from US Department of Treasure is used to generate US Treasure
       Yield Curve. The xml itself, fetched from url, is in terrible condition: meaningless names,
       all kind of date formats("02-03-2012","01-FEB-12","01/23/12","11/28/06" are used simultaneously, 
       tag names contain punctuations symbols, etc ...( This is the reason  for ugly function make_date). 
       Actually, there are two different urls with two xml schemas and for historical datum xml is 
       not normalized at all: the sequence of tags with the same names are not bracketed. 
       However, it is still possible to convert that xml into reasonable python class. 
       The historical xml contains the information for full year and it runs a little bit longer. 
       Run appliation as "python anyxml.py 02/07/2012" or for any business date in the past.

       To inspect the content of resultant object one can use nice function "total_size" in verbose
       mode by Raymond Hettinger from http://code.activestate.com/recipes/577504/ or 
       function objwalk by Yaniv Aknin from:   http://code.activestate.com/recipes/577982/.
       Before using that class make sure that your input xml is valid: try to open it in browser. '''
    
   def __init__(self,source):
      super()
      doc = minidom.parseString(source) 
      self.buildFromXml(doc.documentElement)

   def fromStringToType(self,content):
     ''' Making rhe guess what is the type of data '''
     if content.isalpha():
        contentUp = content.upper()
        if contentUp=='TRUE' or contentUp=='FALSE':
           return make_bool(content)
        return content  
     else:
        index = content.find('T')
        input = content[:index] if index != -1 else content
        components = input.split('-') if '-' in input else input.split('/')      
        if (8<=len(input)<= 10)  and len(components) == 3:
           return make_date(content)
        else:
           try:
              try_int = int(content)
              return try_int
           except ValueError:  
              try:
                 try_flt = float(content)
                 return try_flt
              except ValueError:
                 return content

   def getAttribute(self,node,attribute):
       ''' get attribute in safe mode '''
       if node.nodeType != Node.ELEMENT_NODE:
          return None
       if hasattr(node,'attributes'):
          attributes = node.attributes
          if hasattr(attributes,'get'):
             item = attributes.get(attribute,None)
             if item and len(item.value.strip()) != 0: 
                return item.value.strip()
             else: return None
          else: return None
       else: return None
   
   def buildFromXml(self,root):
       ''' travel int xml tree ''' 
       for node in root.childNodes:
          nodeKind = node.nodeType
          if nodeKind == Node.ELEMENT_NODE:
             nodeName = node.nodeName.strip()
             item = self.buildNode(node)
             if item[1] != None:
#for regulars xml setattr(self,item[0],item[1]) will work
#for irregulars put element into wrappre list
                modName = item[0] + 'List_'
                items = getattr(self,modName,None)
                if items != None:
                   items.append(item[1])
                else:
                   items = list()
                   items.append(item[1])               
                   setattr(self,modName,items)
#get rid of artificial lists
       membersList = [member for member in dir(self) if member.endswith('List_')]
       for member in membersList: 
          element = getattr(self, member)
          if(type(element) == list and len(element) ==1):
             item = element[0]
             delattr(self,member)
             setattr(self,member[:-5],item)

   def nodecount(self,root,justElements = True):
       ''' just to enumerate nodes '''
       if not justElements:
          return len(root.childNodes)
       count = 0
       for child in root.childNodes:
          if child.nodeType == Node.ELEMENT_NODE:
             count +=1 
       return count

   def buildNode(self,root):
       ''' just to retrieve node(tag) name and it's content '''
       rootName = root.nodeName.strip()
       size = len(root.childNodes)
       if size == 0:
          value = self.getAttribute(root,'value')
          if value: return rootName,self.fromStringToType(value)
          else:     return rootName,None  
       else:
          if size ==1:
             child = root.childNodes[0]
             if child.nodeType == Node.TEXT_NODE: 
                value = child.nodeValue.strip() 
                if len(value)==0: return rootName,None
                else: 
                   return rootName,self.fromStringToType(value)
             else:
                internal = self.buildNode(child)
                return internal
          else:
              size = self.nodecount(root)
              if (size ==1):                                #just empty wrapper
                  for kid in root.childNodes:
                      if kid.nodeType ==  Node.ELEMENT_NODE:
                          internal = self.buildNode(kid)
                          return internal
              items = list()
              names = list()
              for kid in root.childNodes:
                 item = self.buildNode(kid)
                 if item[1] != None:
                    items.append(item[1])
                    name = item[0]
                    if name.find(':') !=-1 :
                       name = name.replace(':','_')
                    if iskeyword(name):
                       name = name[:1].upper()+ name[1:]
                    if not name in names:
                       names.append(name)
              return self.transform(rootName, names,items)
 
   def transform(self,rootName, names,items):
       ''' Transform two input lists of names and values into 
       class member of list, dict, namedtuple or tuple.'''
       isHomogeneous = True
       tt = type(items[0])
       if (tt == int): tt = float
       for el in items[:1]:
           ttn = type(el)
           if (ttn == int): ttn = float
           if tt != ttn : 
              isHomogeneous = False
              break
       if ( len(names) ==1 and isHomogeneous): 
          member = items[0]
          if (type(member).__name__ == 'namedtuple' and  len(member)==2 and hash(member[0])):
             myitems = dict()                  # dict
             for member in items:
               myitems[member[0]] = member[1]
             return  rootName,myitems  
          return rootName,items                # list
       if (len(names) == len(items)):
          if isHomogeneous and len(items) > __TupleLimit__ :
             myitems = dict()                  #dict
             count = 0 
             for member in items:
                myitems[names[count]] = member
                count +=1
             return rootName,myitems 
          else:                                # named tuple 
             tupleNames = ' '.join([name for name in names])
             Temp = collections.namedtuple('namedtuple',tupleNames)
             return rootName,Temp(*items)
       message = 'some information about names is lost due to irregular xml in: ' + rootName +'\n'
       warnings = getattr(self,'warnings',None)
       if (warnings == None):
          warnings = message
          setattr(self,'warnings',warnings) 
       else:
          warnings = warnings + message

       if len(items) > __TupleLimit__ :
          return rootName,items
       else:
          return rootName,tuple(items)

if __name__ =='__main__':
   import urllib.request
   import sys,time
   args = sys.argv[1:]
   try:
      inputDate = dt.strptime(args[0], '%m/%d/%Y').date()
   except ValueError as err:
       print(err)
       sys.exit(-1)
   today = date.today()
   if ( inputDate > today):
       print('Error:Input date should be business date in the past or today after 6:00PM')
       sys.exit(-1)

   url_g ='http://www.treasury.gov/resource-center/data-chart-center/interest-rates/'
   url_1 ='Datasets/yield.xml'
   url_2 ='pages/XmlView.aspx?data=yieldyear&year='

   usingHistory = False
   if (inputDate.year != today.year or inputDate.month !=today.month):
      usingHistory = True
      url = url_g + url_2+str(inputDate.year)
   else:
      url = url_g + url_1
   t1 = time.clock()
   urlfile = urllib.request.urlopen(url)
   data = urlfile.read().decode("utf8")
   urlfile.close()

   t2 = time.clock()
   print('read data from url elapsed time:',round(t2-t1,4))
   myclass = anyxml(data)
   warnings = getattr(myclass,'warnings',None)
   if warnings:
      print(warnings)
   curveFound = False
   class FoundCurve(Exception): pass
   if ( not usingHistory):
      try:
        for list_of_week in myclass.LIST_G_WEEK_OF_MONTH:
           if 'LIST_G_NEW_DATE' in list_of_week.keys():
              for date_of_week in list_of_week['LIST_G_NEW_DATE']: 
                 if(date_of_week.BID_CURVE_DATE == inputDate):
                    curveFound = True
                    print("{} {} {}".format('For',inputDate,'US Treasure Curve is:'))
                    print('Tenor   Yield')
                    tbl = date_of_week.G_BC_CAT
                    for k, v in tbl.items():
                        if (k.find('DISPLAY') == -1):
                            print(k[3:], "{}{}".format(v,'%'))    
                    raise FoundCurve()
      except FoundCurve:
         pass 
   else:
      for entry in myclass.entryList_:
         tbl = entry.m_properties
         if tbl['d_NEW_DATE'] == inputDate:
            curveFound = True
            print("{} {} {}".format('For',inputDate,'US Treasure Curve is:'))
            print('Tenor   Yield')
            for k,v in tbl.items():
               if k.find('_BC_') !=-1 and k.find('DISPLAY') == -1:
                  print(k[5:],"{0}{1}".format(round(v,4),'%')) 
            break 
   if not curveFound:
         print('For',inputDate,'US Treasure Curve not found: is it business date?')
   print("anyxml elapsed time:",round(time.clock()-t2,4))
