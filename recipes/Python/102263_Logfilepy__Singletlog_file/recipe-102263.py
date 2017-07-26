import	os, os.path, sys, time

class	Log:

	class	Log_File:
		def	__init__(self, fPath = os.getcwd(), fName = "log.txt"):
			"""	I intend to add some customization features to this,
					e.g., allowing the log file's name and directory to be
					specified, but that will be later
			"""
			self.fpath	=	fPath		#	the class variable, file path
			self.fname	=	fName		#	the class variable, file name
			self.log_file	=	""	#	the class variable, log file
			if	not os.path.isdir(self.fpath):
				self.fpath	=	os.getcwd()
			if	not os.path.isdir(self.fpath):
				sys.stderr.write ("in LogFile initialization\n")
				sys.stderr.write ("  file path set to: <<" + self.fpath + ">>\n")
				sys.stderr.write ("  This appears to not be a valid directory.")
				sys.stderr.write ("  This is a serious internal error")
				fail ("Log file path must be valid")

			if	os.path.isfile(os.path.join(self.fpath, fName)):
				self.fname	=	fName
			else:
				self.fname	=	"log.txt"
			tfName	=	os.path.join(self.fpath, self.fname)
			if	os.path.isfile(tfName):
				size	=	os.path.getsize(tfName)
				if	 size > 65536:
					mode	=	'w+'
				else:
					mode	=	'a+'
			else:
				failIf (os.path.exists(tfName), "file <<" + tfName + ">> exists, "
						+	"but is not a file (possibly a directory?)")
				mode	=	'w+'
			self.log_file	=	open(tfName, mode)
			self.log_file.write(".-=-" * 20 + "\n\n")
			self.log_file.write("log start at: " + time.ctime()
										+ "\n\n")
		
		def	put(self, text = ""):
			if	len(text) > 0:
				self.log_file.write(text)
		
		def	get_id(self):
			return	id(self)
	__log	=	None
	def	__init__(self):
		if	Log.__log == None:
			Log.__log	=	Log.Log_File()
	
	def	get_id(self):
		return	Log.__log.get_id()
	
	def	put(self, text = ""):
		Log.__log.put(text)
	
	def	checkpt(self, text = ""):
		Log.__log.put(time.ctime() + ": " + text + "\n")
	
	def	write(self, text = ""):
		Log.__log.put(text + "\n")
	

if	__name__ == "__main__":
	log_App	=	Log()
	print	"log_App dict::", log_App.__dict__
	print "log_App id = ", log_App.get_id()
	bog_App	=	Log()
	print "log_App id = ", log_App.get_id()
	print "bog_App id = ", bog_App.get_id()
	log_App.write("Once upon a midnight dreary")
	bog_App.write("As I pondered, weak and weary")
	log_App.write("Over many a quaint and curious volumn of forgotten lore")
	bog_App.write("Suddenly there came a tapping")
	log_App.write("As of someone gently rapping")
	log_App.put("\nIn the same line")
	bog_App.put(" I write from both")
	log_App.write(" copies")
