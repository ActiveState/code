# last updated
# 1/28/2015  added sql logging


import sys
import threading
import time
import queue
import csv
from SQLSMO import *



# =============== FUNCTIONS ===========================
def LogSQL(filename, CN, sql):
    """
    Appends to given log file the sql executed with this format:
    -----------------------------------
    --Server:   SERVERNAME
    --Database: DATABASE
    script line 1
    script line 2
    ...
    -----------------------------------
    """

    today = str(datetime.date.today())
    f = open(filename, 'a')
    s = "\n\n-----------------------------------------------------\n\n"
    s = s + '--Server:   ' + CN['servername'] + "\n"
    s = s + '--Database: ' + CN['db'] + "\n"
    s = s + '--Date:     ' + today + "\n\n"
    s = s + sql
    s = s + "\n\n-----------------------------------------------------\n\n"
    f.write(s)
    f.close()

def ReadCSV(filename):
    """
    Returns array with entries marked as ENABLED=Y in source file
    """

    ary = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if row[-1].strip() == 'Y':
                    ary.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    return ary


def ActionParsing(DBLIST2):
    """
    Executes the actions from the source file, passed as the DBLIST2 array
    """
    f = DBLIST2.pop()


    DESTSERVER = f[0]
    SOURCEDB = f[1]
    BACKUPFOLDER = f[2]
    DATAFOLDER = f[3]
    LOGFOLDER = f[4]
    DESTDB = f[5]
    ACTIONS = f[6]

    # open actions file, column 6
    action_list = []
    with open(ACTIONS, newline='') as g:
        action_l = g.readlines()
    for y in action_l:
        if y[0] != '#':
            action_list.append(y)

    CONNECTION = {}
    CONNECTION['servername'] = DESTSERVER
    CONNECTION['username'] = ''
    CONNECTION['password'] = ''
    CONNECTION['db'] = DESTDB


    msg = "\n"
    SQL = "\n"

    for m in action_list:
        m = m.strip()

        if m == 'BACKUP DATABASE FULL':
            # print('testing full backup')
            DB_BACKUP = BACKUPFOLDER + '\\' + DESTDB + '_backup_' + DatedString() + '.BAK'
            #database to backup is DESTDB
            smobackup = SQLSMO(CONNECTION, '', '', DB_BACKUP)
            smobackup.BackupDatabase()
            msg = msg + ' action:' + m + "\n"
            SQL = SQL + smobackup.sqlbackup + "\n\n"
            # msg = msg + " SQL: \n" + smobackup.sqlbackup + "\n"

        elif m == 'RESTORE DATABASE':
            try:
                BKFILE = GetLatestBackup(BACKUPFOLDER, '\\' + SOURCEDB + BACKUP_MASK)[-1]
            except IndexError:
                print('No backup file!')
                break

            smo3 = SQLSMO(CONNECTION, DATAFOLDER, LOGFOLDER, BKFILE)
            smo3.noexecute = NOEXECUTE_OPTION
            ok_to_restore = smo3.Ok_to_restore()
            if ok_to_restore == True:
                confirm_msg = 'Ok to restore'
            else:
                confirm_msg = 'NOT ok to restore'
                smo3.noexecute = 0

            smo3.RestoreDatabase()

            msg = msg + ' action:' + m + "\n"
            msg = msg + confirm_msg + "\n"
            SQL = SQL + smo3.sqlrestore + "\n\n"
            # msg = msg + " SQL: \n" + smo3.sqlrestore + "\n"
        elif m == 'KILL CONNECTIONS':
            r = KillConnections(CONNECTION, DESTDB)
            msg = msg + ' action:' + m + "\n"
            msg = msg + str(r) + "\n"
        elif m == 'SET DBOWNER: sa':
            s = 'USE [' + DESTDB + '] EXEC dbo.sp_changedbowner @loginame = N' + chr(39)+ 'sa' + chr(39) + ', @map = false'
            try:
                rows, fnames = SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing set dbwoner sa: ', inst)
            msg = msg + ' action:' + m + "\n"
            SQL = SQL + s + "\n\n"
            # msg = msg + " SQL: \n" + s + "\n"
        elif m == 'SYNC LOGINS':
            rows = SyncLogins(CONNECTION, DESTDB)
            msg = msg + ' action:' + m + "\n"
            for y in rows:
                msg = msg + str(y) + "\n"
        elif m == 'SET SIMPLE MODE':
            s = 'USE [master] ALTER DATABASE [' + DESTDB + '] SET RECOVERY SIMPLE WITH NO_WAIT'
            try:
                rows, fnames = SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing set simple mode ', inst)
            msg = msg + ' action:' + m + "\n"
            SQL = SQL + s + "\n\n"
            # msg = msg + " SQL: \n" + s + "\n"
        elif m == 'SHRINK LOG':
            s = '''
            declare @logfilename varchar(200)
            select @logfilename = name  from sysfiles where groupid = 0
            DBCC SHRINKFILE (@logfilename , 0, TRUNCATEONLY)
            '''
            s = 'USE [' + DESTDB + '] ' + s
            try:
                rows, fnames = SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing shrink log ', inst)
            msg = msg + ' action:' + m + "\n"
            SQL = SQL + s + "\n\n"
            # msg = msg +  " SQL: \n" + s + "\n"
    with lock:
        print(msg)
        print(f)
        LogSQL('SqlScripts.sql', CONNECTION, SQL)
    return f


#threading functions

def do_work(item):
    """
    do lengthy work
    """

    start2 = time.perf_counter()         # saving start time
    line = ActionParsing(DBLIST2)

    DICT_RESULTS = {}
    ThreadItem = threading.current_thread().name + '_' + str(item)
    DICT_RESULTS[ThreadItem] = {}
    DICT_RESULTS[ThreadItem]['line processed:'] = line

    time_elapsed = time.perf_counter() - start2
    DICT_RESULTS[ThreadItem]['ELAPSED TIME'] = time_elapsed
    DICT_RESULTS2.append(DICT_RESULTS)
    # -----------End of do_work------------------------------

def worker():
    """
    The worker thread pulls an item from the queue and processes it
    """

    while True:
        item = q.get()
        do_work(item)
        q.task_done()

# ===============End of functions=======================


# ============== Program Start=========================
# some global values
DICT_RESULTS2 = []                      # used to store execution messages, to be displayed at the end
BACKUP_MASK = '*.bak'                   # backup mask for files in backup folder
NOEXECUTE_OPTION = 0                    # 1 = no execution, 0 = yes execution
THREAD_POOL = 0                         # 0 means will process all entries in source file in its own thread

# csv file with list of Servers,DBs and desired actions
SOURCEFILE = r'C:\Users\python\PycharmProjects\codecamp\DBLIST_ACTIONS.csv'
DBLIST2 = ReadCSV(SOURCEFILE)
items_to_process = len(DBLIST2)
if THREAD_POOL == 0:
    THREAD_POOL = items_to_process

print('Total items to process:', items_to_process)
print('Thread pool (concurrent processes): ', THREAD_POOL)
if NOEXECUTE_OPTION == 0:
    print('Execution option is yes')
else:
    print('No execution')

# lock to serialize console output
lock = threading.Lock()

# Create the queue and thread pool.
q = queue.Queue()
for i in range(THREAD_POOL):
    t = threading.Thread(target=worker)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()

# stuff work items on the queue.
start1 = time.perf_counter()         # saving start time
for item in range(len(DBLIST2)):
    # print('item:', item)
    q.put(item)

q.join()       # block until all tasks are done


print('time:', time.perf_counter() - start1)
for x in DICT_RESULTS2:
    print(x)
