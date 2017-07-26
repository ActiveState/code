#------------------------------------------------------------------------------
#           Name: attdownload.py
#         Author: Suresh Kumar MP
#  Last Modified: 09/29/06
#    Description: This python script monitors the IMAP mail server for the given
#				  account and moves the mails with attachments to "Downloadedmails"
#				  folder in server after downloading the attachments to the individual
#				  directories on localmachine with a timestamp.
#------------------------------------------------------------------------------
import getopt, getpass, os, sys, time
import imaplib
import email, email.Errors, email.Header, email.Message, email.Utils
from time import strftime
from time import sleep


Usage = """Usage: %s  --user <user> --password <password> --frequency <polling frequency> <imap-server>

	--user		  Provide <user> for authentication on <imap-server>
			
	--password    Password for the given user

	--frequency	  Provide the mail server polling frequency in seconds	

	 Example:  attdownload.py --user username --password password --frequency 300 10.133.23.124

"""

AttachDir = '.'			# Attachment Directory Path
DeleteMessages = 0
SaveAttachments = 1		# Save all attachments found
User = None				# IMAP4 user
Password = None			# User password
Frequency = None		# Mail server polling frequency
exists = 0				
name = 0

def usage(reason=''):
	sys.stdout.flush()
	if reason: sys.stderr.write('\t%s\n\n' % reason)
	head, tail = os.path.split(sys.argv[0])
	sys.stderr.write(Usage % tail)
	sys.exit(1)

def args():
	try:
		optlist, args = getopt.getopt(sys.argv[1:], '?',['user=', 'password=', 'frequency='])
	except getopt.error, val:
		usage(val)

	global SaveAttachments
	global User
	global Password
	global Frequency
	
	for opt,val in optlist:
		if opt == '--user':
			User = val
		elif opt == '--password':
			Password = val
		elif opt == '--frequency':
			Frequency = float(val)
		else:
			usage()

	if len(args) != 1:
		usage()

	return args[0]

def write_file(filename, addr, data):
	os.chdir(addr)
	fd = open(filename, "wb")	
	fd.write(data)
	fd.close()
	

def gen_filename(name, mtyp, addr, date, n):

	timepart = strftime("%d %b %y %H_%M_%S")	
	file = email.Header.decode_header(name)[0][0]
	file = os.path.basename(file)
	print "Saved attachment  " + file + "  from  " + addr
	print "\n"
	path = os.path.join(AttachDir, file)
	pre, ext = os.path.splitext(file)
	pre = pre + "_" + timepart
	path = '%s%s' % (os.path.join(AttachDir, pre),  ext)
	return path

def error(reason):
	sys.stderr.write('%s\n' % reason)
	sys.exit(1)
	
def walk_parts(msg, addr, date, count, msgnum):
	for part in msg.walk():
		if part.is_multipart():
			continue
		dtypes = part.get_params(None, 'Content-Disposition')
		if not dtypes:
			if part.get_content_type() == 'text/plain':
				continue
			ctypes = part.get_params()
			if not ctypes:
				continue
			for key,val in ctypes:
				if key.lower() == 'name':
					filename = gen_filename(val, part.get_content_type(), addr, date, count)
					break
			else:
				continue
		else:
			attachment,filename = None,None
			for key,val in dtypes:
				key = key.lower()
				if key == 'filename':
					filename = val
				if key == 'attachment':
					attachment = 1
			if not attachment:
				continue
			filename = gen_filename(filename, part.get_content_type(), addr, date, count)
			
		try:
			data = part.get_payload(decode=1)
		except:
			typ, val = sys.exc_info()[:2]
			warn("Message %s attachment decode error: %s for %s ``%s''"
				% (msgnum, str(val), part.get_content_type(), filename))
			continue

		if not data:
			warn("Could not decode attachment %s for %s"
				% (part.get_content_type(), filename))
			continue

		if type(data) is type(msg):
			count = walk_parts(data, addr, date, count, msgnum)
			continue
		
		if SaveAttachments:
			exists = "0"
			try:
				curdir= os.getcwd()
				list = os.listdir('.\\')
				for name in list:
					if name == addr:
						exists = "1"
						break
				if exists == "1":
					write_file(filename, addr, data)
					os.chdir(curdir)					
				else:
					os.mkdir(addr)
					write_file(filename, addr, data)
					os.chdir(curdir)
					exists == "0"
					os.chdir(curdir)
			except IOError, val:
				error('Could not create "%s": %s' % (filename, str(val)))
	
		count += 1

	return count


def process_message(text, msgnum):
	
	try:
		msg = email.message_from_string(text)
	except email.Errors.MessageError, val:
		warn("Message %s parse error: %s" % (msgnum, str(val)))
		return text

	date = msg['Date'] or 'Thu, 18 Sep 2006 12:02:27 +1000'
	date = time.strftime('%Y_%m_%d.%T', email.Utils.parsedate(date))
	addr = email.Utils.parseaddr(msg['From'])[1]
	
	
	
	attachments_found = walk_parts(msg, addr, date, 0, msgnum)
	if attachments_found:
		return ''
	else:	
		return None


def read_messages(fd):

	data = []; app = data.append

	for line in fd:
		if line[:5] == 'From ' and data:
			yield ''.join(data)
			data[:] = []
		app(line)

	if data:
		yield ''.join(data)


def process_server(host):

	global DeleteAttachments

	try:
		mbox = imaplib.IMAP4(host)
	except:
		typ,val = sys.exc_info()[:2]
		error('Could not connect to IMAP server "%s": %s'
				% (host, str(val)))

	if User or mbox.state != 'AUTH':
		user = User or getpass.getuser()
	if Password == "":
		pasw = getpass.getpass("Please enter password for %s on %s: "
						% (user, host))
	else:
		pasw = Password
		
	try:
		typ,dat = mbox.login(user, pasw)
	except:
		typ,dat = sys.exc_info()[:2]

	if typ != 'OK':
		error('Could not open INBOX for "%s" on "%s": %s'
			% (user, host, str(dat)))

	mbox.select('Inbox')
	#mbox.select(readonly=(DeleteMessages))
	typ, dat = mbox.search(None, 'ALL')
	mbox.create("DownloadedMails")
	
	deleteme = []
	for num in dat[0].split():
		typ, dat = mbox.fetch(num, '(RFC822)')
		if typ != 'OK':
			error(dat[-1])
		message = dat[0][1]
		if process_message(message, num) == '':
			deleteme.append(num)
	if deleteme == []:
		print "\n"
		print "No mails with attachment found in INBOX"
		
		
	deleteme.sort()
	for number in deleteme:
		mbox.copy(number, 'DownloadedMails')
		mbox.store(number, "+FLAGS.SILENT", '(\\Deleted)')
		

	mbox.expunge()
	mbox.close()
	mbox.logout()

def main():

	file_or_server = args()
	print "\n"
	print "Monitoring the Mail server  " + file_or_server + "  for account  " + User
	while 1:
		process_server(file_or_server)
		printfre = str(Frequency)
		print "Sleeping for  " + printfre + "  seconds..."
		sleep(Frequency)
		
		


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
