def findCloseAddress (ramMapFile, reqAddress):
	"""
	Find similar address in file
	"""
	from sys import maxint as MAXINT
	
	fd = open (ramMapFile, 'r')
	
	foundLine    = ""
	smallestDiff = MAXINT
	
	for line in fd:
		if "SYMBOL TABLE:" in line : 
			break

	for line in fd:
		linePart = line.split()
		if len(linePart) > 0:
			currAddress = int(linePart[0], 16)
			diff        = reqAddress - currAddress
			if diff < smallestDiff and diff >= 0:			
				smallestDiff = diff
				foundLine = ''.join(line)

	print "\nRequired Address : 0x%x" % reqAddress
	print "\nClosest Line :\n%s"	  % foundLine
	print "\nDifference : 0x%x (%d instructions)"  % (smallestDiff,  smallestDiff / 4)	

	
if __name__ == "__main__":
		mapFile = r"C:\default\ram.map" 		

		reqAddress = 0xffffffff803130cc 
		
		findCloseAddress (mapFile, reqAddress)

		
		
		
		
