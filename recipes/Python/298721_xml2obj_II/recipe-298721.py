#!/usr/bin/env python


"""
Program:		XML Routines

Description:	This provides functions and classes to read an XML file building
				a tree of the data file's elements and attributes (to be added!).

Notes:
	--	Think about any of the following:
		--	Read an xml file using xmlData then parse with an LL1 type parser.
		--	Look up MacOSX schema for arrays etc.
		
History:
  2004/10/04	Added "return None" to getFirstChildByName().  Added class to
  				visit the Tree rather than having it embedded in the node
  				class which is a cleaner implementation.

!!! USE AT YOUR OWN RISK !!!
"""

__version__ = 1.0
__license__ = "none"




######################################################################
#								Imports
######################################################################

import		os
import		sys
import		optparse
import		string
import		xml.sax



######################################################################
#							Global Data
######################################################################

# Flags
fDebug = 0
fVerbose  = 0



		
######################################################################
#						set the Debug Flag.
######################################################################

def			setDebug( fValue ):
	"""Set the fDebug flag."""
	global		fDebug

	if fValue:
		fDebug = 1
	else:
		fDebug = 0



######################################################################
#				Read an XML file building a database tree.
######################################################################

# NOTE:		Currently, this system does not handle XML Attributes!

#---------------------------------------------------------------------
#							XML Element Class
#---------------------------------------------------------------------

class		xmlElement:

	def			__init__( self, name, parent, dictAttributes ):
		self.data = None
		self.name = name
		self.parent = parent
		self.dictAttributes = dictAttributes
		self.listChildren = [ ]
		self.dictData = { }

		
	def			__str__( self ):
		szStr = '%s' % (self.name)
		if self.dictAttributes:
			szStr += "%s" % (self.dictAttributes)
		if self.data:
			szStr += ": %s\n" % (self.data)
		else:
			szStr += "\n"
		return szStr

		
	def			addChild( self, node ):
		self.listChildren.append( node )


	def			getAttribute( self, name ):
		return self.dictAttributes[ name ]


	def			getAttributeNames( self ):
		return self.dictAttributes.keys( )


	def			getChildren( self ):
		return self.listChildren
		

	def			getData( self ):
		return self.data
		

	def			getFirstChildByName( self, name ):
		for oChild in self.iterChildrenByName( name ):
			return oChild
		return None
		

	def			getName( self ):
		return self.name
		

	def			hasChildByName( self, name ):
		for oChild in self.iterChildrenByName( name ):
			return 1
		return 0

	def			iterChildren( self ):
		iCur = 0
		while iCur < len( self.listChildren ):
			oChild = self.listChildren[iCur]
			yield oChild
			iCur = iCur + 1
		return
		

	def			iterChildrenByName( self, name ):
		iCur = 0
		while iCur < len( self.listChildren ):
			oChild = self.listChildren[iCur]
			if name == oChild.name:
				yield oChild
			iCur = iCur + 1
		return
		

	def			numChildren( self ):
		return len( self.listChildren )
		

	def			setData( self, data ):

		if string.strip( data ):
			data = data.encode( )
			self.data = data



#---------------------------------------------------------------------
#						XML Element Handler Class
#---------------------------------------------------------------------

class		xmlHandler(xml.sax.ContentHandler):

	def			__init__( self ):
		xml.sax.ContentHandler.__init__( self )
		self.iLevel = 0
		self.listKeys = [ ]
		self.listDataStack = [ xmlElement( u'root', None, None ) ]

		
	def			startElement( self, name, oAttributes ):
		'SAX start element even handler'
		global		fDebug
		
		if fDebug:
			print "startElement(",name.encode(),")"
		attr={ }
		for oKey in oAttributes.getNames( ):
			oData = oAttributes.getValue( oKey )
			if string.strip( oKey ):
				key = oKey.encode( )
				data = oData.strip( )
				attr[key] = data.encode( )
		parent = self.listDataStack[ -1 ]
		node = xmlElement( name.encode(), parent, attr )
		if parent is not None:
			parent.addChild( node )
		self.listDataStack.append( node )
		self.data = ''

		
	def			characters( self, data ):
		'SAX character data event handler'

		if string.strip( data ):
			data = data.encode( )
			self.data += data

		
	def			endElement( self, name ):
		'SAX end element event handler'
		global		fDebug
		
		if fDebug:
			print "endElement(",name,")"

		curData = self.listDataStack.pop( )
		curData.setData( self.data )
		self.data = ''

		
	def			xmlRoot( self ):
		return self.listDataStack[0]



#---------------------------------------------------------------------
#					Read an XML file function.
#---------------------------------------------------------------------

def			readXmlFile( szFileName ):
	" Read in the xml file and build a database tree."

	# Parse the xml file.	
	fileParser = xml.sax.make_parser( )
	fileParser.setFeature( xml.sax.handler.feature_namespaces, 0 ) # Turn off namespaces.
	curHandler = xmlHandler( )
	fileParser.setContentHandler( curHandler )
	fileIn = open( szFileName, 'r' )
	fileParser.parse( fileIn )
	fileIn.close( )
	xmlRoot = curHandler.xmlRoot( )
	return xmlRoot
		
		
#---------------------------------------------------------------------
#							XML Visit Class
#---------------------------------------------------------------------

class		xmlVisit:

	def			_depthFirst( self, curNode ):
		"""	This is a recursive method and therefore has a Python limitation
			of only being able to recurse 1000 times (ie 1000 levels of the
			tree).
		"""
		iRc = self.visitNode( curNode )
		if iRc:
			return iRc
		iRc = self.startChildren( curNode )
		listChildren = curNode.getChildren( )
		for curChild in listChildren:
			iRc = self._depthFirst( curChild )
			if iRc:
				return iRc
		iRc = self.endChildren( curNode )


	def			depthFirst( self, curNode ):
		self._depthFirst( curNode )
		
		
	def			endChildren( self, curNode ):
		""" called when a node's children have been processed.  curNode is the
			node that owns the children.
			Override this if necessary
		"""
		pass


	def			startChildren( self, curNode ):
		""" called when a node's children are about to be processed.  curNode is the
			node that owns the children.
			Override this if necessary
		"""
		pass


	def			visitNode( self, curNode ):
		" called when a node is to be processed. Override this if necessary"
		pass




#---------------------------------------------------------------------
#					Convert the XML Tree to a string.
#---------------------------------------------------------------------

class		xmlTree2String(xmlVisit):

	def			endChildren( self, curNode ):
		" convert the xml tree to a string. "

		self.iIndent -= 2


	def			convert( self, xmlRoot ):
		""" convert the xml tree to a string.
		"""

		# Visit each node adding it to the string.
		self.szString = ''
		self.iIndent = 0
		self.depthFirst( xmlRoot ) 
		return self.szString
		
		
	def			visitNode( self, curNode ):
		" convert the xml tree to a string. "

		s = self.iIndent * ' '
		s += "%s" % (curNode.name)
		if curNode.dictAttributes:
			s += "%s" % (curNode.dictAttributes)
		if curNode.data:
			s += ": %s\n" % (curNode.data)
		else:
			s += "\n"
		self.szString += s
		self.iIndent += 2
		return 0


#---------------------------------------------------------------------
#					Convert the XML Tree to a string.
#---------------------------------------------------------------------

class		xmlTree2KeyedData(xmlVisit):

	def			endChildren( self, curNode ):
		self.listKeys.pop( )


	def			visitNode( self, curNode ):
		self.listKeys.append( curNode.name )
		if curNode.data:
			# Build the key.
			newKey = '_'.join( self.listKeys )
			# Add the key and data to the nodeAccum.
			if newKey:
				self.nodeAccum.__dict__[newKey] = curNode.data
		return 0


	def			makeKeyedData( self, nodeAccum, xmlRoot ):
		self.listKeys = [ ]
		self.nodeAccum = nodeAccum
		self.depthFirst( xmlRoot ) 
		return self.nodeAccum
		

				

######################################################################
#						Command-line interface
######################################################################


def			main( argV=None ):
	"Command-line interface."
	global		fDebug
	global		fVerbose
	global		listComputers

	if argV is None:
		argV = sys.argv

	# Parse the command line.		
	szUsage = "usage: %prog [options] arg1 arg2 ..."
	oCmdPrs = optparse.OptionParser( usage=szUsage )
	oCmdPrs.add_option( "-d", "--debug", action="store_true",
						dest="fDebug", default=False,
						help="Set debug mode"
	)
	(oOptions, oArgs) = oCmdPrs.parse_args( argV )
	if oOptions.fDebug:
		fDebug = 1
		fahData.setDebug( )
		print "In DEBUG Mode..."

	# Build the XML Tree.
	xmlRoot = readXmlFile( argV[1] )
	
	# Now convert it to a string and print that.
	oTree2String = xmlTree2String( )
	szString = oTree2String.convert( xmlRoot )
	print szString
		
	return 0




if __name__ == "__main__":
	sys.exit( main( sys.argv ) or 0 )
