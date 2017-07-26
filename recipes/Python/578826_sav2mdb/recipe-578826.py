# -*- coding: utf-8 -*-

import sys
import os
import random

import pypyodbc
import savReaderWriter

__version__ = "1.0.0"
__author__ = "Albert-Jan Roskam"
__email__ = "@".join(["fomcl", "yahoo" + ".com"])

"""
sav2mdb.py: convert SPSS system files (codepage) to Microsoft Access files
"""

def get_table_name(filename):
    tbl = os.path.splitext(os.path.basename(filename))[0]
    return tbl.capitalize().replace(" ", "_")

def get_metadata(savFilename):
    """Gets variable names (list), variable types and formats (dict)"""
    with savReaderWriter.SavHeaderReader(savFilename) as header:
        varNames, varTypes = header.varNames, header.varTypes
        formats = header.formats
    return varNames, varTypes, formats

def sql_create_table(savFilename):
    """Generate SQL 'CREATE TABLE' statement on the basis of <savFilename>
    SPSS-to-SQL datatype translation:
    numeric, except date/time --> FLOAT
    date or time --> CHAR(26) (iso dates where applicable)
    string < 256 bytes --> CHAR of that length
    string >= 256 bytes --> TEXT
    $sysmis --> NULL
    """
    varNames, varTypes, formats = get_metadata(savFilename)
    tbl = get_table_name(savFilename)
    # if "id" happens to be an existing varname, then suffix the primary key
    suffix = "_%04d" % random.randint(1000, 9999) if "id" in varNames else ""
    sql = "CREATE TABLE %(tbl)s (id%(suffix)s COUNTER PRIMARY KEY,\n  "
    sql = [sql % locals()]
    for varName in varNames:
        varType = varTypes[varName]
        format_ = formats[varName].lower()
        dataType = "FLOAT" if varType == 0 else \
                   "CHAR(%d)" % varType if varType < 256 else "TEXT"
        dataType = "CHAR(26)" if "time" in format_ or \
                   "date" in format_ else dataType
        sql.append("%(varName)s %(dataType)s, \n  " % locals())
    return "".join(sql).rstrip(", \n  ") + "\n);"

def sql_insert_template(savFilename):
    """Generate SQL 'INSERT INTO' template, suitable for sql quote escaping"""
    varNames, varTypes, formats = get_metadata(savFilename)
    tbl = get_table_name(savFilename)
    varNames_ = ", ".join(varNames)
    insert = "INSERT INTO %(tbl)s (%(varNames_)s) VALUES " % locals()
    template = ", ".join(["?"] * len(varNames))
    return insert + "(" + template + ");\n"

def write_ms_access_file(savFilename, mdbFilename=None, overwrite=True):
    """Write the actual MS Access file"""
    if not sys.platform.startswith("win"):
        raise EnvironmentError("Sorry, Windows only")
    if not mdbFilename:
        mdbFilename = os.path.splitext(savFilename)[0] + ".mdb"
        mdbFilename = mdbFilename.replace(" ", "_")
    if os.path.exists(mdbFilename) and overwrite:
        os.remove(mdbFilename)

    create_table = sql_create_table(savFilename)
    insert_table = sql_insert_template(savFilename)
    pypyodbc.win_create_mdb(mdbFilename)
    try:
        conn_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=%s'
        connection = pypyodbc.connect(conn_string % mdbFilename)
        cursor = connection.cursor()
        cursor.execute(create_table)
        with savReaderWriter.SavReader(savFilename) as reader:
            for record in reader:
                cursor.execute(insert_table, tuple(record))
        cursor.commit()
    finally:
        connection.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            write_ms_access_file(sys.argv[1])
        elif len(sys.argv) == 3:
            write_ms_access_file(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 4:
            write_ms_access_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print ("Usage: sav2mdb savFilename[[, mdbFilename], overwrite]\n"
               "If overwrite (True/False) is specified, mdbFilename must\n"
               "also be specified")
