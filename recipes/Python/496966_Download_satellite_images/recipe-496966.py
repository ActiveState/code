#! /usr/bin/env python

import urllib

SAT_ZOOM_LEVEL = 0.0001389 #Like in request form

def retrieveImage(coordinates, image_size, name):
	"""Retrieve satellite images from the Nasa's site
	
	coordinates: tuple (longitude, latitude) in decimal degrees
	image_size: tuple (width, height)
	name: output filename
	"""

	request1 = "http://onearth.jpl.nasa.gov/landsat.cgi?" \
		"zoom=%f&x0=%f&y0=%f&x=%i&y=%i&action=pan&layer=modis%%252Cglobal_mosaic&pwidth=%i&pheight=%i" % \
		(SAT_ZOOM_LEVEL,
		coordinates[0],
		coordinates[1],
		image_size[0]/2,
		image_size[1]/2,
		image_size[0],
		image_size[1])
	for line in urllib.urlopen(request1):
		if line.startswith("<td align=left><input type=image src="):
			request2 = "http://onearth.jpl.nasa.gov/%s" % (line.split("\"")[1],)
			break
	urllib.urlretrieve(request2, name)

if __name__ == '__main__':
	retrieveImage((60.7376856, 56.5757572), (800,600), "test.jpg")
	# Specified coordinates is the point accurately at the image center
