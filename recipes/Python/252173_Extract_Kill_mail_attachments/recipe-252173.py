# This file should clear the file from all attachments which are not text.
# the use of the script is killAttach.py <nameofThemessage> the name of the
# message is simply the name of the (MIME) file in which the message is saved.
# Of course this means that the file contains one and only one message.
#
# The attachments are extracted in a temporary directory
# the directory simply is given as a constant.
# see the constant ATTACHMENTS_DIR
#
# This script is well suited to be used with the sylpheed mail client,
# symply define an action "killAttachments" where the action to be
# called is
# <path_1>python <path_2>\killAttach.py %f
# 
# where path_1 is the path to python executable (or none if it is in the path)
# REMEMBER: It NEEDS python 2.2
#
# path_2 is simply the path to the killAttach.py script
# 	or none if it is already in the path.
#
#
#
# the script could also be used alone, of course, simply call it with the
# argument as the file
#
#
# This software is licensed under the GNU Open Source License
# Copyright(c) 2003 Pasqualino Ferrentino
# ferrentino_p@yahoo.it

import sys, email, os, mimetypes, errno

ATTACHMENTS_DIR = "d:\\temp\\attach\\"

def main():

	#first of all I take the arguments
	if len(sys.argv)!=2:
		print "I need the name of the message to purge!"
		sys.exit(1)

	#open the file
	try:
		myMessageInFile = open(sys.argv[1])
	except IOError:
		print "no file!"
		sys.exit(1)

	#I parse the message to be filtered
	try:
		myMessage = email.message_from_file(myMessageInFile)
		myMessageInFile.close()
		#try:
		#	os.rename(sys.argv[1], sys.argv[1] + "~")
		#except OSError:
		#	os.remove(sys.argv[1] + "~")
		#	os.rename(sys.argv[1], sys.argv[1] + "~")
			
	except email.Errors.HeaderParseError:
		print "Corrupt message!"
		sys.exit(1)

	if ( not myMessage.is_multipart()):
		print "nothing to do!"
		sys.exit(0)


	purgeThisMessageFromTheAttachments(myMessage)
	
	#Now the message should be purged
	#print myMessage.as_string()

	print "message %s successfully purged!" % (sys.argv[1])

	#I save it to the file
	outfile = open (sys.argv[1], "w")
	outfile.write (myMessage.as_string())
	outfile.close()

def purgeThisMessageFromTheAttachments(aMessage):
	""" this function is recursive, if the message contains
	multipart message the function is recursively called to
	purge all the attachments"""

	partsToDelete = [] #empty list
	index = 0

	list = aMessage.get_payload()

	#end of recursion, the payload is a string
	if type(list) == type(""):
		return

	for part in list:
		maintype =  part.get_content_maintype()
		print maintype

		#I mark this part for delete, because it is not text
		if ( maintype != "text" and maintype != "multipart" and
			maintype != "message"):
			# Also the message type is a kind of multipart
			partsToDelete.append(index)

		if (maintype == "multipart" or maintype == "message"):
			#recursive call
			purgeThisMessageFromTheAttachments(part)
			
		index = index + 1

	#I can now delete the parts
	listParts = aMessage.get_payload()
	offset = 0

	#DEBUG prints
	#print "I should delete these parts"
	#print partsToDelete

	#print "The message has these parts"
	#print listParts

	for indexToDelete in partsToDelete:
		#print indexToDelete
		indexToDelete = indexToDelete - offset
		#let's save the part that we wish to delete.
		filename = listParts[indexToDelete].get_filename()
		if not filename:
			ext = mimetypes.guess_extension(part.get_type())
			if not ext:
				#generic extension
				ext = ".bin"
			filename = "part-%03d%s" % (indexToDelete, ext)

		fp = open (ATTACHMENTS_DIR + filename, "wb")
		fp.write(listParts[indexToDelete].get_payload(decode=1))
		fp.close()
		del listParts[indexToDelete]
		offset = offset + 1
		#print listParts

	

#let's call the main
if __name__ == "__main__":
	main()
