#!/usr/bin/env python

__version__ = '$Id: exif_redater.py 2294 2014-12-11 10:04:54Z mn $'

USAGE = "exif_redater.py\n\tredate .jpg/.jpeg files according to EXIF data"

"""
Iterates through a directory, reading the EXIF data from each jpg/jpeg file.
Parses the date/time from EXIF data and:
1. if it differs from file modification date/time then changes file date/time
2. moves file to YYYY/YYYY_MM_DD directory

author: Michal Niklas
"""

import os
import os.path
import shutil
import sys
import time
import traceback

try:
	from PIL import Image
except:
	pass

try:
	import exifread
except:
	pass


ALL_CNT = 0
CHANGED_CNT = 0
DEBUG = 0

# which file should be checked
EXTENSIONS = ('.jpg', '.jpeg')

# what tags use to redate file (use first found)
DT_TAGS = ["Image DateTime", "EXIF DateTimeOriginal", "DateTime"]


def log_error(s):
	sys.stderr.write('%s\n' % (s))


def show_fdt(fdt):
	"""human readable format of file modification datetime"""
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(fdt))


def exif_info2time(ts):
	"""changes EXIF date ('2005:10:20 23:22:28') to number of seconds since 1970-01-01"""
	tpl = time.strptime(ts + 'UTC', '%Y:%m:%d %H:%M:%S%Z')
	return time.mktime(tpl)


MAX_DIFF = 130.0


def get_exif_date_exif(jpegfn):
	"""return EXIF datetime using exifread (formerly EXIF)"""
	dt_value = None
	f = open(jpegfn, 'rb')
	try:
		tags = exifread.process_file(f)
		if DEBUG:
			print('tags cnt: %d' % len(tags))
			print('\n'.join(tags))
		for dt_tag in DT_TAGS:
			try:
				dt_value = '%s' % tags[dt_tag]
				if DEBUG:
					print('%s: %s' % (dt_tag, dt_value))
				break
			except:
				continue
		if dt_value:
			exif_time = exif_info2time(dt_value)
			return exif_time
	finally:
		f.close()
	return None


def get_exif_date_pil(jpegfn):
	"""return EXIF datetime using PIL"""
	im = Image.open(jpegfn)
	if hasattr(im, '_getexif'):
		exifdata = im._getexif()
		dt_value = exifdata[0x9003]
		exif_time = exif_info2time(dt_value)
		return exif_time
	return None


def redate_by_exif(fn):
	"""reads EXIF from jpg/jpeg and if file datetime differs from EXIF changes file date"""
	global ALL_CNT, CHANGED_CNT
	ALL_CNT += 1
	exif_time = None
	s = os.stat(fn)
	file_time = s[8]
	if DEBUG:
		print(fn)
	try:
		exif_time = get_exif_date_pil(fn)
	except:
		s1 = traceback.format_exc()
		try:
			exif_time = get_exif_date_exif(fn)
		except:
			s2 = traceback.format_exc()
			print('Something is terribly wrong! Both PIL and exifread raises exception')
			print('-' * 20)
			print(s1)
			print('-' * 20)
			print(s2)
			print('-' * 20)
			print('-' * 20)
	if exif_time:
		dir_n = time.strftime("%Y/%Y_%m_%d", time.gmtime(exif_time))
		try:
			os.makedirs(dir_n)
		except:
			pass
		secs_diff = file_time - exif_time
		print("%s    %s -> %s (%s)" % (fn, show_fdt(file_time), show_fdt(exif_time), dir_n))
		if secs_diff > MAX_DIFF or secs_diff < -MAX_DIFF:
			os.utime(fn, (exif_time, exif_time))
			CHANGED_CNT += 1
		shutil.move(fn, dir_n)


def process_dir(_, dir_name, files):
	"""looks for .jpg/.jpeg file in dir"""
	sys.stdout.write('%-70s\r' % (dir_name))
	for fname in files:
		can_change = False
		fnl = fname.lower()
		for ext in EXTENSIONS:
			if fnl.endswith(ext):
				can_change = True
				break
		if can_change:
			fname = os.path.join(dir_name, fname)
			if os.path.isfile(fname):
				redate_by_exif(fname)


def main():
	os.path.walk('.', process_dir, None)
	print('\nChecked: %d\nChanged %d\n' % (ALL_CNT, CHANGED_CNT))


def test():
	redate_by_exif('grunwald.jpg')


if __name__ == '__main__':
	if '--version' in sys.argv:
		print(__version__)
	elif '--help' in sys.argv:
		print(USAGE)
	elif '--test' in sys.argv:
		test()
	else:
		main()
