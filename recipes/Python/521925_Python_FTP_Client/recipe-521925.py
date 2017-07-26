from ftplib import FTP
import sys, os, os.path, operator

def upload(handle,filename):
	f = open(filename,"rb")
	(base,ext) = os.path.splitext(filename)
	picext = ".bmp .jpg .jpeg .dib .tif .tiff .gif .png"
	if(operator.contains(picext,ext)):
		try:
			handle.storbinary("STOR " + filename,f,1)
		except Exception:
			print "Successful upload."
		else:
			print "Successful upload."
		f.close()
		return

	try:
		handle.storbinary("STOR " + filename,f)
	except Exception:
		print "Successful upload."
	else:
		print "Successful upload."
	f.close()
	return


def download(handle,filename):
	f2 = open(filename,"wb")
	try:
		handle.retrbinary("RETR " + filename,f2.write)
	except Exception:
		print "Error in downloading the remote file."
		return
	else:
		print "Successful download!"
	f2.close()
	return

print "CLIFTP ~ NSP Corp.\n\n"
host_name = raw_input("Enter website name to connect to, exclude ftp notation:  ")
if "http://" in host_name:
	host_name = host_name.replace("http://","")
host_name = host_name.replace("\n","")
user = raw_input("Enter username: ")
pwd = raw_input("Enter password: ")
try: ftph = FTP(host_name)
except:
	print "Host could not be resolved."
	raw_input()
	sys.exit()
else: pass
try:
	ftph.login(user,pwd)
except Exception:
	if user == "anonymous" or user == "Anonymous" and pwd == "anonymous" or pwd == "Anonymous":
		print "The server does not accept anonymous requests."
		raw_input()
		sys.exit()
	else:
		print "Invalid login combination."
		raw_input()
		sys.exit()
else:
	print "Successfully connected!\n"
print ftph.getwelcome()
flag = 1
count = 0
path = ftph.pwd()
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
print "Press help at any time to see proper usage.\n"
while flag:
	command = raw_input("FTP ]> ")
	if "get " in command:
		rf = command.replace("get ","")
		rf = rf.replace("\n","")
		download(ftph,rf)
		continue
	elif "put " in command:
		lf = command.replace("put ","")
		lf = lf.replace("\n","")
		upload(ftph,lf)
		ftph.close()
		ftph = FTP(host_name)
		ftph.login(user,pwd)
		continue
	elif "makedir " in command:
		mkdirname = command.replace("makedir ","")
		mkdirname = mkdirname.replace("\n","")
		try: ftph.mkd(mkdirname)
		except:
			print "Incorrect usage."
			continue
		else:
			print "Directory created."
			continue
	elif "remdir " in command:
		rmdirname = command.replace("remdir ","")
		rmdirname = rmdirname.replace("\n","")
		current = ftph.pwd()
		ftph.cwd(rmdirname)
		allfiles = ftph.nlst()
		for file in allfiles:
			try:
				ftph.delete(file)  
			except Exception:
				pass
			else:
				pass
		ftph.cwd(current)
		try:
			ftph.rmd(rmdirname)
		except Exception:
			print "All files within the directory have been deleted, but there is still another directory inside.  As deleting this directory automatically goes against true FTP protocol, you must manually delete it, before you can delete the entire directory."
		else:
			print "Directory deleted."
		continue
	elif command == "dir":
		print ftph.dir()
		continue
	elif command == "currdir":
		print ftph.pwd()
		continue
	elif "chdir " in command:
		dirpath = command.replace("chdir ","")
		dirpath = dirpath.replace("\n","")
		ftph.cwd(dirpath)
		print "Directory changed to " + dirpath
		continue
	elif command == "up":
		dir = ftph.pwd()
		temp = dir
		index = len(dir) - 1
		for i in range(index,0,-1):
			if temp[i] == "/" and i != len(dir):
				ftph.cwd(temp)
				print "One directory back."
				continue
			if(operator.contains(charset,dir[i])):
				temp = temp[:-1]
				if temp=="/":
					ftph.cwd(temp)
					print "One directory back."
	elif command == "rename":
		fromname = raw_input("Current file name: ")
		toname = raw_input("To be changed to: ")
		ftph.rename(fromname,toname)
		print "Successfully renamed."
		continue
	elif "delete " in command:
		delfile = command.replace("delete ","")
		delfile = delfile.replace("\n","")
		ftph.delete(delfile)
		print "File successfully deleted."
		continue
	elif command == "term":
		ftph.close()
		print "Session ended."
		raw_input()
		sys.exit()
	elif "size " in command:
		szfile = command.replace("size ","")
		szfile = szfile.replace("\n","")
		print "The file is " + str(ftph.size(szfile)) + " bytes."
		continue		
	elif command == "debug -b":
		ftph.set_debuglevel(1)
		print "Debug mode set to base."
		continue
	elif command == "debug -v":
		ftph.set_debuglevel(2)
		print "Debug mode set to verbose."
		continue
	elif command == "debug -o":
		ftph.set_debuglevel(0)
		print "Debug mode turned off."
		continue
	elif command == "help":
		print "debug -o - turns off debug output\n"
		print "debug -v - turns the debug output to verbose mode\n"
		print "debug -b - turns the debug output to base\n"
		print "size [filename] - returns the size in bytes of the specified file"
		print "term - terminate the ftp session\n"
		print "delete [filename] - delete a file\n"
		print "rename - rename a file\n"
		print "up - navigate 1 directory up\n"
		print "chdir [path] - change which directory you're in\n"
		print "currdir - prints the path of the directory you are currently in\n"
		print "dir - lists the contents of the directory\n"
		print "remdir [directory path] - removes/deletes an entire directory\n"
		print "makedir [directory path] - creates a new directory\n"
		print "put [filename] - stores a local file onto the server (does not work with microsoft office document types)\n"
		print "get [filename] - download a remote file onto your computer\n\n"
		continue
	else:
		print "Sorry, invalid command.  Check 'help' for proper usage."
		continue

#EoF	
	
