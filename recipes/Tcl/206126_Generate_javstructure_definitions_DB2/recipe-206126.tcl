echo off

echo **********************************************************
echo * call tcl script from within windows DB2 shell.
echo ********************************************************** 

set tclshell=c:\tcl\bin\tclsh84

echo db2cmd /w /i /c %tclshell% c:\scripts\tcl\dclgendb.tcl
db2cmd /w /i /c %tclshell% c:\scripts\tcl\dclgendb.tcl

-------------------------------------------------------------------

tcl script:

#!d:\\Tcl\\bin\\tclsh84

######################################
# generate describe reports.
######################################

proc dclgen {schema userid password database outputdir} {

    exec db2 connect to $database user $userid using $password

    set tables [split [exec db2 list tables for schema $schema] \n]

    set schema [string toupper $schema] 
    set spaces_     {\s+} 
    set characters_ {\S+} 
    set regexp_string ($characters_)($spaces_)($schema)

    foreach line $tables {

        if {[regexp $regexp_string $line match tablename spaces schema_name] == 1} {
	    puts "outputfile = $outputdir\\$tablename\.java"
	    exec db2dclgn -d $database -u $userid -p $password -t $schema.$tablename -l java -a replace -o $outputdir\\$tablename\.java
	    puts "outputfile = $outputdir\\$tablename\.txt"
            exec db2 describe "select * from $schema\.$tablename" >& $outputdir\\$tablename\.txt
	} else {
	    set continue true
	}
    }

    exec db2 terminate
}

######################################
# generate describe reports for db_one.
######################################

set userid     user1
set password   pass1

set database   db_one 
set schema     schema1
set outputdir  c:\\db2_reports\\db_one\\describe

dclgen $schema $userid $password $database $outputdir

######################################
# generate describe reports for db_two.
######################################

set database   db_two 
set schema     schema2
set outputdir  d:\\db2_reports\\db_two\\describe

dclgen $schema $userid $password $database $outputdir
