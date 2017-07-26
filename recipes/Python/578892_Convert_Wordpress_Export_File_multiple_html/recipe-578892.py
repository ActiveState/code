import datetime
import string, os, sys, getopt
from xml.dom import minidom


__author__ = 'Luis Rei <luis.rei@gmail.com>'
__homepage__ = 'http://luisrei.com'
__version__ = '1.0'
__date__ = '2008/03/23'


def convert(infile, outdir, authorDirs, categoryDirs):
    """Convert Wordpress Export File to multiple html files.
    
    Keyword arguments:
    infile -- the location of the Wordpress Export File
    outdir -- the directory where the files will be created
    authorDirs -- if true, create different directories for each author
    categoryDirs -- if true, create directories for each category
    """
    # First we parse the XML file into a list of posts.
    # Each post is a dictionary
    
    dom = minidom.parse(infile)

    blog = [] # list that will contain all posts

    for node in dom.getElementsByTagName('item'):
    	post = dict()

        try:
            post["title"] = node.getElementsByTagName('title')[0].firstChild.data
        except AttributeError:
            post['title'] = '<no title>'

    	post["date"] = node.getElementsByTagName('pubDate')[0].firstChild.data
    	post["author"] = node.getElementsByTagName(
    	                'dc:creator')[0].firstChild.data
    	post["id"] = node.getElementsByTagName('wp:post_id')[0].firstChild.data
    	
    	if node.getElementsByTagName('content:encoded')[0].firstChild != None:
    	    post["text"] = node.getElementsByTagName(
    	                    'content:encoded')[0].firstChild.data
    	else:
    	    post["text"] = ""
    	
    	# wp:attachment_url could be use to download attachments

    	# Get the categories
    	tempCategories = []
    	for subnode in node.getElementsByTagName('category'):
    		 tempCategories.append(subnode.getAttribute('nicename'))
    	categories = [x for x in tempCategories if x != '']
    	post["categories"] = categories 

    	# Add post to the list of all posts
    	blog.append(post)
    	
    
    # Then we create the directories and HTML files from the list of posts.
    last_date = None
    
    for post in blog:
        date = post['date']
        if last_date and '-0001' in date:
            date = date.replace('-0001', str(last_date.year))
        
        date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S +0000')
        last_date = date

        # The "category" directories
        path = ""
        if authorDirs == True:
            path += post["author"].encode('utf-8') + "/"
        
        # This creates a path for the file in the format
        # category1/category2/category3/file. Note that the category list was
        # sorted.
        
        if categoryDirs == True:
            if (post["categories"] != None):
                path += string.join(post["categories"],"/")

        if os.path.exists(path) == False and path != "":
            os.makedirs(path)
        
        # And finally the file itself
        path = outdir + path
        title = post["title"].encode('utf-8')
        fn_date = date.strftime('%Y%m%d-%H%M%S')
        filename = os.path.join(path, '{}-{}.html'.format(fn_date, title)).replace(' ', '_').strip().lower()
        
        # Add a meta tag to specify charset (UTF-8) in the HTML file
        meta = """<META http-equiv="Content-Type" content="text/html; \
        charset=UTF-8">"""

        # Convert the unicode object to a string that can be written to a file
        # with the proper encoding (UTF-8)
        text = post["text"].encode('utf-8')
        
        # Replace simple newlines with <br/> + newline so that the HTML file
        # represents the original post more accuratelly
        text = text.replace("\n", "<br/>\n")

        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            print 'creating {}'.format(dirname)
            os.makedirs(dirname)

        with open(filename, 'wb') as f:
            f.write(meta+"\n")
        
            # Add "HTML header"
            start = "<html>\n<head>\n<title>"+ title +"</title>\n</head>\n<body>\n"
            f.write(start)
            
            f.write(text)
            
            # Finalize HTML
            end = "\n</body>\n</html>"
            f.write(end)

def usage(pname):
    """Displays usage information
    
    keyword arguments:
    pname -- program name (e.g. obtained as argv[0])
    
    """
    
    
    print """python %s [-hac] [-o outdir] infile
    Converts a Wordpress Export File to multiple html files.
    
    Options:
        -h,--help\tDisplays this information.
        -a,--authors\tCreate different directories for each author.
        -c,--categories\tCreate directory structure from post categories.
        -o,--outdir\tSpecify a directory for the output.
        
    Example:
    python %s -c -o ~/TEMP ~/wordpress.2008-03-20.xml
        """ % (pname, pname)


def main(argv):
    outdir = ""
    authors = False
    categories = False
	
    try:
		opts, args = getopt.getopt(
		    argv[1:], "ha:o:c", ["help", "authors", "outdir", "categories"])	
    except getopt.GetoptError, err:
		print str(err)
		usage(argv[0])
		sys.exit(2)
	
    for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage(argv[0])
			sys.exit()
		elif opt in ("-a", "--authors"):
			authors = True
		elif opt in ("-c", "--categories"):
		    categories = True
		elif opt in ("-o", "--outdir"):
		    outdir = arg
		
    infile = "".join(args)
	
    if infile == "":
	    print "Error: Missing Argument: missing wordpress export file."
	    usage(argv[0])
	    sys.exit(3)
	
    if outdir == "":
	    # Use the current directory
	    outdir = os.getcwd()
	
    convert(infile, outdir, authors, categories)
	

if __name__ == "__main__":
	main(sys.argv)
