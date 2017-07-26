""" qemu-nbd wrapper """

import os

def list_devices():
	devices = []
	for dev in os.listdir('/dev'):
		if dev.startswith('nbd'):
			# see if it's a partition
			if len(dev.split('p')) == 1:
				devices.append(dev)
	
	return devices

def find_available():
	devices = []
	busy = []
	for x in os.popen("cat /proc/partitions | grep nbd | awk '{print $4}'").readlines():
		busy.append(x.strip())
		
	for d in list_devices():
		if not d in busy:
			devices.append(d)
	
	return devices

def connect(image_file, read_only=True):
	image_file = os.path.realpath(image_file)
	
	if not os.path.exists(image_file):
		return False
	
	devices = find_available()
	if len(devices) == 0:
		return False
	
	dev = devices[0]
	
	if read_only:
		read_only = '-r'
	else:
		read_only = ''
		
	os.popen('qemu-nbd -c /dev/%s %s %s' % (dev, read_only, image_file))
	
	return dev

def disconnect(dev=None):
	umount(dev)
	
	if dev == None:
		for dev in list_devices():
			disconnect(dev)
	else:
		os.popen('qemu-nbd -d /dev/%s' % dev)

def mount(dev, partition=1, path=None):
	full_dev_path = '/dev/%sp%s' % (dev, partition)
	
	if path == None:
		import tempfile
		path = tempfile.mkdtemp()
	
	os.popen('mount %s %s' % (full_dev_path, path))
	
	return path

def find_mount(dev=None):
	if dev == None:
		mounts = []
		for dev in list_devices():
			m = find_mount(dev)
			if m != None and m not in mounts:
				mounts.append(m)
		
		return mounts
	
	else:
		mount = None
		
		sys_mount = os.popen('mount | grep %s' % dev).readline().strip().split(' ')
		if len(sys_mount) > 1:
			mount = {
				'dev': sys_mount[0],
				'mount': sys_mount[2],
				'type': sys_mount[3]
			}
		
		return mount
	
def umount(dev=None):
	m = find_mount(dev)
	
	if dev == None:
		for x in m:
			os.popen('umount %s' % x['mount'])
	elif m != None:
		os.popen('umount %s' % m['mount'])
