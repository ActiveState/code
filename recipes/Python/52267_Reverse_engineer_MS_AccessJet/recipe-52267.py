# jet2sql.py - M.Keranen <mksql@yahoo.com> [07/12/2000]
# --------------------------------------------------------------------
# Creates ANSI SQL DDL from a MS Jet database file, useful for reverse
# engineering database designs in E/R tools.
#
# Requires DAO 3.6 library.
# --------------------------------------------------------------------
# Usage: python jet2sql.py infile.MDB outfile.SQL

import sys, string, pythoncom, win32com.client

const = win32com.client.constants
daoEngine = win32com.client.Dispatch('DAO.DBEngine.36')

class jetReverse:
    def __init__ (self, infile):

        self.jetfilename=infile
        self.dtbs = daoEngine.OpenDatabase(infile)

        return

    def terminate(self):
        return

    def writeTable(self, currTabl):
        self.writeLine('\ncreate table ' + chr(34) + currTabl.Name + chr(34),"",1)
        self.writeLine('(',"",1)

        # Write Columns
        cn=0
        for col in currTabl.Fields:
            cn = cn +1
            self.writeColumn(col.Name, col.Type, col.Size, col.Required, col.Attributes, col.DefaultValue, col.ValidationRule, currTabl.Fields.Count-cn)

        # Validation Rule
        tablRule = currTabl.ValidationRule
        if tablRule <> "":
            tablRule = "    check(" + tablRule + ") "
            self.writeLine("",",",1) # add a comma and CR previous line
            self.writeLine(tablRule,"",0)

        # Primary Key
        pk=self.getPrimaryKey(currTabl)
        if pk <> "":
            self.writeLine("",",",1) # add a comma and CR previous line
            self.writeLine(pk,"",0)

        # End of table
        self.writeLine("","",1) # terminate previous line
        self.writeLine(');',"",1)

        # Write table comment
        try: sql = currTabl.Properties("Description").Value
        except pythoncom.com_error: sql=""
        if sql <> "":
           sql = "comment on table " + chr(34) + currTabl.Name + chr(34) + " is " + chr(34) + sql + chr(34) +";"
           self.writeLine(sql,"",1)

        # Write column comments
        for col in currTabl.Fields:
            try: sql = col.Properties("Description").Value
            except pythoncom.com_error: sql=""
            if sql <> "":
               sql = "comment on column " + chr(34) + currTabl.Name + chr(34) + "." + chr(34) + col.Name + chr(34) + " is " + chr(34) + sql + chr(34) + ";"
               self.writeLine(sql,"",1)

        # Write Indexes
        self.writeIndexes(currTabl)

        return

    def writeColumn(self, colName, colType, length, requird, attributes, default, check, colRix):
        # colRix: 0 based index of column from right side. 0 indicates rightmost column

        if colType == const.dbByte: dataType = "Byte"
        elif colType == const.dbInteger: dataType = "Integer"
        elif colType == const.dbSingle: dataType = "Single"
        elif colType == const.dbDouble: dataType = "Double"
        elif colType == const.dbDate: dataType = "DateTime"
        elif colType == const.dbLongBinary: dataType = "OLE"
        elif colType == const.dbMemo: dataType = "Memo"
        elif colType == const.dbCurrency: dataType = "Currency"
        elif colType == const.dbLong:
            if  (attributes & const.dbAutoIncrField): dataType = "Counter"
            else: dataType = "LongInteger"
        elif colType == const.dbText:
            if length == 0: dataType = "Text"
            else: dataType = "char("+str(length)+")"
        elif colType == const.dbBoolean:
            dataType = "Bit"
            if default == "Yes": default = "1"
            else: default = "0"
        else:
            if length == 0: dataType = "Text"
            else: dataType = "Text("+str(length)+")"

        if default <> "":
            defaultStr = "default " + default + " "
        else: defaultStr = ""

        if check <> "":
            checkStr = "check(" + check + ") "
        else:
            checkStr = ""

        if requird or (attributes & const.dbAutoIncrField):
            mandatory = "not null "
        else:
            mandatory = ""

        sql = "    " + chr(34) + colName + chr(34) + " " + dataType + " " + defaultStr + checkStr + mandatory
        if colRix > 0:
            self.writeLine(sql,",",1)
        else:
            self.writeLine(sql,"",0)

        return

    def getPrimaryKey(self, currTabl):

        # Get primary key fields
        sql = ""
        for idx in currTabl.Indexes:
           if idx.Primary:
              idxName = idx.Name
              sql = "    primary key "
              cn=0
              for col in idx.Fields:
                  cn=cn+1
                  sql = sql + chr(34) + col.Name + chr(34)
                  if idx.Fields.Count > cn : sql = sql + ","
        return sql

    def writeIndexes(self, currTabl):

        # Write index definition
        nIdx = -1
        for idx in currTabl.Indexes:
            nIdx = nIdx + 1
            idxName = idx.Name
            tablName = currTabl.Name
            if idx.Primary:
                idxName = tablName + "_PK"
            elif idxName[:9] == "REFERENCE":
               idxName = tablName + "_FK" + idxName[10:]
            else:
                idxName = tablName + "_IX" + str(nIdx)

            sql = "create "
            if idx.Unique: sql = sql + "unique "
            if idx.Clustered: sql = sql + "clustered "
            sql = sql + "index " + chr(34) + idxName + chr(34)
            sql = sql + " on " + chr(34) + tablName + chr(34) + " ("

            # Write Index Columns
            cn=0
            for col in idx.Fields:
                cn = cn + 1
                sql = sql + chr(34) + col.Name + chr(34)
                if col.Attributes & const.dbDescending:
                    sql = sql + " desc"
                else:
                    sql = sql + " asc"
                if idx.Fields.Count > cn: sql = sql + ","

            sql=sql + " );"

            self.writeLine(sql,"",1)
        return

    def writeForeignKey(self, currRefr):

        # Export foreign key
        sql = "\nalter table " + chr(34) + currRefr.ForeignTable + chr(34)
        self.writeLine(sql,"",1)

        sql = "    add foreign key ("
        cn = 0
        for col in currRefr.Fields:
            cn = cn + 1
            sql = sql + chr(34) + col.ForeignName + chr(34)
            if currRefr.Fields.Count > cn: sql = sql + ","
            
        sql = sql + ")"
        self.writeLine(sql,"",1)

        sql = "    references " + chr(34) + currRefr.Table + chr(34) + " ("
        cn = 0
        for col in currRefr.Fields:
            cn = cn + 1
            sql = sql + chr(34) + col.Name + chr(34)
            if currRefr.Fields.Count > cn: sql = sql + ","

        sql = sql + ")"
        if (currRefr.Attributes & const.dbRelationUpdateCascade) <> 0:
           sql = sql + " on update cascade"
        if (currRefr.Attributes & const.dbRelationDeleteCascade) <> 0:
           sql = sql + " on delete cascade"
        sql=sql+";"
        self.writeLine(sql,"",1)

        return

    def writeQuery(self, currQry):

        sql = "\ncreate view " + chr(34) + currQry.Name + chr(34) + " as"
        self.writeLine(sql,"",1)

        # Write Query text
        sql=string.replace(currQry.SQL,chr(13),"") # Get rid of extra linefeeds
        self.writeLine(sql,"",1)

        # Write Query comment
        try: sql = currQry.Properties("Description").Value
        except pythoncom.com_error: sql=""
        if sql <> "":
            sql =  "comment on table " + chr(34) + currQry.Name + chr(34) + " is " + chr(34) + sql + chr(34)
            self.writeLine(sql,"",1)
            
        return

    def writeLine(self,strLine, delimit, newline):
        # Used for controlling where lines terminate with a comma or other continuation mark
        sqlfile.write(strLine)
        if delimit: sqlfile.write(delimit)
        if newline: sqlfile.write('\n')
        return


if __name__ == '__main__':
    if len(sys.argv)<2:
        print "Usage: jet2sql.py infile.mdb outfile.sql"
    else:
        jetEng = jetReverse(sys.argv[1])
        outfile = sys.argv[2]

        sqlfile = open(outfile,'w')

        print "\nReverse engineering %s to %s" % (jetEng.jetfilename, outfile)

        # Tables
        sys.stdout.write("\n   Tables")
        for tabl in jetEng.dtbs.TableDefs:
            sys.stdout.write(".")
            if tabl.Name[:4] <> "MSys" and tabl.Name[:4] <> "~TMP":
                jetEng.writeTable(tabl)

        # Relations / FKs
        sys.stdout.write("\n   Relations")
        for fk in jetEng.dtbs.Relations:
            sys.stdout.write(".")
            jetEng.writeForeignKey(fk)

        # Queries
        sys.stdout.write("\n   Queries")
        for qry in jetEng.dtbs.QueryDefs:
            sys.stdout.write(".")
            jetEng.writeQuery(qry)

        print "\n   Done\n"
        
        # Done
        sqlfile.close()
        jetEng.terminate()
