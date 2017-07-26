class Ini:
	"Contains all that is needed to write an INI file"
	
	def __init__(self):
		"You can add here the begin of your INI file"
		self.file = ""
		
	def addsection(self, section):
		"Add a section delimiter to the INI file"
		self.file += "\n\n[" + section + "]"
		
	def addkey(self, key, value):
		"Writes a string to the INI file"
		self.file += "\n" + key + "=" + value
		#print key+"="+value ,"[OK - Ajouté]"
		
	def comment(self, comm):
		"Writes a comment to the INI file"
		self.file += "\n ;" + comment
		
	def verb(self, str):
		"Write all that is given as argument to INI file"
		self.file += str
		
	def show(self, action="return"):
		"""Prints or returns the contents of the INI file
		Usage: action='return' returns the contents
		          action='print' prints the contents"""
		if action == "return":
			return self.file
		elif action == "print"
			print self.file
