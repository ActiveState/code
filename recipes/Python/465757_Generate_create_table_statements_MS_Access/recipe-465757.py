# simplistic state machine for reading an Access Database Documenter text file
# and generating create table sql statements compatible with MySQL
# by Bob Gailer 01/02/06 bgailer@alum.rpi.edu
import re
# accomodate a space as part of fieldname or type e.g. e.g. Expense Type, Long Integer
pat = re.compile(r"\s*(\S* ?\S* ?\S* ?\S*)")
out = file("documenter2.txt", "w")
def newTbl(line):
  global tbl, outLine, lookFor
  newtbl = line.split()[1]
  # could be page header or new table
  if tbl != newtbl:
    tbl = newtbl
    if outLine: out.write(outLine[:-2] + ")\n")
    outLine = "create table %s (" % tbl
    lookFor = "columns"
    return True
# target types taken from MySQL documentation
types = {"text": "varchar",  "byte": "int1",   "date/time": "timestamp", 
         "single": "float",  "integer": "int", "hyperlink": "varchar", "long integer": "int",
         "memo": "longtext", "yes/no": "int1", "currency": "decimal(10,2)"}
outLine = tbl = ""
lookFor = "table:"
specialChars = """ ~@#$%^&*()-=+\\|{};:'",<>/?|"""
replacements = '_'*len(specialChars)
for lineIn in file("documenter.txt"):
  lineIn = lineIn.lower()
  line = lineIn.strip()
  if lookFor == "table:":
    if line.startswith(lookFor):
      if newTbl(line):continue 
  elif lookFor == "columns":
    if line.startswith(lookFor): lookFor = "name"
  elif lookFor == "name":
    if line.startswith(lookFor): lookFor = "table indexes, relationships, table:"
  elif lookFor == "table indexes, relationships, table:":
    if line.startswith("table indexes"): lookFor = "next table"
      # future objective: parse indexes to identify primary key and generate create index statements
    if line.startswith("relationships"): lookFor = "table:"
    if line.startswith("table:"):
      if newTbl(line):continue
    if lineIn[:9] == "         " and lineIn[9] != " ": # field name
      print line # diagnostic tool; can drop
      fld, type, length = pat.findall(line)[:3]
      outLine += "%s %s" % (fld.strip().replace(specialChars, replacements), types[type.strip()])
      if type == "text": outLine += "(%s)" % length
      lookFor = "allowzerolength"
  elif lookFor == "allowzerolength":
    if line.startswith(lookFor):
      null = (" not", "")[line.split()[1] == "False"]
      outLine += null + " null, "
      lookFor = "table indexes, relationships, table:"
if outLine: out.write(outLine[:-2] + ")\n")
out.close()
