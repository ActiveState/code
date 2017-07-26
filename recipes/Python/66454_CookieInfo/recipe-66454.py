import string, sys

true, false = 1, 0

class Cookie:
	Url = ""
	Data1 = ""
	Data2 = ""
	Data3 = ""
	Data4 = ""
	Data5 = ""

	# construct the cookie object
	def __init__(self, cookieInfo):	
		self.Url   = cookieInfo[0]
		self.Data1 = cookieInfo[1]
		self.Data2 = cookieInfo[2]
		self.Data3 = cookieInfo[3]
		self.Data4 = cookieInfo[4]
		self.Data5 = cookieInfo[5]

	# Get statements (pretend the data is private) 
	def getUrl(self):   return self.Url
	def getData1(self): return self.Data1
	def getData2(self): return self.Data2
	def getData3(self): return self.Data3
	def getData4(self): return self.Data4
	def getData5(self): return self.Data5
				
	# generate SQL for the cookie
	def generateSQL(self):
		sql = "INSERT INTO Cookie (Url,Data1,Data2,Data3,Data4,Data5)"
		sql += " VALUES ('"+self.Url+"','"+self.Data1+"','"+self.Data2+"','"+self.Data3+"','"
                sql += self.Data4+"','"+self.Data5+"');"
		return sql

	# generate XML for the cookie
	def generateXML(self):
		xml = "<cookie url='"+self.Url+"' data1='"+self.Data1+"' data2='"+self.Data2
                xml+= "' data3='"+self.Data3+"' data4='"+self.Data4+"' data5='"+self.Data5+"'/>"
		return xml

class CookieInfo:
	rawCookieContent = ""
	cookies = []
	cookieSeperator = "	"

	# Construct the CookieInfo object.
	def __init__(self, cookiePathName):	
		cookieFile = open(cookiePathName, "r")
		self.rawCookieContent = cookieFile.readlines()
		cookieFile.close()

		for line in self.rawCookieContent:
			if line[0:1] == '#':
				pass
			elif line[0:1] == '\n':
				pass
			else:
				self.cookies.append(Cookie(line.split(self.cookieSeperator)))
				

	# Returns the amount of cookies present in the file
	def count(self):
		return len(self.cookies)

	# Find a cookie by its URL and return a Cookie object, returns "" on fail
	def findCookieByURL(self, url):
		for cookie in self.cookies:
			if cookie.getUrl() == url:
				return cookie
		else: return false

	# Find an array of Cookie objects that contain the given string
	def findCookiesByString(self, str):
			string_find = string.find
			string_join = string.join
			results = []
			for c in self.cookies:
				atrs = [c.getUrl(),c.getData1(),c.getData2(), c.getData3(),c.getData4(),c.getData5()]
				if string_find(string_join(atrs, " "), str) != -1:
					results.append(c)

			return results

	# Return SQL for all the cookies
	
	def returnAllCookiesInSQL(self):
		sql = ""
		for cookie in self.cookies:
			sql += cookie.generateSQL + "\n"

	# Return XML for all the cookies

	def returnAllCookiesInXML(self):
		xml = "<?xml version='1.0' ?>\n\n<cookies>\n"
		for cookie in self.cookies:
			xml += cookie.generateXML + "\n"
		xml += "\n</cookies>"
	


# test/sample code (modify for your particular cookies file)

c = CookieInfo("cookies.txt")
print "You have: " + str(c.count()) + " cookies!"

# prints out 3 data element from www.chapters.ca's cookie 
cookie = c.findCookieByURL("www.chapters.ca")

if cookie != false:
	print "Here is the 3th piece of data from the cookie made by www.chapters.ca: " + cookie.getData3()
else:
	print "The URL you have provided doesn't exist in your cookies file!"

# prints out the url's of all cookies with "mark" in them
print "Here are the url's of the cookies that have 'mail' somewhere within their content: "
for cookie in c.findCookiesByString("mail"):
	print cookie.getUrl()
	
# prints out the sql and xml for the www.chapters.ca cookie
cookie = c.findCookieByURL("www.chapters.ca")
print "Here is the SQL for the www.chapters.ca cookie: " + cookie.generateSQL()
print "Here is the XML for the www.chapters.ca cookie: " + cookie.generateXML()
