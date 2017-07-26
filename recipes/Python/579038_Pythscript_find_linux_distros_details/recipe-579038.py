from bs4 import BeautifulSoup
from mechanize import Browser
import urllib2 
import sys,re


if len(sys.argv) == 0:
    print "\nSyntax: python %s 'distribution title'" % (sys.argv[0])
    exit()
else :
     distribution = '+'.join(sys.argv[1].split())

try:
  br = Browser()
  br.open("http://distrowatch.com/table.php?distribution="+distribution)
  br.response().read()
  print br.title()
  url = br.geturl()

  content = urllib2.urlopen(url).read()
except urllib2.URLError :
       print "Unable to connect to internet !! OR  not connected to internet !!"
else :
     soup=BeautifulSoup(content)

try :
   title = soup.find("h1").contents[0].strip()
   print "DISTRIBUTION:",title
   ul = soup.findAll("ul")
   li = soup.ul.findAll("li")
   
   for i in li:
       print("{} {}.".format(i.b.text,"".join([a.text for a in i.findAll("a")])))
except:
    print("Link not found Distribution name ERROR")
   
    


    
  
  
  
