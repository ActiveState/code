#don't include initial "$" or trailing "*XX"
item = "GPRMC,004422.767,A,3601.9719,N,07950.6023,W,0.00,,180804,,,A"
#should return a "*6F"    
s = 0
for i in range(len(item) ):
    s = s ^ ord(item[i])
checksum = "*"
#convert to hex
s = "%02X" % s
checksum += s
        
print "Checksum: %s" % checksum
