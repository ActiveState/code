'''
generates a set of files by doing ASCII same size substitutions on an original file, controller by a csv file

 CSV FORMAT :
FILE NAME changes.csv 
first row: ignored  (colum names)
first column: filenames
Second row: original file name, strings to search
rest of rows: generated filename, strings to replace

USE
put this script, the csv and original file original in same folder, generated files go to the same folder

'''
import csv,sys
from codecs import ascii_encode
# lee csv
reader = list(csv.reader( open("changes.csv",  newline=''),delimiter=','))


# row 1 : original filename, strings to find
l0=reader[1]
items= len(l0)
#read original file as binary 
   
with open(l0[0],"rb") as f:
   s=bytes(f.read())
#generate output files
c=3   
for row in reader[2:]:
     l= row
     print(l)
     s1=s
     print (l)
     # do as many replaces as columns -1
     for i in range(1,items):
        #stop if replace is not same size as search 
        if len(l0[i])!=len(l[i]):
             print('Line ',c, l[i],' not same length as ', l0[i])
             sys.exit(0)
        s1=s1.replace(ascii_encode(l0[i])[0],ascii_encode(l[i])[0])
	#after replacements, write file	
     with open(l[0],"wb") as f1:
        f1.write(s1)
     c+=1    
       
       
