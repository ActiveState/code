from win32com.client import Dispatch

html = Dispatch ( 'htmlfile' ) // disguise for MSHTML as a COM server

html.writeln( "<html><header><title>A title</title><meta name='a name' content='page description'></header><body>This is some of it. <span>And this is the rest.</span></html>" )

print "Title: %s" % ( html.title, )
print "Bag of words from body of the page: %s" % ( html.body.innerText, )
print "URL associated with the page: %s" % ( html.url, )
print "Display of name:content pairs from meta tags: "
metas=html.getElementsByTagName("meta")
for m in xrange ( metas.length ):
    print "\t%s: %s" % ( metas [ m ] . name, metas [ m ] . content, )
