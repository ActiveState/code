def CalculateApacheIpHits(logfile_pathname):

	# make a dictionary to store Ip's and their hit counts and read the
        # contents of the logfile line by line

	IpHitListing = {}
	Contents = open(logfile_pathname, "r").readlines()
	
	# go through each line of the logfile
	for line in Contents:

                #split the string to isolate the ip
                Ip = line.split(" ")[0]

                # ensure length of the ip is proper: see discussion
		if 6 < len(Ip) < 15:
			# Increase by 1 if ip exists else hit count = 1
                        IpHitListing[Ip] = IpHitListing.get(Ip, 0) + 1

	return IpHitListing

# example usage
HitsDictionary = CalculateApacheIpHits("/usr/local/nusphere/apache/logs/access_log")
print HitsDictionary["127.0.0.1"]
