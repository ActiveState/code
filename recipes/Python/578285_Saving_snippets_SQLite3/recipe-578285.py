# Name: pySnipnix.py
# Author: pantuts
# Description: Saving your snippets to sqlite3 database.
# Agreement: You can use, modify, or redistribute this tool under
# the terms of GNU General Public License (GPLv3).
# This tool is for educational purposes only. Any damage you make will not affect the author.
# first run: python pySnipnix.py

#!/usr/bin/python

import argparse
import sqlite3
import re
import sys

# important, create the file
fileN = open('database.db', 'a+')

def main():
	
	# add all arguments needed
	# for argument that need FILE use [ type=argparse.FileType('r') ]
	parser = argparse.ArgumentParser(description=None, usage='python %(prog)s -h --help -f file -s search -a \'title\' \'code here\' -e id -d id -v --version')
	parser.add_argument('-f', metavar='filename', type=argparse.FileType('r'), dest='filename', help='File for database')
	parser.add_argument('-s', metavar='string', dest='search', help='Search for string in database')
	parser.add_argument('-a', metavar='string', dest='add', nargs=2, help='Add snippet. You should use \'\' for long string')
	parser.add_argument('-e', metavar='id', type=int, dest='edit', help='Edit snippet')
	parser.add_argument('-d', metavar='id', type=int, dest='delete', help='Delete from database')
	parser.add_argument('-S', dest='show', action='store_true', help='Show all records')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='Print version')
	
	# parse all arguments to 'args'
	args = parser.parse_args()
	
	# database connection
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()
	
	def createTable():
		cmd = 'CREATE TABLE IF NOT EXISTS snippets (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(50), code VARCHAR NOT NULL)'
		cur.execute(cmd)
		conn.commit()
		
	def insertSnippets():
		# convert the string to lowercase and then execute
		lst = [args.add[0].lower() , args.add[1].lower()]
		cmd = 'INSERT INTO snippets VALUES (NULL, ?, ?)'
		cur.execute(cmd, lst)
		conn.commit()
		
		print('\nNew Snippet...')
		print('Snippet Title: \t%s' % args.add[0])
		print('Code: \t\t%s' % args.add[1])
		
	def editSnippets():
		cur.execute('SELECT * FROM snippets where id=%s' % str(args.edit))
		res = cur.fetchone()
		if res is None:
			print('No record to edit!')
		else:
			resl = [result for result in res]
			print('Current title >> ' + resl[1])
			ed1 = input('Title (Leave black, same title): ')
			print('Current snippet >> ' + resl[2])
			ed2 = input('Code: ')
			if ed1 is '':
				ed1 = resl[1]
			cur.executemany('UPDATE snippets SET title=\'%s\', code=\'%s\' WHERE id=?' % (ed1.lower(), ed2.lower()), str(resl[0]))
			conn.commit()
			print('Done!\n')
	
	def deleteSnippets():
		print('\nDeleting record with ID %s ...' % str(args.delete))
		
		# first find if record exists and return false if not found
		cur.execute('SELECT * FROM snippets where id=%s' % str(args.delete))
		res = cur.fetchone()
		if res is None:
			print('No record to delete!')
		else:
			cmd = 'DELETE FROM snippets where id=%s' % str(args.delete)
			cur.execute(cmd)
			conn.commit()
			print('Deleted!\n')
	
	def showOrSearch(cmd):
		# creating conn.create_function explanation: 1st(string to be used inside SQL), 2nd(count of arguments), 3rd(the function created)
		def matchPattern(pattern, columnName):
			pat = re.compile(pattern)
			return pat.search(columnName) is not None
		conn.create_function('matchPattern', 2, matchPattern)
		
		if cmd == 2:
			cur.execute('SELECT * FROM snippets WHERE matchPattern(\'%s\', title)' % str(args.search.lower()))
		else:
			cmd = 1
			cur.execute('SELECT * FROM snippets')
		res = cur.fetchall()
		# create empty dict, process filter keys and values
		s = {'id':{}, 'title':{}, 'code':{}}
		print('\nRecords result...')
		for result in res:
			s['id'] = result[0]
			s['title'] = result[1]
			s['code'] = result[2]
			print('[%s]\t[ %s ]---------->[ %s ]\n' % (s['id'], s['title'], s['code']))
		
	# invoke creation of table
	createTable()
	
	if len(sys.argv) < 1:
	    parser.print_help()
	
	# do filtering when -f 'filename' is correct
	if args.filename is not None:
		
		if args.show:
			if args.add or args.delete or args.search or args.edit:
				print('\nYou can\'t use other options with -S option')
				exit()
			else:
				args.add = None
				args.delete = None
				args.search = None
				args.edit = None
				showOrSearch(1)
		
		elif args.edit:
			if args.add or args.delete or args.search:
				print('\nYou can\'t use other options with -e option')
				exit()
			else:
				args.search = None
				args.add = None
				args.delete = None
				editSnippets()
		
		else:
			if args.add is None and args.delete is None and args.search is None:
				print('\n!!!!!You need to specify addional arguments to process the database!!!!!\n')
				parser.print_help()
			
			if args.search:
				args.edit = None			
				showOrSearch(2)
			
			if args.add:
				args.edit = None
				args.search = None				
				insertSnippets()
				
			if args.delete:
				args.search = None
				args.edit = None
				deleteSnippets()
				
	
	else:
		parser.print_help()
	
	# close our connection to the database
	conn.commit()
	conn.close()	
    
def by():
	print('\n[Script by: pantuts]')
	print('[email: pantuts@gmail.com]')

if __name__=="__main__":
	main()
	# close our file
	fileN.close()

	
