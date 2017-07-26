import re

class reop:
	"""supporting class for representing re operators"""
	def __init__(self,x):
		self.value = x
def buildmap(inx):
	"""builds the map from the symbol set above, every symbol as a unicode char"""
	import itertools
	from collections import defaultdict
	d = defaultdict(itertools.count().next)
	for x in inx: 
		d[x]
	return d
def buildimap(inmap):
	"""builds the inverse map"""
	return dict([(y,x) for x,y in inmap.iteritems()])
def buildseq(inmap,inseq,xdef=None):
	"""given a sequence and the mapping returns the encoding"""
	if xdef is not None:
		xdef = inmap[xdef]
		if len(inmap) < 254:
			r = "".join([chr(inmap.get(x,xdef)) for x in inseq])
		else:
			r = u"".join([unichr(inmap.get(x,xdef)) for x in inseq])
	else:
		if len(inmap)+len(inseq) < 254:
			r = "".join([chr(inmap[x]) for x in inseq])
		else:
			r = u"".join([unichr(inmap[x]) for x in inseq])
	return r

def compile(inmap,gregexp):
	"""given a mapping dictionary and a generic regular expression returns it compiled"""
	return re.compile(u"".join([isinstance(x,reop) and x.value or u"\\"+unichr(inmap[x]) for x in gregexp]))

def unmap(inmapr,encoded):
	return [inmapr[ord(x)] for x in encoded]
	
if __name__ == "__main__":
	x = ["hello","world","view","around","*"]
	map1 = buildmap(x)
	rex = compile(map1,("look",reop(".*?"),"world"))
	es = buildseq(map1,"when I look the world what can I look at you in the world".split(" "))
	print "encoded is ",es,len(es),type(es)
	print unmap(map1,es)
	print "go!"
	map1i = buildimap(map1)
	for m in rex.findall(es):
		print unmap(map1i,m)
		
