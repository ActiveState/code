from xml.dom import minidom
from os import walk
import ConfigParser
import csv
from string import split
from string import strip
from time import gmtime, localtime, asctime
from os.path import join, dirname, exists, abspath

#log errors stuff
from traceback import format_exception
from sys import exc_info


#this is the log file - made global so all the subroutines can see it
global mylog

#small app to suck InfoPath data files into Excel csv file


def get_fields():
    global mylog
    mylog.writelines(".. parsing config \n")
    fields =[]
    cp = ConfigParser.ConfigParser()
    cp.read("config.ini")
    fields = split(cp.get("InfoPath","fields"),",")
    path = cp.get("InfoPath","path")
 

    return fields, path


def read_file(fields, path, writer):
    global mylog
    #read and write out the files
    for root, dirs, files in walk(path):
        for filename in files:
            if ".xml" in filename:
                abspath = join(root, filename)
                try:
		    mylog.write("\n" + abspath + "\n")
                    f = open(abspath,'r')
                    dom = minidom.parseString(f.read())
                    row = []            

                    for field in fields:
			try:
                            data = dom.getElementsByTagName(strip(field))[0].childNodes[0].data

			    data.encode('utf-8') #put your code set here
			except:
                            mylog.write("...error on " + field + "\n")
                            mylog.write(''.join(format_exception(*exc_info()))) 

			    data = " "

                        row.append(data)


                    writer.writerow(row)
                    f.close()
                except:
                    txt =  ''.join(format_exception(*exc_info()))
                    mylog.write(txt + "\n") 

                
def create_log ():
    global mylog
    logname = "reportlog.txt"  
    time_now = asctime(localtime())
    
    mylog = open(logname, 'w')
    mylog.writelines(time_now + ".. starting \n")
    return	

if __name__=="__main__":

    #create the log file
    create_log()
    #get the settings from config.ini in same dir
    fields, path = get_fields()
    #open csv and write out header fields
    writer = csv.writer(open("report.csv", "wb"))
    writer.writerow(fields)
    #read files and output Excel csv
    read_file(fields, path, writer)
