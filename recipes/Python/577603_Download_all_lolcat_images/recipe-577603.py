#!/usr/bin/env python
 
# Retrieve lolcat images from icanhascheezburger.com, starting from the oldest image
# Author: Rahul Anand <rahulanand.fine@gmail.com> | Homepage: http://eternalthinker.blogspot.com/

import urllib2, urllib
import re, os

file("log.txt", "w").close() # clear current log
# config string is in the format: lastKnownMaxPages/lastParsedPage/imgCountSoFar
config = [int(item) for item in file("lolconfig.txt", "r").read().split('/')]
limitPage = config[0]
lastPage = config[1]
imgCount = config[2]

urlContent = urllib2.urlopen('http://icanhascheezburger.com/').read()
limitPageOriginal = int(re.findall(""">Next.*?page/(.*?)/">Last<""", urlContent)[0]) # Get the current max pages
lastPage += limitPageOriginal - limitPage # Alter current page to account for new pages added to the website
limitPage = str(limitPageOriginal) + '/'

# Start each page from the oldest to the latest
while lastPage >= 1:
	logString = limitPage + str(lastPage) + '/' + str(imgCount)
		
	config = file("lolconfig.txt", "w")
	config.write(logString) # Write the config log about current parsing 
	config.close()	
	
	log = file("log.txt", "a")
	log.write(logString + '\n') # Write the log
	log.close()
	
	folderName = './lolcats' + str(imgCount/300) + '/' # Make new folder for every 300 images
	if not os.path.exists(folderName): 
		os.mkdir(folderName)
		print "Now downloading to", folderName.rsplit('/', 2)[1]
	
	url = "http://icanhascheezburger.com/page/" + str(lastPage)
	urlContent = urllib2.urlopen(url).read()
	print 'Page:', lastPage
	lastPage -= 1
	
	# Parse and download images from current page
	imgUrls = re.findall("""<div class="md"><p.*?img .*?src=["'](.*?)["']""", urlContent, re.DOTALL) # el regex
	imgUrls = imgUrls[::-1] # The bottom image is the oldest in a page. So reverse the parsed list
	for i in range(0, len(imgUrls) ):
	    imgUrl = imgUrls[i] 
	    fileName = str(imgCount) + ".jpg"
	    imgCount += 1 	
	    try:
	    	print "   *", fileName
		urllib.urlretrieve(imgUrl, folderName + fileName)        
	    except:
		print "Error retrieving image", fileName # :'(
		
		
		
		
