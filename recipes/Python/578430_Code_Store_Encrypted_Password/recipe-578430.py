import sys
import hashlib
import getpass

def main(argv):

	if len(argv) != 1:
		sys.exit('Usage: store_pass.py <file_name>')

	print '\nPassword Storage Program v.01\n'
	
	if raw_input('The file ' + sys.argv[1] + ' will be erased or overwrite if existing.\nDo you wish to continue (Y/n): ') not in ('Y','y') :
		sys.exit('\nChanges were not recorded\n')
	
	password = hashlib.sha224(getpass.getpass('Please Enter a Password: ')).hexdigest()

	try:
		file_conn = open(sys.argv[1],'w')
		file_conn.write(password + '\n')
		file_conn.close()
	except:
		sys.exit('There was a problem writing to the file!')

	print '\nPassword safely stored in ' + sys.argv[1] + '\n'		
			
if __name__ == "__main__":
	main(sys.argv[1:])
