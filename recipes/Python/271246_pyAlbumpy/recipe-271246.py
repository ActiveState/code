"""
 This is a simple command-line based, lightweight Python script to
 create an image album.

 Copyright 2004 Premshree Pillai. All rights reserved.
 <http://www.qiksearch.com/>

 The script takes the following five inputs:
 	1. Directory name: This is the directory from where the
 	   images are read from
  	2. Album title <optional>: This title will appear on
 	   each of the HTML files created
 	3. Thumbnail scaling factor: This is a value less than
 	   1.0 (e.g., 0.2., 0.3, etc). The size of the thumbnail
 	   images created will be the scaling factor times the
 	   original image size
 	4. Image scaling factor: This is again a value less than
 	   or equal to 1.0. Images created using this factor appear
 	   on the HTMLs of individual images
 	5. Option to Add EXIF information
 
 The script creates the following three directories within the
 image directory:
 	1. thumbnails
 	2. images
 	3. htmls
 
 The album can be viewed by running the index.htm file

 27-FEB-04 pyAlbum.py released.
 06-APR-04 Added thumbnail support.
 	   Added scaling for individual image pages.
 	   Now requires PIL (http://www.pythonware.com/products/pil)
 11-APR-04 Implemented pyAlbum as a class.
 	   Added optional EXIF support.
 	   Requires EXIF.py
	   (http://home.cfl.rr.com/genecash/digital_camera/EXIF.py)
"""

class pyAlbum:

	def __init__(self, dirName, title, scale1, scale2, exifFlag = 1):
		self.count = 0
		self.dirName = dirName
		self.title = title
		self.scale1 = scale1
		self.scale2 = scale2
		self.exifFlag = exifFlag
		self.slideName = "htmls"
	
	def retPrevFile(self, index):
		if(index == 0):
			return "<span class=\"no_go\">&laquo; <b>No Previous</b></span>"
		else:
			str = """&laquo; <a href="%s">Previous</a>""" % (self.slideName + self.files[self.count - 1] + '.htm')
			return str
	
	def retNextFile(self, index):
		if(index == len(self.files) - 1):
			return "<span class=\"no_go\"><b>No Next</b> &raquo;</span>"
		else:
			str = """<a href="%s">Next</a> &raquo;""" % (self.slideName + self.files[self.count + 1] + '.htm')
			return str
	
	def retPipe(self, index):
		return " | "
		if(index > 0 and index < len(self.files) - 1):
			return " | "
		else:
			return ""
	
	def getScale1(self):
		os.chdir(self.dirName)
		os.mkdir(self.slideName)
		global scale1
		scale1 = raw_input("Enter scaling factor for Thumbnails: ")
		try:
			scale1 = float(scale1)
		except ValueError:
			print "Invalid value entered!"
			getScale1()
		if scale1 > 1.0:
			print "Scaling factor should be less than 1!"
			getScale1()
	
	def getScale2():
		global scale2
		scale2 = raw_input("Enter scaling factor for Images: ")
		try:
			scale2 = float(scale2)
		except ValueError:
			print "Invalid value entered!"
			getScale2()
		if scale2 > 1.0:
			print "Scaling factor should be less than 1!"
			getScale2()
	
	def doFiles(self):
		self.files = []
		for x in os.listdir(self.dirName):
			os.chdir(self.dirName)
			if(os.path.isfile(x)):
				self.files.append(x)
	
	def createThumbnails(self):
		# Create thumbnails
		self.tnDir = "thumbnails"
		os.mkdir(self.tnDir)
		for x in os.listdir(self.dirName):
			os.chdir(self.dirName)
			if(os.path.isfile(x)):
				image_size = Image.open(x).size
				width = int(image_size[0] * self.scale1)
				height = int(image_size[1] * self.scale1)
				img = Image.open(x)
				img2 = img.resize([width,height],2)
				os.chdir(self.tnDir)
				img2.save(x)
	
	def createImages(self):
		# Create images for display in the files
		os.chdir(self.dirName)
		self.imagesDir = "images"
		os.mkdir(self.imagesDir)
		for x in os.listdir(self.dirName):
			os.chdir(self.dirName)
			if(os.path.isfile(x)):
				image_size = Image.open(x).size
				width = int(image_size[0] * self.scale2)
				height = int(image_size[1] * self.scale2)
				img = Image.open(x)
				img2 = img.resize([width,height],2)
				os.chdir(self.imagesDir)
				img2.save(x)
	
	def createCSS(self):
		# Create CSS file
		os.chdir(self.dirName)
		self.CSSFile = "styles.css"
		os.mkdir(self.slideName)
		os.chdir(self.slideName)
		fp = open(self.CSSFile,"w")
		temp = """
			body	{font-family:Verdana, Arial, Trebuchet MS; font-size:10pt; margin-left:0px; margin-right:0px; margin-top:0px}
			td	{font-family:Verdana, Arial, Trebuchet MS; font-size:8pt}
			h2	{font-family: Trebuchet MS, Arial, Verdana; background:#000000; color:#FFFFFF; padding:10px}
			h4	{font-family: Trebuchet MS, Arial, Verdana; color:#CCCCCC}
			a	{font-family:Verdana, Arial, Trebuchet MS; font-size:10pt; font-weight:bold; text-decoration:underline}
			a:visited{color:#FF0000}
			a:hover	{font-family:Verdana, Arial, Trebuchet MS; font-size:10pt; font-weight:bold; text-decoration:none; background:#CCCCFF;}
			.no_go	{font-family:Verdana, Arial, Trebuchet MS; font-size:10pt; color:#CCCCCC}
		img	{border:#000000 solid 1px}
		"""
		fp.write(temp)
		fp.close()
	
	def createIndex(self):
		# Create the index file
		self.indexFile = "index.htm"
		os.chdir(self.dirName)
		fp = open(self.indexFile,"w")
		temp = """<html>
			<head>
				<title>%s</title>
				<link rel="stylesheet" href="%s/styles.css">
			</head>
			<body>
			<center><h2>%s</h2></center>
			<table align="center"><tr>
			""" % (self.title, self.slideName, self.title)
		self.count = 0
		for x in self.files:
			image_size = Image.open(x).size
			file_size = int(os.stat(x)[6]/1024)
			width = int(image_size[0])
			height = int(image_size[1])
			if self.count == 0 :
				temp = temp + "</tr><tr>"
			temp = temp + "<td valign=\"bottom\" align=\"center\" style=\"text-align:center\"><a href=\"" + self.slideName + "/" + self.slideName + x + ".htm" + "\"><img src=\"" + self.tnDir + "/" + x + "\"><br>" + x + "</a><br><span style=\"color:gray\"><small>" + str(width) + "&times;" + str(height) + ", " + str(file_size) + "kB</small></span> </td>"
			self.count = self.count + 1
			if self.count == 4:
				self.count = 0
		temp = temp + "</tr></table>\n<p style=\"padding-left:10px\"><small>Created using <a href=\"http://premshree.resource-locator.com/python/pyAlbum.py\"><small>pyAlbum.py</small></a></small></p>\n</body>\n</html>"
		fp.write(temp)
		fp.close()

	def exifInfo(self, fileName):
		os.chdir(self.dirName)
		if not(self.exifFlag):
			return ""
		import exif
		file = open(fileName,"rb")
		data = exif.process_file(file)
		if not data:
			return "No EXIF Information available."
		x = data.keys()
		x.sort()
		count = 0
		vals = [0,4,9,11,12,15,17,18,22,25,38,39,41,43,45]
		"""
		0  - ApertureValue
		4  - DateTimeDigitized
		9  - ExposureBiasValue
		11 - ExposureProgram
		12 - ExposureTime
		15 - Flash
		17 - FocalLength
		18 - ISOSpeedRatings
		22 - MeteringMode
		25 - ShutterSpeedValue
		38 - Image Make
		39 - Image Model
		41 - Image ResolutionUnit
		43 - Image XResolution
		45 - Image YResolution
		"""
		retVal = []
		for i in x:
			if count in vals:        
				#print 'error', i, '"', data[i], '"'
				retVal.append(data[i])
			count = count + 1
		retValStr = []
		for i in retVal:
			retValStr.append(i.__str__())
		date = retValStr[1]
		date = date.split(" ")
		time = date[1]
		date = date[0]
		year = date.split(":")[0]
		month = int(date.split(":")[1])
		day = date.split(":")[2]
		hr = int(time.split(":")[0])
		min = time.split(":")[1]
		am_pm = "AM"
		if hr >= 12:
			am_pm = "PM"
		if hr > 12:
			hr = hr - 12
		hr = str(hr)
		monthArr = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		date = monthArr[month - 1] + " " + day + ", " + year
		time = hr + ":" + min + " " + am_pm
		out = """<table align="center" cellpadding="8" cellspacing="0" border="1" style="border: 1; text-align: center; margin-top: 20px;">
			<tr>
				<td colspan="4" align="center" style="text-align: center;">
					<strong>Photographed on %s at %s</strong>	
				</td>
			</tr>
			<tr>
				<td><strong>Aperture</strong></td>
				<td>%s</td>
				<td><strong>Exposure bias</strong></td>
				<td>%s</td>
			</tr>
			<tr>
				<td><strong>Exposure program</strong></td>
				<td>%s</td>
				<td><strong>Exposure time</strong></td>
				<td>%s</td>
			</tr>
			<tr>
				<td><strong>Flash</strong></td>
				<td>%s</td>
				<td><strong>Focal length</strong></td>
				<td>%s</td>
			</tr>
			<tr>
				<td><strong>ISO speed ratings</strong></td>
				<td>%s</td>
				<td><strong>Light source</strong></td>
				<td>-</td>
			</tr>
			<tr>
				<td><strong>Make</strong></td>
				<td>%s</td>
				<td><strong>Metering mode</strong></td>
				<td>%s</td>
			</tr>
			<tr>
				<td><strong>Model</strong></td>
				<td>%s</td>
				<td><strong>Resolution unit</strong></td>
				<td>%s</td>
			</tr>
			<tr>
				<td><strong>Shot resolution</strong></td>
				<td>-</td>
				<td><strong>Shutter speed</strong></td>
				<td>%s</td>
			</tr>
			<tr>
				<td><strong>X resolution</strong></td>
				<td>%s</td>
				<td><strong>Y resolution</strong></td>
				<td>%s</td>
			</tr>
		</table>""" % (date, time, retValStr[0], retValStr[2], retValStr[3], retValStr[4], retValStr[5], retValStr[6], retValStr[7], retValStr[10], retValStr[8], retValStr[11], retValStr[12], retValStr[9], retValStr[13], retValStr[14])
		return out
	
	def createHTMLs(self):
		# Create HTML files
		os.chdir(self.dirName)
		os.chdir(self.slideName)
		self.count = 0
		for x in self.files:
			os.chdir(self.dirName)
			file_size = int(os.stat(x)[6]/1024)
			os.chdir(self.slideName)
			file = self.slideName + x + '.htm'
			fp = open(file,"w")
			temp = """<html>
				<head>
					<title>%s</title>
					<link rel="stylesheet" href="styles.css">
				</head>
				<body>
				<center><h2>%s</h2></center>
				<center><h4>%s (%s/%s)</h4></center>
				<center><a href="../%s"><img src="../images/%s"></a></center>
				<center><br><a href="../%s"><small>Download full-size image (%s kB)</small></a></center>
				<center><br><b>%s%s<a href="../index.htm">Index</a>%s%s</b></center>
				%s
				<p style="padding-left:10px"><small>Created using <a href="http://premshree.resource-locator.com/python/pyAlbum.py"><small>pyAlbum.py</small></a></small></p>
				</body>
				</html>
			""" % (self.title, self.title, x, self.count + 1, len(self.files), x, x, x, file_size, self.retPrevFile(self.count), self.retPipe(self.count), self.retPipe(self.count), self.retNextFile(self.count),self.exifInfo(x))
			fp.write(temp)
			fp.close()
			self.count = self.count + 1
	
	def exit(self):
		# Done!
		print "\n", "Album created!"
		print "Press <enter> to exit..."
		if(raw_input()):
			exit

if __name__ == '__main__':

	import os
	import sys
	from PIL import Image

	def getDir():
		global dirName
		dirName = raw_input("Enter the directory to read images from (absolute path): ")
		if(not(os.path.isdir(dirName))):
			print "Directory does not exist!"
			getDir()
	getDir()

	title = raw_input("Enter a title for the album: ")

	def getScale1():
		global scale1
		scale1 = raw_input("Enter scaling factor for Thumbnails: ")
		try:
			scale1 = float(scale1)
		except ValueError:
			print "Invalid value entered!"
			getScale1()
		if scale1 > 1.0:
			print "Scaling factor should be less than 1!"
			getScale1()
	getScale1()

	def getScale2():
		global scale2
		scale2 = raw_input("Enter scaling factor for Images: ")
		try:
			scale2 = float(scale2)
		except ValueError:
			print "Invalid value entered!"
			getScale2()
		if scale2 > 1.0:
			print "Scaling factor should be less than 1!"
			getScale2()
	getScale2()

	def getExif():
		global exifFlag
		exifFlag = raw_input("Add EXIF information (y/n)? ")
		if exifFlag in ['y', 'n']:
			if exifFlag == 'y':
				exifFlag = 1
			else:
				exifFlag = 0
		else:
			getExif()
	getExif()

	# Wait...
	print "\nPlease wait a few moments..."

	album = pyAlbum(dirName, title, scale1, scale2, exifFlag)
	album.doFiles()
	album.createThumbnails()
	album.createImages()
	album.createCSS()
	album.createIndex()
	album.createHTMLs()
	album.exit()
