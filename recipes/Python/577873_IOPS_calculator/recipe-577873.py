#!/usr/bin/python

import os, time, math

run_tests = 3

devices = os.listdir('/sys/block/')
check_devices = []

reads = {}
writes = {}

for dev in devices:
	if dev.startswith('md') or dev.startswith('sd') or dev.startswith('hd'):
		check_devices.append(dev)
		reads[dev] = []
		writes[dev] = []

check_devices = sorted(check_devices)

for t in range(run_tests + 1):
	for dev in check_devices:
		file_data = open('/sys/block/%s/stat' % dev).readline().strip().split(' ')
		clean = []
		for num in file_data:
			if num != '':
				clean.append(int(num))
		
		reads[dev].append(clean[0])
		writes[dev].append(clean[4])
	
	time.sleep(1)

print "Device        Read        Write"
print "--------------------------------------"
for dev in check_devices:
	clean_reads = []
	reads[dev].reverse()
	for test, result in enumerate(reads[dev]):
		if test > 0:
			clean_reads.append(float(reads[dev][test - 1] - result))
	
	rops = int(math.ceil(sum(clean_reads) / len(clean_reads)))
	
	clean_writes = []
	writes[dev].reverse()
	for test, result in enumerate(writes[dev]):
		if test > 0:
			clean_writes.append(float(writes[dev][test - 1] - result))
	
	wops = int(math.ceil(sum(clean_writes) / len(clean_writes)))
	
	print "%s %s %s" % (dev.ljust(13), repr(rops).ljust(11), repr(wops))
