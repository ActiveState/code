debugLevel=0
def setDebugLevel(level):
	global debugLevel
	debugLevel=level
def getDebugLevel():
	return debugLevel
def debugPrint(level,text):
	if level <= debugLevel:
		print text

class fileReaderBase(object):
	def attributesToList(self,prefix,dictionary):
		return [ '%s-%s:%s'%(prefix,key,value) for key,value in dictionary.iteritems()]
	def processLine(self,line):
		rawParam,data=line.split(':',1)
		params=rawParam.split('-',1)
		debugPrint(30,'Found Meta Data: %s'%(params))

		# find an arbitrarily complex function name based on the dashes in the line
		# Look for most specific first and quit trying once we find a function with
		# the appropriate name.
		for i in range(len(params),0,-1):
			functionName='handle_'+'_'.join(params[:i])
			processMethod=getattr(self,functionName,None)
			if processMethod:
				processMethod(data,params)
				return
		
class fileFileData(crosswordReaderBase):
	def __init__(self):
		self.clear()
	def clear(self):
		self.metaAttributes={}
		self.puzzleAttributes={}
		self.grid=[]
        def handle_META(self,data,parameters):
		self.metaAttributes[parameters[-1]]=data
        def handle_PUZZLE(self,data,parameters):
		self.puzzleAttributes[parameters[-1]]=data
        def handle_PUZZLE_clue(self,data,parameters):
		pass
        def handle_PUZZLE_data(self,data,parameters):
		self.grid.append(data)
	def toLines(self):
		retVal=self.attributesToList('META',self.metaAttributes)
		retVal=self.attributesToList('PUZZLE',self.puzzleAttributes)
		retVal.extend(['PUZZLE-data:%s'%data for data in self.grid])
		return retVal
	def getGridLines(self):
		return self.grid
	def setGridLines(self,gridLines):
		self.grid=gridLines

##################

Example file:

META-title:My Title
META-date:date

PUZZLE-across:13
PUZZLE-down:14
PUZZLE-type:American

COMMENT-Use _ for black squares, use * for unknown characters
COMMENT-Use uppercase characters for words you want to seed

PUZZLE-data:_dug_tote_cbs
PUZZLE-data:coco_oval_oat
PUZZLE-data:hold_wire_rbi
PUZZLE-data:EMAILED_cider
PUZZLE-data:___vol_etc___
PUZZLE-data:orcas_gasket_
PUZZLE-data:bee_spar_yowl
PUZZLE-data:indy_rill_nib
PUZZLE-data:_deacon_ousts
PUZZLE-data:___klm_bin___
PUZZLE-data:posse_WISPIER
PUZZLE-data:amt_acid_lone
PUZZLE-data:rna_rime_util
PUZZLE-data:rig_saps_gad_

CLUE-across-1:*Excavated
CLUE-across-4:Big handbag
CLUE-across-8:Truckers Radio
CLUE-down-1:Very bad end
CLUE-down-2:*Home of the bruins
