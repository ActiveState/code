#!/export/home/www.netuni.nl/local/bin/python

import sys, os, getopt, getpass
import MySQLdb

def ohmysqldump(db, user, passwd, excluded, options, host=''):
    conn = MySQLdb.connect(host='', db=db, user=user, passwd=passwd)
    c = conn.cursor()
    sql = 'show tables;'
    c.execute(sql)
    tables = c.fetchall()
    conn.close()
    arguments = [db]
    for table in tables:
        try:
            if not table[0] in excluded:
                arguments.append(table[0])
        except:
            print "You cannot exclude non-existing tables."
            sys.exit(1)
    arguments.insert(0, "mysqldump")
    command = 'mysqldump'
    os.execvp(command, arguments)

def usage():
    print """

ohmysqldump is a wrapper for mysqldump including an option to dump a
mysqldatabase EXCEPT the listed tables.

Usage: [OPTIONS] [database] [tables]

  -E, exclude           Exclude the tables
  
The -p and --password options in mysqldump has an optional argument. This
technique isn't supported (consider -p database table. Is 'database' a
password? Or is it the name of the database?). You can store the password in
an optionfile (~/.my.cnf) or ohmysqldump will ask for it (twice).

All (other) options in mysqldump are supported. 
    """
    #mysqldump --help follows:
    #os.execvp("mysqldump", ["mysqldump", "--help"])

def main():

    shortoptions = "aAB#:?cCeEFOfh:lKntdpP:qQS:Tu:vVw:Xx"
    
    longoptions = ["all", "debug=", "character-sets-dir=", "help", "complete-insert", \
    "compress", "default-character-set=", "extended-insert", "add-drop-table", \
    "add-locks", "allow-keywords", "delayed-insert", "master-data", "flush-logs", \
    "force", "host=", "lock-tables", "no-autocommit", "disable-keys", \
    "no-create-db", "no-create-info" "no-data", "opt", "password=", "port=", \
    "quick", "quote-names", "socket=", "tab=", "user=", "verbose", "version", \
    "where=", "xml", "first-slave" "fields-terminated-by=", \
    "fields-enclosed-by=", "fields-optionally-enclosed-by=", \
    "fields-escaped-by=", "lines-terminated-by=", "all-databases", \
    "databases", "tables", "exclude"]

    #Try to find additional info in the mysql option-files
    f = os.popen("my_print_defaults client mysqldump")
    myoptions = f.readlines()
    f.close
    for line in myoptions:
        if len(line):
            # Inject it into the commandline for easy parding by getopt
            # Inject it in front so any commandline-parameters will override
            # the optionfile
            sys.argv.insert(1,line.replace("\n",""))

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortoptions, longoptions)
    except getopt.GetoptError:
        #print "error"
        # print help information and exit
        usage()
        sys.exit(2)
        
    if not opts and not args:
        usage()
        sys.exit()

    options = []
    
    runohmy = 0
    askpasswd = 0
    
    db=""
    user = ""
    host=""
    passwd = ""

    for opt, arg in opts:
        # Catch some options to handle here
        if opt in ["-?", "--help"]:
            usage()
        elif opt in ["-E", "--exclude"]:
            runohmy = 1
            if len(args)>1:
                db = args[0]
                excluded = args[1:]
                # Don' pass it along
                continue
            else:
                usage()
                sys.exit(1)
        elif opt in ["-p", "--password"]:
            if arg:
                passwd = arg
            else:
                askpasswd = 1
        elif opt in ["-u", "--user"]:
            user = arg
        elif opt in ["-h", "--host"]:
            host = arg
        elif opt in ["-V", "--version"]:
            print "ohmysqldump v0.3"
            os.execvp("mysqldump", ["mysqldump", "--version"])

        if opt[2:]+"=" in longoptions:
            options.append(opt+"="+arg)
        elif opt[1:]+":" in shortoptions:
            options.append(opt)
            options.append(arg)
        else:
            options.append(opt+arg)

    if not runohmy:
        options.insert(0, "mysqldump")
        command = 'mysqldump'
        for arg in args:
            options.append(arg)
        os.execvp(command, options)
    else:
        if (not passwd and askpasswd):
            passwd = getpass.getpass("password: ")
        if not (user and (passwd and not askpasswd) and db and excluded):
            usage()
            sys.exit(1)
        else:
            ohmysqldump(db, user, passwd, excluded, options, host='')

if __name__ == "__main__":
    main();
