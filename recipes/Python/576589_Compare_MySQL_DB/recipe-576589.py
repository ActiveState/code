# -*- coding: iso-8859-1 -*-
""" This module aims to compare 2 DB and check for differences.

    As it uses memory to compare table content, it may not be the right tool for huge tables.
    When you run the program, you are ask if you want a detailed comparison.
    As global comparison will list all the different tables, detailed comparison will output
    every different record (and will take longer to run)
"""
import os, os.path, MySQLdb, pprint, string

class prm(object):
    """ Class used to store global parameters
    """
    # Connexion parameters to the DB we want to compare
    # DB 1
    db1prms={"host":"127.0.0.1", "user":"myuser", "passwd":"mypassword", "db":"theFirstDB"}
    db1=MySQLdb.connect(db1prms["host"], db1prms["user"], db1prms["passwd"], db1prms["db"])

    # DB 2
    db2prms={"host":"168.25.15.10", "user":"myuser", "passwd":"mypassword", "db":"theSecondDB"}
    db2=MySQLdb.connect(db2prms["host"], db2prms["user"], db2prms["passwd"], db2prms["db"])

    # Outfile to store result
    outfile="out.txt"

class dbao(object):
    """ Utilities to interact with database
    """
    def __init__(self, db, name=''):
        self.db=db
        self.name=name
        self.cur=db.cursor()

    def rowmap(self, rows):
        """ returns a dictionary with column names as keys and values
        """
        cols = [column[0] for column in self.cur.description]
        return [dict(zip(cols, row)) for row in rows]

    def getRows(self, tbl):
        """ Returns the content of the table tbl
        """
        statmt="select * from %s" % tbl
        self.cur.execute(statmt)
        rows=list(self.cur.fetchall())
        return rows

    def getTableList(self):
        """ Returns the list of the DB tables
        """
        statmt="show tables"
        self.cur.execute(statmt)
        rows=list(self.cur.fetchall())
        return rows

class dbCompare(object):
    """ Core function to compare the DBs
    """
    def __init__(self):
        self.processDetailedComparison=string.lower(raw_input("Detailed Compare (y/n) ?")[0]) in ['o', 'y']

    def compareLists(self, l1, l2):
        result={'l1notInl2':[],
                'l2notInl1':[]}
        d1=dict(zip(l1, l1))
        d2=dict(zip(l2, l2))
        for row in l1:
            if not d2.has_key(row):
                result['l1notInl2'].append(row)
        for row in l2:
            if not d1.has_key(row):
                result['l2notInl1'].append(row)
        return result

    def process(self):
        # Récupération de la liste des tables de la première base
        of=outfile()
        db1=dbao(prm.db1, prm.db1prms["host"])
        tl1=db1.getTableList()
        # Récupération de la liste des tables de la deuxième base
        db2=dbao(prm.db2, prm.db2prms["host"])
        tl2=db2.getTableList()
        if tl1==tl2:
            of.write("Identical tables")
        else:
            print "Different tables"
            of.write("Different tables")
            cp=self.compareLists(tl1, tl2)
            if cp['l1notInl2'] != []:
                of.write("   --> Tables from %s missing in %s" % (db1.name, db2.name))
                of.write(string.join([t[0] for t in cp['l1notInl2']],', '))
            if cp['l2notInl1'] != []:
                of.write("   --> Tables from %s missing in %s" % (db2.name, db1.name))
                of.write(string.join([t[0] for t in cp['l2notInl1']], ', '))

        for tbl in tl1:
            if tbl in tl2:
                print tbl[0]
                rl1=db1.getRows(tbl)
                rl2=db2.getRows(tbl)
                if rl1==rl2:
                    of.write("         %s identical" % tbl)
                else:
                    print "ERROR : %s different" % tbl
                    of.write("ERROR : %s different" % tbl)
                    cp=self.compareLists(rl1, rl2)
                    if self.processDetailedComparison:
                        if cp['l1notInl2'] != []:
                            of.write("   --> Rows from %s@%s missing in %s" % (tbl, db1.name, db2.name))
                            of.write(db1.rowmap(cp['l1notInl2']))
                        if cp['l2notInl1'] != []:
                            of.write("   --> Rows from %s@%s missing in %s" % (tbl, db2.name, db1.name))
                            of.write(db2.rowmap(cp['l2notInl1']))

class outfile(object):
    """ To write in the outfile
    """

    def __init__(self):
        self.outFile=prm.outfile
        df=open(self.outFile,'w')
        df.close()

    def write(self, *msg):
        df=open(self.outFile,'a')
        for m in msg:
            if type(m) is dict or type(m) is list:
                df.write("%s\n" % pprint.pformat(m))
            else:
                df.write("%s\n" % str(m))
        df.close()

if __name__ == "__main__":
    dc=dbCompare()
    dc.process()
