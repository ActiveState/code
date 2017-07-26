import glob, getopt
import fileinput,re,shelve,linecache,sys
from TextSplitter import TextSplitter



#aword = re.compile(r'\b[\w-]+\b')
aword =re.compile (r'<[^<>]*>|\b[\w-]+\b') #using xml as well.
index={}

# Generate an index in file indexFileName

def genIndex(indexFileName, extension):
   fname='*.'+extension
   for line in fileinput.input(glob.glob(fname)):
      location = fileinput.filename(), fileinput.filelineno()
      for word in aword.findall(line.lower()):
         if word[0] != '<':
            index.setdefault(word,[]).append(location)
   shelf = shelve.open(indexFileName,'n')
   for word in index:
      shelf[word] = index[word]
   shelf.close()

# cmd line usage.

def usage():
   print "Usage: \n\txmlIndexer -c filename "
   print "\tto create an index of all xml files in current directory in 'filename'"
   print "\t xmlIndexer -f filename -s searchPattern"
   print "\tto search the current index 'filename' for 'searchPattern'"
   
# main.
if __name__ == '__main__':
   if len(sys.argv) <= 1:
      usage()
      sys.exit(2)
   try:
      opts,args = getopt.getopt(sys.argv[1:],"c:s:f:h",["help","create=","search=","filename="])
   except getopt.GetoptError:
      usage()
      print "Option Exception"
      sys.exit(2)

   indexFile=""
   searchPattern=""
   for o, a in opts:
      #print "o: " + o
      #print "a: " + a
      if o in ("-h","--h","-help"):
         usage()
         sys.exit()
      if o in ("-c","--c","--create"):
         indexFile= a # generate index, set indexfile to arg
         searchPattern="" # ensure no pattern in use
         break
      if o in ("-f","--f","--filename"):
         indexFile = a
      if o in ("-s","--s","--search"):
         searchPattern=a  # set search pattern

   

   #check for pair if searchpattern set then need an index file.
   if searchPattern != "":
      if indexFile == "":
         print "\t Option error. Need an index file to search for a pattern"
         usage()
         sys.exit(2)
      else:                                       # search for pattern in index
         print "Searching for " + searchPattern + " in index " + indexFile
         
         word = searchPattern
         shelf = shelve.open(indexFile, 'r')
         try:
            locations = shelf[word] # was word.lower() to be case ignorant
         except KeyError:
            print word+': not found'
         else:
            print "Word ", word +' is', 
            for file, line in locations:
                print ' in file ' + file +' line:' , line
   else:                         # generate the index
      genIndex(indexFile, 'xml')   
      print "Index generated in file "+indexFile
      
