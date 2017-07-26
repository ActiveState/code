##
## XMLPush
##
## A small utility to move XML as exported from SQL Server or MS Access to a
## mySQL table. 
##
## Not too fancy, but gets the job done. As with all recipes, season to taste
## depending on your needs.
##
##  Albert L. Perrien II
##  08 March 2011
##  aperrien@razodisk.com
##

import re
from lxml import etree
import MySQLdb


def XMLPush(datafile,server,dbuser,password,dbname,table)


    def quote(text):
        return "'" + text + "'"

    def doublequote(text):
        return '"' + text + '"'

    connection = MySQLdb.connectionect (host = server,
                           user = dbuser,
                           passwd = password,
                           db = dbname)

    cursor = connection.cursor()

    tree = etree.parse(datafile)

    root = tree.getroot()


    # Parse out data from XML
    data = []
    for child in root:
        datarow = {}
        for leaf in child:
            datarow[leaf.tag] = leaf.text
        data.append(datarow)

    # Push data to DB
    statements = []
    for row in data:
        columns = []
        values = []
        for item in row:
            # Reformatting data to mySQL formats
            columns.append(item.replace(" ",""))
            temp = row[item]
            values.append(quote(temp.replace("'","")))

        # Push data to table
        statement = "INSERT INTO " + table + " (" + ",".join(columns) + ") VALUES (" + \
                    ",".join(values) + ")"

        statements.append(statement)

    for statement in statements:
        cursor.execute(statement)
        connection.commit()
        
    
    connection.close()



XMLPush("MainTable.xml","mySQL-Server","mySQL-User","mySQL-Password","DB_Name","Table")
