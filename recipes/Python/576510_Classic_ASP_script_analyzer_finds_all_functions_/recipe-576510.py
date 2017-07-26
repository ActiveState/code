""" Classic ASP script analyzer, finds all functions, includes, duplicate functions  """
#TO-DO: testing, it was tested only on one big project

import string, re, sys, os.path, logging, sqlite3
from Tkinter import *
import tkFileDialog, tkMessageBox

def find_functions(file_name, data, db_cursor, functions):
	""" finds all functions in asp script """
	my_re = re.compile(r'[^\'\"][ ]{0,10}function[ ]{1,3}(?P<fun>[a-z0-9_\-]{1,30})', re.IGNORECASE)
	res = my_re.findall(data)
	if res:
		for line in res:			
			print "function", line.lower()
			tmp = file_name + '\t\t' + line.lower()		#(file_name, line)
			functions.append(tmp)			
			db_cursor.execute("""insert into project_functions
					values ((SELECT max(id) FROM project_functions)+1, '%s', '%s', 'function')""" % (file_name, line.lower()))			

	my_re = re.compile(r'[^\'\"][ ]{0,10}sub[ ]{1,3}(?P<fun>[a-z0-9_\-]{1,30})', re.IGNORECASE)
	res = my_re.findall(data)
	if res:
		for line in res:			
			print "sub", line.lower()
			#tmp = (file_name, line)
			tmp = file_name + '\t\t' + line.lower()		#(file_name, line)
			functions.append(tmp)
			db_cursor.execute("""insert into project_functions
					values ((SELECT max(id) FROM project_functions)+1, '%s', '%s', 'sub')""" % (file_name, line.lower()))				


def find_includes(file_path, recursive_level, dir_before, db_cursor, includes, functions):
	""" find al includes,  recursive call """
	for dr in dir_before:
		os.chdir(dr)
		try: f = open(file_path, "r")
		except: pass

	try:
		data = f.read()
		f.close()
	except:
		print dir_before
		print file_path
		return ([], [])

	
	find_functions(os.path.split(file_path)[1], data, db_cursor, functions)

	if len(os.path.split(file_path)[0]) > 1:	 
		#print "dir_before 1", os.path.split(file_path)[0]
		try:
			os.chdir(os.path.split(file_path)[0]) #change work dir to script home dir
			if not os.getcwd() in dir_before:
				dir_before.append(os.getcwd())
		except:
			pass		

   # print "Current directory", os.getcwd(), dir_before, recursive_level

	include_file = []

	my_re = re.compile(r'[^\'][\s]{0,5}<!--[\s]{0,5}#[\s]{0,5}INCLUDE[\s]{0,5}FILE[\s]{0,5}=(?P<file>[ \d\w\.\\\\/_\-"]{1,50})-->', re.IGNORECASE)
	res = my_re.findall(data)
	if not res:
		#print "No include in %s file Regexp not matched" % (file_path)
		#logger.info("No include in %s file Regexp not matched" % (file_path))
		return 1
	else:
		for line in res:			
			include_file.append(line.replace("\"","").strip())
			#print include_file

	#include_file.sort()
	#include_file.reverse()

	includes.append("Includes in: " + os.path.split(file_path)[0] + "\\" + os.path.split(file_path)[1])
	print "Includes in:", os.path.split(file_path)[0] + "\\" + os.path.split(file_path)[1]
	for inc_file in include_file:
		includes.append(inc_file)
		print inc_file 

	for inc_file in include_file:
		find_includes(inc_file, recursive_level + 1, dir_before, db_cursor, includes, functions)
					
	return (includes, functions)


def main(file_path, db_path):
	""" read arguments and analyze """

	if not os.path.exists(file_path):
		print "File %s not found" % (file_path	)
		return 1

	c = ''	 
	conn = sqlite3.connect(db_path)    
	c = conn.cursor()

	try:
		c.execute('''DROP TABLE project_functions''')
	except:
		pass

	c.execute('''create table project_functions
		(id INTEGER PRIMARY KEY, script_name text, fun_name text, fun_type text)''')	
	
	includes = []
	functions = []


	file_path_dir = os.path.split(file_path)[0]
	os.chdir(file_path_dir) #change work dir to script home dir
	print file_path_dir

	includes, functions = \
		find_includes(file_path, 0, [file_path_dir], c, includes, functions)

	conn.commit()

	doubles_fun = []
	c.execute("""SELECT fun_name FROM project_functions
			group by fun_name
			having count(fun_name) > 1""")
	for fun_name in c:
		doubles_fun.append(fun_name)
		
	duplicites = []		
	for i,fun_name in enumerate(doubles_fun):
		dup = fun_name[0] + '\t'
		print i,fun_name[0]
		#t = (fun_name,)	
		c.execute("select script_name, fun_name, fun_type from project_functions where fun_name='%s'" % (fun_name))
		for row in c:
			print '\t', row[0]
			dup = dup + row[0] + ','
		
		duplicites.append(dup)


	c.close()
	
	return (includes, functions, duplicites)


class App:
	""" GUI """
	def __init__(self, master):
		self.master = master

		Label(master, text="File to analyze:").grid(row=0)
		Label(master, text="File for database:").grid(row=1)
		#Label(master, text="File for export (optional):").grid(row=2)

		self.e1 = Entry(master, width = 35)
		self.e2 = Entry(master, width = 35)
		self.e2.insert(INSERT, "C:\\analyze_webscript.db3")
		#self.e3 = Entry(master, width = 35)
		#self.e3.insert(INSERT, "X:\\temp.web\\analyze_webscript.txt")

		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		#self.e3.grid(row=2, column=1)

		self.b1 = Button(master, text="Browse", command=self.br1, width = 10)
		self.b2 = Button(master, text="Browse", command=self.br2, width = 10)
		#self.b3 = Button(master, text="Browse", command=self.br3, width = 10)

		self.b1.grid(row=0, column=2)
		self.b2.grid(row=1, column=2)
		#self.b3.grid(row=2, column=2)

		self.v1 = IntVar()
		self.c1 = Checkbutton(master, text="find all includes", variable=self.v1)
		self.c1.var = self.v1
		self.c1.grid(columnspan=2, sticky=W)

		self.v2 = IntVar()
		self.c2 = Checkbutton(master, text="find all functions in all includes", variable=self.v2)
		self.c2.var = self.v2
		self.c2.grid(columnspan=2, sticky=W)

		self.v3 = IntVar()
		self.c3 = Checkbutton(master, text="find duplicite functions", variable=self.v3)
		self.c3.var = self.v3
		self.c3.grid(columnspan=2, sticky=W)


		#self.listbox = Listbox(master, selectmode=SINGLE)
		#for item in ["one", "two", "three", "four"]:
		#	 self.listbox.insert(END, item)		 
		#self.listbox.grid(row=3,column=1)

		self.b4 = Button(master, text="Start Analyze", command = self.start_analyze, width = 15)
		self.b4.grid(row=5, column=2)

		self.text = Text(master,width=70, height=30)
		self.vscroll = Scrollbar(master,orient=VERTICAL)
		self.vscroll.grid(row=6, column=4, sticky=N+S)
		self.vscroll.config(command=self.text.yview)
		#self.vscroll.config(command=self.text.yview)
		#self.text.config(yscrollcommand=self.vscroll.set)
		self.text.grid(row=6, columnspan=3, sticky=W)

	def start_analyze(self):
		print "started"
		print self.v1.get()
		print self.v2.get()
		print self.v3.get()

		if (not self.v1.get()) and (not self.v2.get()) and (not self.v3.get()):
			tkMessageBox.showwarning("Action", "Please choose action")
			return 1	

		analyze_file = self.e1.get()
		db_file = self.e2.get()

		if len(analyze_file) == 0 or len(db_file) == 0:
			tkMessageBox.showwarning("Action", "Please set file location")
			return 1	

		print analyze_file
		print db_file
		#print self.e3.get()
		includes, functions, duplicites = \
				main(analyze_file, db_file)
		#self.frame = Frame(width=768, height=576, bg="", colormap="new")
		#self.ef1 = Text(self.frame, width = 50, heigth = 50)
		#self.ef1.insert(INSERT, includes)
		#self.frame.pack()
	
		self.text.delete(1.0, END)		

		if self.v1.get():
			self.text.insert(END, 'INCLUDES:\n')
			self.text.insert(END, '\n'.join(includes))

		if self.v2.get():
			if self.v1.get():
				self.text.insert(END, '\n\n')
			self.text.insert(END, 'FUNCTIONS:\n')
			self.text.insert(END, '\n'.join(functions))

		if self.v3.get():
			if self.v1.get() or self.v2.get():
				self.text.insert(END, '\n\n')
			self.text.insert(END, 'DUPLICATES:\n')
			self.text.insert(END, '\n'.join(duplicites))

		#self.text.pack(side=LEFT,expand=1,fill=BOTH)
		#self.vscroll = Scrollbar(frame2,orient=VERTICAL)
		#self.vscroll.pack(side=LEFT,fill=Y,anchor=E)
		#self.vscroll.config(command=self.text.yview)
		#self.text.config(yscrollcommand=self.vscroll.set)
		#frame2.pack(expand=1,fill=BOTH)

		

	def br1(self):
		self.e1.delete(0, len(self.e1.get()))
		p = tkFileDialog.askopenfilename(title = "File for analyze", initialdir = "C:\\inetpub\\wwwroot")
		self.e1.insert(INSERT, p)

	def br2(self):
		self.e2.delete(0, len(self.e2.get()))
		p = tkFileDialog.askopenfilename(title = "File for database")
		self.e2.insert(INSERT, p)

	#def br3(self):
#		p = tkFileDialog.askopenfilename(title = "File for export")
#		self.e3.insert(INSERT, p)

root = Tk()
root.title("ASP script analyzer")
App(root)
root.mainloop()
