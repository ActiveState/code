import string,sys,os
import csv   #http://www.object-craft.com.au/projects/csv/
import getopt

# file props.py
from props import *

#rem download from http://object-craft.com.au/projects/csv

class csv2xml:
    """Given
    an input parameter of a property file and a CSV file,
    an output file name, 
    convert the CSV file to the output file
    according to the property definitions"""

    propsFile="" #properties file name
    
    inputFile="" #input file name
    infile =0 # handle

    outputFile="" # output file name
    outfile = 0  #output file handle
    
    
    # Standard XML declaration
    PROLOG = "<?xml version=\"1.0\"?>"
    # Start tag 
    OPEN_START = "<"
    # end tag 
    OPEN_END = "</"
    # Close  
    CLOSE = ">"
    # newline 
    NEWLINE = "\n"
    #indentation  
    INDENT = "  "
    #Field Delimiter property; from property Fielddelimiter 
    fldDelimiter=""
    # Row delimiter property : from property Rowdelimiter 
    rowDelimiter=""
    #Number of fields per row
    nfields=0
    #Number of rows (by calculation)
    nrows = 0
    #Header, the xml decl, doctype etc.
    header1,header2,header3= "","",""
    #tag to use for each row.
    rowname=""
    #tag to use for root of output document
    rootname=""
    #tags to use for successive fields
    fieldnames={}


    #debug
    debug=0;
    debug2=0;
    def __init__ (self):
         version="0.3";
         print "csv2xml, version ",version
         self.propsFile=""
         self.inputFile=""
         self.outputFile=""
         self.fieldnames.clear()


    def usage(self):
        print self.__doc__
        print "Usage: csv2xml -p propertyFile -i inputFile -o outputFile"
        


    def checkFiles(self, inFile,outFile,pFile):
        #print "Outfile is: ", outFile
        if not(os.access(inFile, os.R_OK | os.F_OK)):
            print "\tNo read access to Input File ",inFile, "Quitting"
            sys.exit(2)
        if not(os.access(outFile,  os.F_OK)):
            print "output file does not exist, creating it"
            self.outfile=open(outFile, 'w')
            self.outfile.close();
        if not(os.access(pFile, os.R_OK|os.F_OK)):
               print "\tNo read access to Properties File ",pFile, "Quitting"
               sys.exit(2)
        return 1

            
    def setParameters(self, props):
        """ Load up the global parameter attributes.

        Loads the global properties from the props class.

        params: props - An instance of class props.



        """

        
        self.fldDelimiter = props.getProperty("head","fielddelimiter","X")
        self.rowDelimiter = props.getProperty("head","rowdelimiter","X")
        self.rootname = props.getProperty("head","rootname")
        self.rowname = props.getProperty("head","recordname")
        if self.debug:
            print "RowDelim[" , self.rowDelimiter , "]"
        self.dtd = props.getProperty("head","dtd","null")
        self.comment = props.getProperty("head","comment")
        if (self.fldDelimiter == "X"):
	    print "Warning: Property file error: Fielddelimiter not set, using comma"
        self.fldDelimiter=","

        if (self.rowDelimiter[0] == 'X'):
            print "Warning: Property file error: Rowdelimiter not set, using NewLine"
        self.rowDelimiter="\n"
        
        self.header1 = self.PROLOG + self.NEWLINE
        if (self.dtd != ""):
            self.header2 ="<!DOCTYPE " + self.rootname + 
            " SYSTEM " +"\""+ self.dtd + "\""+ ">"+  self.NEWLINE + 
            self.NEWLINE
            self.header3 ="<!-- " + self.comment + " -->" + self.NEWLINE
        self.nfields = props.getProperty("head","fields")

        if self.debug2:
            print "setParameters: ",self.nfields
        for i in range(int(self.nfields)):
            fieldref = "field" + str(i)
            #self.addProp(fieldref, props.getProperty('fields',fieldref))
            self.fieldnames[fieldref]=props.getProperty('fields',fieldref)
            if self.debug2:
                print "setParameters: ",props.getProperty('fields',fieldref)
        if self.debug2:
            print self.fieldnames.keys()

    def convert(self):
    #
    # *Convert the input file rows into XML,
    # * and  outputting.
    # *
    # *
    # **
        output =open(self.outputFile, 'w')
        output.write(self.header1+self.header2+self.header3)
        if self.debug:
            print "convert: writing to ", self.outputFile
            print "convert: reading fm: ", self.inputFile
        output.write(self.OPEN_START+self.rootname+self.CLOSE)  #ROOT tag
    
    #
        p = csv.parser()
        f = open(self.inputFile,'r')
        nrows = int(self.nfields) # number of fields
        #Read and parse input file till full record in hand as list
        
        while 1:
            line = f.readline()
            if not line:
                break
            rec = p.parse(line)
            if rec is not None:
                output.write(self.OPEN_START+self.rowname+self.CLOSE+self.NEWLINE) #<entry>
                idx = 0
                for fld in rec:
                    #idx = rec.index(fld)  #index of this item
                    nfld1 = string.replace(fld,"&","&amp;") # subst for &
                    nfld  = string.replace(nfld1,"£","&#x00A3;") # subst for £
                    tag = self.fieldnames['field'+str(idx)]
                    output.write(self.INDENT+self.OPEN_START+tag+self.CLOSE)
                    output.write(nfld)
                    output.write(self.OPEN_END+tag+self.CLOSE+self.NEWLINE)
                    idx += 1
                output.write(self.OPEN_END+self.rowname+self.CLOSE+self.NEWLINE)# </entry>
                
        output.write(self.OPEN_END+self.rootname+self.CLOSE)  #ROOT tag
        output.close()
    #################### Main #############################

    def main(self):
        if len(sys.argv) < 3:
            self.usage()
            sys.exit(2)
        try:
            opts,args = getopt.getopt(sys.argv[1:],"i:o:p:h",["help","input=","output=","properties="])
        except getopt.GetoptError:
            self.usage()
            print "Option Exception"
            sys.exit(2)

        indexFile=""
        searchPattern=""
        for o, a in opts:
            if self.debug:
                print "main:",o,a
            if o in ("-h","--h","-help"):
                usage()
                sys.exit()
            if o in ("-p","--p","--properties"):
                self.propsFile= a # set properties file
            if o in ("-i","--i","--input"):
                self.inputFile = a
            if o in ("-o","--o","--output"):
                self.outputFile=a  # set output file
                
        if (self.debug):
            print "Input File      ",self.inputFile
            print "Properties File ",self.propsFile
            print "Output File     ",self.outputFile

        if self.checkFiles(self.inputFile,self.outputFile,self.propsFile):
            if (self.debug):
                print "Files All OK"
            #set  file handles for files
            self.outfile = file(self.outputFile, 'w')
            self.infile  = file(self.inputFile, 'r')
            print "\tConverting "+self.inputFile+" using "+self.propsFile
            if (self.debug):
                print "Files opened."
            #instantiate the properties.
                
            myprops= props(self.propsFile)
            self.setParameters(myprops)
            
            self.convert() # convert the file.
            if self.debug:
                print "Mycsv: Done"


            
if __name__ == "__main__":
    con=csv2xml()
    con.main()
   

#====================================================================

Seperate class, probably should be included in the main file.
This reads a configuration file of the form:

The header group adds a comment, specifies the field and
row delimiters to be expected (\n should not be changed)
the recordname is the row tag.
The number of fields specifies the number of fields to expect.
  This format is specified in one of the RFC's. 


[head]
comment=Generated using CSVToXML
fielddelimiter=,
rowdelimiter=\n
rootname=products
recordname=entry
fields=35

[fields]
field0 =ProdID
field1 =Prod_Code
field2 =Print_Name
field3 =Prod_Name
field4 =Add_Info
field5 =Desc_Info
field6 =Description
field7 =Audience_Other
field8 =Product_Type
field9 =SectionID
field10 =SectionID2
field11 =Related_Products
field12 =Related_Sections1
field13 =Related_Sections2
field14 =Related_Sections3
#====================================================================


import ConfigParser
import sys

#
# Properties file  props.py. Works in conjuction with
# pcatsCSV.py to extract properties from a properties file.
#
#Only method, retrieve a named property from the properties file
# format of props file as per java 
# addition, comment as per python

class props:
    """ Mimic the java getProperties """
    handle = ""  # file handle for property.
    debug = 0
    def __init__ (self,propsFileName):
        if self.debug:
            print "props: Init called on : ",propsFileName
       
        try:
            self.handle=ConfigParser.ConfigParser()
            self.handle.readfp(open (propsFileName))
        except:
            print "\tprops: Error reading properties file, quitting"
            sys.exit(2)
            
        if self.debug:
            print "props: Done reading"


            
    def getProperty (self,sect, proName, *defaultValue):
        val = ""
        try:
            val = self.handle.get(sect,proName)
        except (ConfigParser.NoOptionError):
            print "props.getProperty, Property \""+ proName+ "\" Not found"
        if self.debug:
            if val=="":
               print "props.getProperty[", proName, "]Not found" 
            else:
                print "props.getProperty, [", proName, "] Value ", val
        return val
        


   
