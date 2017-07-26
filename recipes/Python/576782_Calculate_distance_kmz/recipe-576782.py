#!/usr/bin/env python
# -*- coding: utf8 -*-

__version__ = '$Id: kmz2dist.py 609 2009-06-01 05:04:52Z mn $'
# author: Michal Niklas

"""
Calculates distance in kilometers from points saved in .kmz file.
Such files can be created by Google Earth
look at:
http://code.google.com/intl/pl-PL/apis/kml/documentation/kmlreference.html

Recipe by Bartek Górny is used to calculate distance between 2 points:
Recipe 576779: Calculating distance between two geographic points
http://code.activestate.com/recipes/576779/
"""

import sys
import zipfile
import glob
from xml.dom import minidom

# save Recipe 576779: Calculating distance between two geographic points
# http://code.activestate.com/recipes/576779/
# as distance
import distance


def get_distance(coordinates_str):
	"""gets distance of one path from coordinates string in form of:
	14.81363432237944,53.57016581501523,0 14.81411766813742,53.56923005549378,0 14.81880340335202,53.56879451890311 ...
	look at:
		http://code.google.com/intl/pl-PL/apis/kml/documentation/kmlreference.html#coordinates
	"""
	sum_distance = 0.0
	arr = []
	coordinates = []
	if ' ' in coordinates_str:
		arr = coordinates_str.split(' ')
	if len(arr) > 1:
		for s in arr:
			if ',' in s:
				pt = s.split(',')
				pos_latt = (float(pt[0].strip()), 0, 0)
				pos_long = (float(pt[1].strip()), 0, 0)
				position = (pos_latt, pos_long)
				coordinates.append(position)
	if coordinates:
		for i in range(len(coordinates) - 1):
			start = coordinates[i]
			stop = coordinates[i + 1]
			sum_distance += distance.points2distance(start, stop)
	return sum_distance


def show_distance(fname):
	"""calculates distance from points saved in doc.kml which is part of .kmz
	   zip archive file"""
	path_cnt = 0
	zf = zipfile.ZipFile(fname, 'r')
	for fn in zf.namelist():
		if fn.endswith('.kml'):
			content = zf.read(fn)
			xmldoc = minidom.parseString(content)
			placemarks = xmldoc.getElementsByTagName('Placemark')
			for placemark in placemarks:
				name = placemark.getElementsByTagName('name')
				if name:
					name = name[0].firstChild.data.strip()
					coordinates = placemark.getElementsByTagName('coordinates')
					if coordinates:
						coordinates = coordinates[0].firstChild.data.strip()
						if coordinates:
							distance_km = get_distance(coordinates)
							if distance_km > 0.0:
								if path_cnt == 0:
									print '\n%s:' % (fname)
								path_cnt += 1
								print('\t%s\t%5.2f' % (name, distance_km))
	return path_cnt


def main():
	"""show .kmz file name and distance in kilometers"""
	fnames = glob.glob('*.kmz')
	if not fnames:
		print('No *.kmz files found')
	else:
		for fname in fnames:
			show_distance(fname)


if __name__ == '__main__':
	if '--version' in sys.argv:
		print(__version__)
	else:
		main()
