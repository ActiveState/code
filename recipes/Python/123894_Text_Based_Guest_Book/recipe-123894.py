#!/usr/bin/python

import cgi

# define files to use
header_file_name 	= 'files/header'
footer_file_name 	= 'files/footer'
book_file_name 		= 'files/book'
form_file_name		= 'files/form'


##########################
## Function Definitions ##
##########################

# Print the header from an external file
def printfile( file_name ):
	file = open( file_name , "r")
	for line in file.readlines():
		print line
	file.close();

# define a function for the message entry
# entry == the form dictionary
# book  == the guestbook file
def bookEntry( entry ):
	book = open( book_file_name, 'a')
	book.write( '<TR><TD COLSPAN="2"><B>%s</B>' % entry['name'].value )
	book.write( '''
	<HR WIDTH="100%"><BR>
	</TD></TR>
	<TR><TD VALIGN="TOP" ALIGN="RIGHT">
	''' )
	if entry.has_key('email'):
		email = entry['email'].value 
		book.write( '<A HREF="mailto:%s">\n  %s\n</A>' % (email,email) )
		book.write( '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n<BR>\n' )
	if entry.has_key('website'):
		website = entry['website'].value 
		book.write( '<A HREF="http://%s">\n  %s\n</A>' % (website,website) )
		book.write( '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n' )
	book.write( '</TD><TD VALIGN="TOP">\n%s\n</TD></TR>\n' %entry['message'].value )
	book.write( '<TR><TD><BR></TD></TR>\n\n\n' )
	book.close()   # This line was changed from the April 30 version


###################
## Program Logic ##
###################

# create the form dictionary
form = cgi.FieldStorage()

# check if a from was submitted
if len( form ) > 1:
	# check to see if both a name and message are provided
	if not (form.has_key("name") and form.has_key("message")):
		print "To add an entry, both name and message is required";
	else:
		bookEntry( form )
		
#################
## Page Output ##
#################

# print a header
print "content-Type: text/html"
print

# Print the header from an external file
printfile( header_file_name )

# read the current guestbook
printfile( book_file_name )

# write a form
printfile( form_file_name )

# print the footer
printfile( footer_file_name )
