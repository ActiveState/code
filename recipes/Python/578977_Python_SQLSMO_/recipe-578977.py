# SQLSMO.py
# Created by Jorge Besada
# Last modified 3/16/2015

import os
import glob
import time
import datetime
import subprocess

# --------------Functions-----------------------------------------------------------------------------
def SqlExecute(conn, sqlquery=''):

    """
    Executes sqlquery and returns lists with column names and data
    The connection info is passed as a dictionary with these required keys:
    servername, username,password
    If username is empty will use integrated security
    These keys are optional: defdb, colseparator
    """

    if 'colseparator' not in conn.keys():
        conn['colseparator'] = chr(1)
    if conn['username'] == '':
        constr = "sqlcmd -E -S" + conn['servername'] + "  /w 8192 -W " + ' -s' + conn['colseparator'] + '  '
    else:
        constr = "sqlcmd -U" + conn['username'] + " -P" + conn['password'] + ' -S' + conn['servername'] + '  /w 8192 -W  -s' + conn['colseparator'] + '  '

    # now we execute
    try:
        data = subprocess.Popen(constr + '-Q"' + sqlquery + '"', stdout=subprocess.PIPE).communicate()
    except Exception as inst:
        print('Exception in SqlExecute:', inst)
        return -1

    records = []
    lst = data[0].splitlines()
    # lst[0] column names;  lst[1] dashed lines, (skip); lst[2:] data
    # now we decode
    for x in lst:
        try:
            #try default utf-8 decoding
            line = x.decode()
        except UnicodeDecodeError:
            #in case of weird characters this one works most of the time
            line = x.decode('ISO-8859-1')
        lst2 = line.split(conn['colseparator'])
        records.append(lst2)
    fieldnames = records[0]
    data = records[2:]

    return data, fieldnames


def GetLatestBackup(dirpath, filter='\*.*'):
    """
    Returns folder contents sorted by modified date
    Sample use:
    backupfolder = r'\\SERVERNAME\SQLBackups1\SQLBackupUser'
    This brings all files
    lst = GetLatestBackup(backupfolder)
    Here we bring a subset using filter string
    filter = '\DATABASE_*.bak'
    lst = GetLatestBackup(backupfolder, filter)
    """

    a = [s for s in glob.glob(dirpath + filter) if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

def DeleteOlderFiles(workfolder, days):
    """
    Used to delete older backups in a folder, days is retention days
    Sample use to delete all files in C:temp with created date older than 3 days:
    DeleteOlderFiles(r'c:\temp', 3)
    """

    # os, time already imported

    now = time.time()
    cutoff = now - (days * 86400)
    filelist = os.listdir(workfolder)
    for x in filelist:
            if os.path.isfile( workfolder + '\\' + x):
                t = os.stat( workfolder + '\\' + x )
                c = t.st_ctime

                # delete file if older than a week
                if c < cutoff:
                    print('deleting ' + x)
                    os.remove(workfolder + '\\' + x )


def KillConnections(conn, db):
    """
    Kills connections in database if database exists
    """

    s = 'SET NOCOUNT ON DECLARE @kill varchar(8000) = ' + chr(39) + chr(39) + ';'
    s += ' SELECT @kill = @kill + ' + chr(39) + 'kill ' + chr(39) + '  + CONVERT(varchar(5), spid) + ' + chr(39) + ';' + chr(39)
    s += ' FROM master..sysprocesses WHERE dbid = db_id(' + chr(39) + db + chr(39) + ')'
    s += ' select @kill; EXEC(@kill);'

    rows, fnames = [], []
    try:
        rows, fnames = SqlExecute(conn, s)
    except Exception as inst:
            print('Error killing connections: ', inst)
    return rows

def SyncLogins(conn, db):
    s = '''
    DECLARE @UserName nvarchar(255)
    DECLARE @SQLCmd nvarchar(511)
    DECLARE orphanuser_cur cursor for
    SELECT UserName = name
    FROM sysusers
    WHERE issqluser = 1 and (sid is not null and sid <> 0x0) and suser_sname(sid) is null ORDER BY name
    OPEN orphanuser_cur
    FETCH NEXT FROM orphanuser_cur INTO @UserName
    WHILE (@@fetch_status = 0)
    BEGIN
    select @UserName + ' user name being resynced'
    set @SQLCmd = 'ALTER USER '+@UserName+' WITH LOGIN = '+@UserName
    EXEC (@SQLCmd)
    FETCH NEXT FROM orphanuser_cur INTO @UserName
    END
    CLOSE orphanuser_cur
    DEALLOCATE orphanuser_cur
    '''
    # sqlcmd needs single line sql commands for the -Q option
    s = s.replace("\n", ' ')
    sqlsynclogins = 'SET NOCOUNT ON USE [' + db + '] ' + s
    rows, fnames = [], []
    try:
        rows, fnames = SqlExecute(conn, sqlsynclogins)
    except Exception as inst:
        print('Error executing fix logins: ', inst)
    return rows

def DatedString():
    """
    Returns dated string with this format
    2014_12_30_135857_4581860
    """

    from datetime import datetime
    now = str(datetime.now())
    now = now.replace('-', '_')
    now = now.replace(' ', '_')
    now = now.replace(':', '')
    now = now.replace('.', '_') + '0'

    return now


def BuildTlogSQL(dbname, sourcedb, bkfolder, recovery = 'NORECOVERY', BACKUP_MASK = '_backup_20*.BAK', LOG_MASK = '_backup_20*.TRN'):
    """
    - check for log backups
    DECLARE backupFiles CURSOR FOR
    SELECT backupFile
    FROM @fileList
    WHERE backupFile LIKE '%.TRN'
    AND backupFile LIKE @dbName + '%'
    AND backupFile > @lastFullBackup
    OPEN backupFiles
    -- Loop through all the files for the database
    FETCH NEXT FROM backupFiles INTO @backupFile
    WHILE @@FETCH_STATUS = 0
    BEGIN
       SET @cmd = 'RESTORE LOG ' + @dbName + ' FROM DISK = '''
           + @backupPath + @backupFile + ''' WITH NORECOVERY'
       PRINT @cmd
       FETCH NEXT FROM backupFiles INTO @backupFile
    END
    CLOSE backupFiles
    DEALLOCATE backupFiles
    -- 6 - put database in a useable state
    SET @cmd = 'RESTORE DATABASE ' + @dbName + ' WITH RECOVERY'
    PRINT @cmd
    """

    BKFILE = '____.BAK'
    try:
        BKFILE = GetLatestBackup(bkfolder, '\\' + sourcedb + BACKUP_MASK)[-1]   # BACKUP_MASK = '_backup_20*.BAK'
    except IndexError:
        pass

    s = ''

    filter = '\\' + sourcedb + LOG_MASK
    filelist = GetLatestBackup(bkfolder, filter )

    if len(filelist) == 0:
        print('No log files for ' + sourcedb)
        if recovery == 'RECOVERY':
            s = 'RESTORE DATABASE ' + dbname + ' WITH RECOVERY' + chr(13) + chr(10) + 'GO ' + chr(13) + chr(10)
            return s
    else:
        for x in filelist:
            if x[:-4] > BKFILE[:-4]:        # this means the log file is older than the latest full backup file
                s += 'RESTORE LOG ' + dbname + ' FROM DISK = ' + chr(39) + x + chr(39) + \
                    ' WITH NORECOVERY' + chr(13) + chr(10) + 'GO ' + chr(13) + chr(10)
        if x[:-4] > BKFILE[:-4]:
            if recovery == 'RECOVERY':
                s += 'RESTORE DATABASE ' + dbname + ' WITH RECOVERY' + chr(13) + chr(10) + 'GO ' + chr(13) + chr(10)
        return s

# ----------------End of functions----------------------------------------


# -----------------Start of class SQLSMO----------------------------------

class SQLSMO:
    def __init__(self, conn, datafilepath='', logfilepath='', backupfilepath='' ):
        self.conn = conn
        self.datafolder = datafilepath
        self.logfolder = logfilepath
        self.logfilename = ''
        self.backupfile = backupfilepath
        self.currdb = conn['db']
        self.defdb = 'master'
        self.noexecute = 0                  #1=no execute, 0=yes to execute
        self.sqlrestore = ''
        self.sqlbackup = ''

        self.sqlfilelist =          'SET NOCOUNT ON RESTORE FILELISTONLY FROM DISK = ' + chr(39) + self.backupfile + chr(39)
        self.sqlfileheader =        'SET NOCOUNT ON RESTORE HEADERONLY FROM DISK = ' + chr(39) + self.backupfile + chr(39)
        self.sqlxp_fixeddrives =    'SET NOCOUNT ON EXEC master..xp_fixeddrives'
        self.sqlsphelpdb =          'SET NOCOUNT ON select name, physical_name, (size * 8/1000) as size, data_space_id from ['+ self.currdb + '].sys.database_files'

        self.datafiles_size_existing = 0    #info from existing database --- populated by GetDatabaseInfo
        self.logfiles_size_existing = 0     #info from existing database --- populated by GetDatabaseInfo

        self.dictdbinfo = {}                #info from existing database --- populated by GetDatabaseInfo
        self.dictfiles = {}                 #info from backup file       --- populated by GetBackupInfo
        self.dictheader = {}                #info from backup file       --- populated by GetBackupInfo
        self.dictfreespace = {}             #info on disk space          --- populated by GetFreeSpace

        self.datafiles_size = 0             #info from backup file       --- populated by GetBackupInfo
        self.logfiles_size = 0              #info from backup file       --- populated by GetBackupInfo

        self.backup_options = {'backup_type': 'DATABASE', 'compression': False} #options for backup_type: LOG, DIFFERENTIAL
        self.restore_options = {'dated_file_names': False,
                                'original_file_names': False,
                                'restore_type': 'DATABASE',                     #options: LOG
                                'recovery': 'RECOVERY',                         #options: NORECOVERY
                                'replace': True                                 #option: False
                               }

    def GetDataseInfo(self):
        """
        Returns info about existing database
        Return values are rows and column names
        It populates these variables
        self.logfiles_size_existing
        self.datafiles_size_existing
        """
        self.logfiles_size_existing  = 0.0
        self.datafiles_size_existing = 0.0

        rows, fnames = [], []
        try:
            # fnames are: name physical_name size data_space_id
            rows, fnames = SqlExecute(self.conn, self.sqlsphelpdb)
        except Exception as inst:
            print('No existing database information', inst)
            self.dictdbinfo = {}
            return rows, fnames


        for x in rows:
            self.dictdbinfo[x[0]] = x[1:]       #using as key file name

        logsize = 0.0
        datasize = 0.0
        for x in rows:
            if x[-1] == '0':                    #x[-1] is data_space_id, 0 is log, anything else is data
                gb = float(x[-2])/1000
                logsize += gb
            else:
                gb = float(x[-2])/1000
                datasize += gb

        self.logfiles_size_existing = logsize
        self.datafiles_size_existing = datasize

        return rows, fnames

    def GetBackupInfo(self):
        """
        Returns two dictionaries
        ---------------dictionary with backup file contents------------------------------------------------------------
        'LogicalName', 'PhysicalName', 'Type', 'FileGroupName', 'Size', 'MaxSize',
        'FileId', 'CreateLSN', 'DropLSN', 'UniqueId', 'ReadOnlyLSN', 'ReadWriteLSN',
        'BackupSizeInBytes', 'SourceBlockSize', 'FileGroupId', 'LogGroupGUID', 'DifferentialBaseLSN',
        'DifferentialBaseGUID', 'IsReadOnly', 'IsPresent', 'TDEThumbprint'
        The dictionary key is the LogicalName
        ---------------dictionary with contents of backup header--------------------------------------------------------
        BackupTypeDescription Database
        FirstRecoveryForkID {32840502-607C-441E-9439-D7364C4BBFFF}
        CheckpointLSN 93565000000174200025
        FamilyGUID {52405D85-E8F5-4AD8-92C9-5EC262B2A651}
        SoftwareVendorId 4608
        DatabaseBackupLSN 93487000002002400022
        BackupFinishDate 2014-08-27 02:59:05+00:00
        CodePage 0
        DatabaseVersion 661
        ExpirationDate None
        SortOrder 52
        CompatibilityLevel 100
        Collation SQL_Latin1_General_CP1_CI_AS
        BindingID {09CD467E-193E-4A29-82C9-709AE5CCA9D4}
        HasIncompleteMetaData False
        RecoveryForkID {32840502-607C-441E-9439-D7364C4BBFFF}
        SoftwareVersionMinor 50
        Position 1
        SoftwareVersionBuild 2500
        SoftwareVersionMajor 10
        Containment 0
        MachineName SQLSERVERNAME
        BackupType 1
        HasBackupChecksums False
        DifferentialBaseGUID None
        UserName DOMAIN\_sql_account
        IsSingleUser False
        ForkPointLSN None
        DifferentialBaseLSN None
        IsCopyOnly False
        RecoveryModel FULL
        BeginsLogChain False
        IsSnapshot False
        IsReadOnly False
        BackupName DatabaseName_backup_2014_08_27_020001_3668583
        FirstLSN 93565000000174200025
        BackupSetGUID {CFF54981-E420-477C-ADBB-B32FDC31EAF0}
        DeviceType 2
        IsDamaged False
        BackupSize 233650456576
        Compressed 1
        UnicodeComparisonStyle 196609
        HasBulkLoggedData False
        Flags 512
        CompressedBackupSize 56790589512
        BackupDescription None
        ServerName SQLSERVERNAME\INSTANCE
        DatabaseName DatabaseName
        UnicodeLocaleId 1033
        BackupStartDate 2014-08-27 02:18:38+00:00
        IsForceOffline False
        LastLSN 93565000000878200001
        DatabaseCreationDate 2012-06-06 15:47:24+00:00
        """

        # backup files info
        rows, fnames = [], []
        try:
            rows, fnames = SqlExecute(self.conn, self.sqlfilelist)
        except Exception as inst:
            print(inst)
            self.dictfiles = {}

        self.logfiles_size = 0.0
        self.datafiles_size = 0.0
        for x in rows:
            self.dictfiles[x[0]] = x[1:]                                    #using as key file name
            try:
                if x[2] == 'L':                                             #x[2] is Type, D or L
                    self.logfiles_size += float(float(x[4])/1000000000)     #x[4] is Size in bytes
                    self.logfilename = x[0]
            except IndexError:
                print('-Check backup file exists')
                print('-Check backup file version, maybe higher than current SQL version')
                print('-Check SQL server account has access to the backup file')
                exit()
            if x[2] == 'D':
                self.datafiles_size += float(float(x[4])/1000000000)

        # backup header info
        try:
            rows, fnames = SqlExecute(self.conn, self.sqlfileheader)
        except Exception as inst:
            print(inst)
            self.dictheader = {}

        i = 0
        for x in fnames:
            self.dictheader[x] = rows[0][i]
            if x == 'DatabaseName':
                self.defdb = self.dictheader[x]
            i += 1

        return self.dictfiles, self.dictheader

    def GetFreeSpace(self):
        """
        Returns dictionary with drive letters and free space in GB
        C	11.553        D	26.849        E	31.829        F	64.230
        """

        self.dictfreespace = {}
        rows, fnames = [], []
        try:
            rows, fnames = SqlExecute(self.conn, self.sqlxp_fixeddrives)
        except Exception as inst:
            print('Error getting disk space', inst)
            return self.dictfreespace

        i = 0

        for x in rows:
            self.dictfreespace[x[0]] = str(float(rows[i][1])/1000)   # changing to gb
            i += 1
        return self.dictfreespace

    def Ok_to_restore(self):
        """
        Check for space available in destination
        If database exists (it is an overwrite) the space used by it is considered
        """
        # Populate these two: self.datafiles_size_existing, self.logfiles_size_existing
        self.GetDataseInfo()

        # Populate these two: self.datafiles_size, self.logfiles_size
        self.GetBackupInfo()

        dict_freespace = self.GetFreeSpace()
        # print('freespace dict')
        # print(dict_freespace)
        data_disk = 0.0
        log_disk = 0.0
        for x in dict_freespace.keys():                             #x is the drive letter
            if self.datafolder[0].upper() == x.upper():                             #if letter of datafolder matches drive letter, add to data_disk variable
                data_disk += float(dict_freespace[x])
            if self.logfolder[0].upper() == x.upper():                              #if letter of logfolder matches drive letter, add to log_disk variable
                log_disk += float(dict_freespace[x])



        # test prints
        # print('Space in drives in ' + self.conn['servername'])
        # print(dict_freespace)
        # print('Total data_disk available', data_disk)
        # print('Total log_disk available', log_disk)
        # print('self.datafiles_size from backup file', self.datafiles_size)
        # print('self.logfiles_size from backup file', self.logfiles_size)
        # print('self.datafiles_size_existing', self.datafiles_size_existing)
        # print('self.logfiles_size_existing', self.logfiles_size_existing)


        # this is for the case the database does not exist:
        # compare disk space with backup file disk space
        # we decide using self.datafiles_size (0 means database does not exist)
        # but we need to check if it is a single drive for both log and data
        if self.datafolder[0] != self.logfolder[0]:     # case log and data in different drives
            # print('log and data different drives')
            if self.datafiles_size_existing == 0:       # case no existing database
                # print('database does not exist, log and data on different drives')
                if (float(data_disk) > float(self.datafiles_size)) and (float(log_disk) > float(self.logfiles_size)):  # disk space > backup space requiered
                    return True
                else:
                    return False
            else:                                       # case database exists
                # print('database exists, log and data on different drives')
                if (float(data_disk) > (float(self.datafiles_size) - float(self.datafiles_size_existing))) \
                    and (float(log_disk) > (float(self.logfiles_size) - float(self.logfiles_size_existing))):
                    return True
                else:
                    return False
        else:                                         # case log and data are in same drive
            # print('log and data same drive')
            if self.datafiles_size_existing == 0:                            # no existing database
                # print('database does not exist, log and data on same drive')
                if float(data_disk) > (float(self.datafiles_size) + float(self.logfiles_size)):
                    return True
                else:
                    return False
            else:
                # print('database exists, log and data on same drive')
                if float(data_disk > (float(self.datafiles_size) + float(self.logfiles_size)) - (float(self.datafiles_size_existing) + float(self.logfiles_size_existing))):
                    return True
                else:
                    return False

    def RestoreDatabase(self):
        """
        Restores the database from given backup file to given data and log folders
        There 2 options:
        1) rename files with a timestamp added to the name
        (This is done to avoid file name collisions)
        2) use names based on database name with _Data and _Log suffixes (this is the default)
        """

        self.GetBackupInfo()

        t = ''
        if self.restore_options['dated_file_names']:
            today = str(datetime.date.today())
            t = today.replace('-', '')
        s = 'USE MASTER RESTORE ' + self.restore_options['restore_type'] + ' [' + self.currdb + '] FROM DISK =' + chr(39) + self.backupfile + chr(39) + ' WITH '
        filecount = 0
        suffix2 = ''
        for x in self.dictfiles.keys():
            if self.dictfiles[x][1] == 'D':
                suffix = 'Data'
                d = self.datafolder
            if self.dictfiles[x][1] == 'L':
                suffix = 'Log'
                d = self.logfolder
                self.logfilename = x
            file, ext = os.path.splitext(os.path.basename(self.dictfiles[x][0]))
            if filecount > 1:           # after 2 values (0 and 1) we add one to the file name
                suffix2 = str(filecount)
            file_renamed = self.currdb + '_' + suffix + suffix2 + t + ext
            s += ' MOVE ' + chr(39) + x + chr(39) + ' TO ' + chr(39) + d + '\\' + file_renamed + chr(39) + ', '
            filecount += 1

        s = s + ' NOUNLOAD, ' + self.restore_options['recovery'] + ', STATS = 10'
        if self.restore_options['replace']:
            s += ', REPLACE'

        self.sqlrestore = s
        if self.noexecute == 1:
            return []

        # Doing the actual restore here. NEW: added code to kill connections in the same execution

        s = 'SET NOCOUNT ON DECLARE @kill varchar(8000) = ' + chr(39) + chr(39) + ';'
        s += ' SELECT @kill = @kill + ' + chr(39) + 'kill ' + chr(39) + '  + CONVERT(varchar(5), spid) + ' + chr(39) + ';' + chr(39)
        s += ' FROM master..sysprocesses WHERE dbid = db_id(' + chr(39) + self.currdb + chr(39) + ')'
        s += ' select @kill; EXEC(@kill); '
        s += self.sqlrestore
        rows, fnames = [], []
        try:
            rows, fnames = SqlExecute(self.conn, s)
        except Exception as inst:
            print('Error restoring database: ', inst)
        return rows

    def BackupDatabase(self):
        if self.backup_options['backup_type'] != 'DIFFERENTIAL':
            s = 'BACKUP ' + self.backup_options['backup_type'] + ' [' + self.currdb + '] TO DISK = ' + chr(39)
            s += self.backupfile + chr(39) + ' WITH NOFORMAT, INIT, NAME = N' + chr(39)
            s += self.currdb + ' ' + self.backup_options['backup_type'] + ' Backup' + chr(39)
        else:
            s = 'BACKUP DATABASE [' + self.currdb + '] TO DISK = ' + chr(39)
            s += self.backupfile + chr(39) + ' WITH DIFFERENTIAL, NOFORMAT, INIT, NAME = N' + chr(39)
            s += self.currdb + ' Differential Backup' + chr(39)
        if self.backup_options['compression']:
            s += ' , SKIP, NOREWIND, NOUNLOAD, COMPRESSION,  STATS = 10'
        else:
            s += ' , SKIP, NOREWIND, NOUNLOAD,  STATS = 10'
        self.sqlbackup = s
        rows, fnames = [], []
        if self.noexecute == 0:
            try:
                rows, fnames = SqlExecute(self.conn, s)
            except Exception as inst:
                print('Error restoring database: ', inst)
        return rows

    # ---------------End of class SQLSMO------------------------------------------

# ===============TEST SECTION=====================================================

if __name__ == '__main__':

    print('find latest backup')
    BACKUPFOLDER = r'C:\SQL2014\BACKUPS'
    lst = GetLatestBackup(BACKUPFOLDER, '\AdventureWorks2012*.bak')

    BKFILE = lst[-1]
    print('Latest backup:')
    print(BKFILE)

    CONNECTION = {}
    SQLSERVER = r'(local)\sql2014'
    CONNECTION['servername'] = SQLSERVER
    CONNECTION['username'] = ''
    CONNECTION['password'] = ''
    CONNECTION['db'] = 'AdventureWorks2012'
    print('Connection dict:', CONNECTION)


    print('testing full backup with dated file name')
    BKFILE = r'C:\SQL2014\BACKUPS\AdventureWorks_Backup_' + DatedString() + '.BAK'
    smo = SQLSMO(CONNECTION, '', '', BKFILE)
    smo.noexecute = 0
    smo.BackupDatabase()
    print('backup script: ', smo.sqlbackup)


    print('testing log backup')
    BKFILE = r'C:\SQL2014\BACKUPS\AdventureWorks_Backup.TRN'
    smo = SQLSMO(CONNECTION, '', '', BKFILE)
    smo.noexecute = 0
    smo.backup_options['backup_type'] = 'LOG'
    smo.BackupDatabase()
    print('backup script: ', smo.sqlbackup)


    print('testing differential backup')
    BKFILE = r'C:\SQL2014\BACKUPS\AdventureWorks_Backup.DIF'
    smo = SQLSMO(CONNECTION, '', '', BKFILE)
    smo.noexecute = 0
    smo.backup_options['backup_type'] = 'DIFFERENTIAL'
    smo.BackupDatabase()
    print('backup script: ', smo.sqlbackup)


    print('testing full backup again')
    BKFILE = r'C:\SQL2014\BACKUPS\AdventureWorks_Backup.BAK'
    smo = SQLSMO(CONNECTION, '', '', BKFILE)
    smo.noexecute = 0
    smo.BackupDatabase()
    print('backup script: ', smo.sqlbackup)

    BKFILE = lst[-1]
    print('Latest backup:')
    print(BKFILE)
    DATAFOLDER = r'C:\SQL2014\DATA'
    LOGFOLDER = r'C:\SQL2014\LOG'
    SQLSERVER = r'(local)\sql2014'

    print('restoring copy of database')
    CONNECTION = {}
    CONNECTION['servername'] = SQLSERVER
    CONNECTION['username'] = ''
    CONNECTION['password'] = ''
    CONNECTION['db'] = 'AdventureWorks2012_COPY_NEW'

    print('Connection dict:', CONNECTION)

    DATAFOLDER = r'C:\SQL2014\DATA'
    LOGFOLDER = r'C:\SQL2014\LOG'

    SQLSERVER = r'(local)\sql2014'

    print('testing restores checking using Ok_to_restore')
    smo = SQLSMO(CONNECTION, DATAFOLDER, LOGFOLDER, BKFILE)

    print('-----Info on existing database----------------------------------')
    rows, fnames = smo.GetDataseInfo()
    print(smo.dictdbinfo)
    print('data size from existing db', smo.datafiles_size_existing)
    print('log size from existing db', smo.logfiles_size_existing)
    print('-----Info on existing database----------------------------------')



    go_ahead = smo.Ok_to_restore()
    if go_ahead:
        print('Ok to restore')
        print('killing connections is now part of the restore call, no need to call the function KillConnections')
        # Default is RECOVERY, put here as reminder you can change to NORECOVERY
        smo.restore_options['recovery'] = 'RECOVERY'
        print('restore options:', smo.restore_options)
        # Now we restore
        rows_restore = smo.RestoreDatabase()

        print('---------------Info on backup files from filelistonly----------------------------')
        for x in smo.dictfiles:
            print(x, smo.dictfiles[x])
        print('---------------Info on backup files from headeronly------------------------------')
        for x in smo.dictheader:
            print(x, smo.dictheader[x])

        print('data size from backup', smo.datafiles_size)
        print('log size from backup', smo.logfiles_size)
        print('rows of restore')
        print(rows_restore)
        print('Lets do some fixes: setting db to simple mode, change dbowner to sa, shrink log, back to full mode')
        s = 'USE [master] ALTER DATABASE [' + smo.currdb + '] SET RECOVERY SIMPLE WITH NO_WAIT '
        s += ' USE ' + smo.currdb + ' EXEC dbo.sp_changedbowner @loginame = ' + chr(39) + 'sa' + chr(39) + ', @map = false '
        s += ' DBCC SHRINKFILE (' + chr(39) + smo.logfilename + chr(39) + ' , 0, TRUNCATEONLY) '
        sqlfixes1 = s + 'ALTER DATABASE [' + smo.currdb + '] SET RECOVERY FULL WITH NO_WAIT '
        print('sql to apply:')
        print(sqlfixes1)
        try:
            rows, fnames = SqlExecute(smo.conn, sqlfixes1)
        except Exception as inst:
            print('Error executing database fixes: ', inst)
        for x in rows:
            print(x)
        print('resync logins')
        rows = SyncLogins(smo.conn, smo.currdb)
        for x in rows:
            print(x)
    else:
        print('Cannot restore')
    print('SQL RESTORE SCRIPT:', smo.sqlrestore)

    print('testing select query')
    conn = {}
    conn['servername'] = '(local)\sql2014'
    conn['username'] = ''
    conn['password'] = ''


    #testing select query
    s = 'set nocount on select top 10 BusinessEntityID, FirstName, MiddleName, \
        LastName, ModifiedDate from AdventureWorks2012.Person.Person'
    rows, fnames = SqlExecute(conn, s)
    print(fnames)
    for x in rows:
        print(x)
