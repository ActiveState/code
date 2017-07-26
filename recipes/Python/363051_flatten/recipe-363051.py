def flatten(sequence):

        def hms(fpd):
                if fpd < 60:
                    return fpd
                elif fpd < 60**2:
                    return "%s:%s" % (int(fpd/60), fpd-int(fpd/60)*60)
                else:
		    h = int(fpd/60**2)
		    fpd -= h*60**2
		    m = int(fpd/60)
		    fpd -= m*60
		    s = fpd
                    return "%s:%s:%s" % (h, m, s)
                
	def rflat(seq2):
		seq = []
		for entry in seq2:
			if seqin([entry]):
        			seq.extend([i for i in entry])
			else:
				seq.append(entry)
		return seq

	def seqin(sequence):
		for i in sequence:
			if ('__contains__' in dir(i) and    ## all sequences have '__contains__' in their dir()
                           type(i) != str and type(i) != dict): ## parentheses present to aid commenting mid-condition
				return True
		return False

        import time
        btime = time.time()
        d1time = btime
	seq = [sequence][:]    ## in case parameter isn't already a sequence
	print "Thinking",
	while seqin(seq):
                d2time = time.time()
                if d2time-d1time >= 5:
                    print ".",
                    d1time = d2time
		seq = rflat(seq)
	atime = time.time()
	print
	print "Sequence flattened in " + str(hms(atime-btime))
	return seq
