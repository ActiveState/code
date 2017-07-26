# dbmove.py - M.Keranen (mksql@yahoo.com) [11/24/03]
# ----------------------------------------------------------------------------------------
# Automate the process of moving databases from one SQL Server to another.
# Assumes current login has administrator access to $ shares on source and target servers.
# ----------------------------------------------------------------------------------------
# Usage: python dbmove.py source_server, sa_password, target_server, sa_password, dbname, db_target_path, log_target_path, connect_string_path

import os, string, sys, time, win32file, win32com.client, win32net
from _winreg import *

def clusterdetect(server):
# Detect the presence of a clustered virtual instance, and return the proper
# SQL Server network name of the server
     
     try: rReg = ConnectRegistry(target,HKEY_LOCAL_MACHINE)
     except: 
          print "Unable to connect to registry on server %s" % (server)
          sys.exit()
     else:
          key = "SOFTWARE\\Microsoft\\Microsoft SQL Server\\" + server + "\\Cluster"
          try: rKey = OpenKey(rReg, key)
          except: clustername = server
          else:
               try: clustername = QueryValueEx(rKey,"ClusterName")[0]
               except: 
                    clustername = string.lower(server)
                    print "* No ClusterName key defined in registry on server %s" % (server)
               else: 
                    clustername = string.lower("%s\\%s" % (server,clustername))
                    print "Cluster detected: %s" % (clustername)
                    CloseKey(rKey)
          CloseKey(rReg)

          return clustername


def getdefaultdirs(server):
# Retrieve default database and log directories from target server
     
     try: rReg = ConnectRegistry(target,HKEY_LOCAL_MACHINE)
     except: 
          print "Unable to connect to registry on server %s" % (server)
          sys.exit()
     else:
          try: rKey = OpenKey(rReg, r"SOFTWARE\Microsoft\MSSQLServer\MSSQLServer")
          except: 
               print "Unable to open registry key on server %s" % (server)
               sys.exit()
          else:
               dbdir = [None,None]
              
               try: dbdir[0] = QueryValueEx(rKey,"DefaultData")[0]
               except: print " * No DefaultData key defined in target registry"
                    
               try: dbdir[1] = QueryValueEx(rKey,"DefaultLog")[0]
               except: print " * No Defaultlog key defined in target registry"
               CloseKey(rKey)
          CloseKey(rReg)

          return dbdir
     

def getdbfileinfo(server, sap, dbname):
#Query server for source files. Returns a list of all files belonging to the database.

     adoConn = win32com.client.Dispatch('ADODB.Connection')
     connect = "Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=%s;User ID=sa;Password=%s" % (server, dbname, sap)
     try: adoConn.Open(connect)
     except: 
          print " ! getdbfileinfo: Unable to connect to %s.%s" % (source,dbname)
          return False
     
     sql = "SELECT filename FROM sysfiles ORDER BY fileid"
     try: rs = adoConn.Execute(sql)
     except: 
          print " ! getdbfileinfo: Unable to query file info for %s.%s" % (source,dbname)
          print " ->%s" % (sql)
          return False
     
     srcfiles=[]
     while not rs[0].EOF:
          srcfiles.append(string.strip(rs[0].Fields(0).Value))
          rs[0].MoveNext()
     
     rs[0].Close()
     adoConn.Close()
     adoConn = None   
     
     return srcfiles
        
    
def detachdb(server, sap, dbname):

     print "   DETACH: %s.%s" % (server,dbname)
     
     adoConn = win32com.client.Dispatch('ADODB.Connection')
     connect = "Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=master;User ID=sa;Password=%s" % (server, sap)
     try: adoConn.Open(connect)
     except: 
          print " ! detachdb: Unable to connect to %s.%s" % (server,dbname)
          return False
     
     #sql = "EXEC sp_dboption '%s', 'trunc. log on chkpt.', 'TRUE'" % (dbname)
     #try: adoConn.Execute(sql)
     #except: 
     #     print " ! detachdb: Unable to set truncate dboption for %s.%s" % (server,dbname)
     #     print " ->%s" % (sql)
     #     return False

     # Wait for user connections to clear from database
     sql = "select sysprocesses.hostname from sysprocesses,sysdatabases where sysprocesses.dbid = sysdatabases.dbid and name = '%s'" % (dbname)
     try: rs = adoConn.Execute(sql)
     except: 
          print " ! detachdb: Unable to query sysprocesses on %s" % (server)
          print " ->%s" % (sql)
          return False
     
     if not rs[0].EOF: 
          print("      Database in use on " + (string.strip(rs[0].Fields(0).Value))),
          while not rs[0].EOF:
               rs = adoConn.Execute(sql)
               print("."),
               time.sleep(5)
          print " "

     sql = "CHECKPOINT"
     try: adoConn.Execute(sql)
     except: 
          print " ! detachdb: Unable to checkpoint %s.%s" % (server,dbname)
          print " ->%s" % (sql)
          return False

     sql = "EXEC sp_detach_db @dbname = %s" % (dbname)
     try: adoConn.Execute(sql)
     except: 
          print " ! detachdb: Unable to execute detach for %s.%s" % (server,dbname)
          print " ->%s" % (sql)
          return False
     
     adoConn.Close()
     adoConn = None
     
     return True


def copydb(source,srcpath,target,tgtpath):

     print "   COPY:  (%s)%s -> (%s)%s" % (source,srcpath,target,tgtpath)
          
     srcfile = '\\\\'+source+'\\'+srcpath[0]+"$"+srcpath[2:]
     tgtfile = '\\\\'+target+'\\'+tgtpath[0]+"$"+tgtpath[2:]+'\\'+srcpath[srcpath.rfind('\\')+1:]

     try: win32file.CopyFile(srcfile,tgtfile,0)
     except:
          print " ! Unable to copy %s -> %s" % (srcfile,tgtfile)
          return False
     
     return True
     

def attachsinglefiledb(server, sap, dbname, mdfile):
# Single file attach

     print "   ATTACH SINGLE: %s.%s" % (server,dbname)
     
     adoConn = win32com.client.Dispatch('ADODB.Connection')
     connect = "Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=master;User ID=sa;Password=%s" % (server, sap)
     try: adoConn.Open(connect)
     except: 
          print " ! attachsinglefiledb: Unable to connect to %s" % (server)
          return False
     
     sql = "EXEC sp_attach_single_file_db @dbname = '%s', @physname = '%s'" % (dbname,mdfile)
     try: adoConn.Execute(sql)
     except: 
          print " ! attachsinglefiledb: Unable to execute attach for %s.%s" % (server,dbname)
          print " ->%s" % (sql)
          return False
     
     adoConn.Close()
     adoConn = None
     
     return True


def attachdb(server, sap, dbname, mdfile, ldfile):
# Data and Log file attach

     print "   ATTACH: %s.%s" % (server,dbname)
     
     adoConn = win32com.client.Dispatch('ADODB.Connection')
     connect = "Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=master;User ID=sa;Password=%s" % (server, sap)
     try: adoConn.Open(connect)
     except: 
          print " ! attachdb: Unable to connect to %s" % (server)
          return False
     
     sql = "EXEC sp_attach_db @dbname = '%s', @filename1 = '%s', @filename2 = '%s'" % (dbname,mdfile,ldfile)
     try: adoConn.Execute(sql)
     except: 
          print " ! attachdb: Unable to execute attach for %s.%s" % (server,dbname)
          print " ->%s" % (sql)
          return False
     
     adoConn.Close()
     adoConn = None
     
     return True
     

def loginfix(server,sap,dbname,username):
     
     adoConn = win32com.client.Dispatch('ADODB.Connection')
     connect = "Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=%s;User ID=sa;Password=%s" % (server, dbname, sap)
     try: adoConn.Open(connect)
     except: 
          print " ! loginfix: Unable to connect to %s.%s" % (server,dbname)
          return False

     sql = 'exec sp_change_users_login "UPDATE_ONE","%s","%s"' % (username,username)

     try: adoConn.Execute(sql)
     except: 
          print " ! loginfix: Unable to execute sp_login_fix for %s.%s" % (server,dbname)
          print " ->%s" % (sql)
          return False
     
     adoConn.Close()
     adoConn = None

     return True
          

def fgrepcs(oldsrv, olddb, newsrv, connectpath):
# Create a new verions of the file, search each input file line the file for server & db names, 
#  replace them, and write to a new file.
   

     for file in connectpath:
     
          print "   CONNECTION STRING: %s" % (file)   
        
          try: fp = open(file, 'r')
          except:
               print " ! Unable to open connection string file"
               return False
               
          try: fpr = open(file+'.new','w')
          except: 
               print" ! Unable to create new connection string file"
               return False
          
          for line in fp.readlines():
               line = line.lower()
               line = line.replace(oldsrv.lower(),newsrv.lower())
               fpr.writelines(line)
     
          fpr.close()
          fp.close()
     
          oldfile = file+'.old'
          i=0
          while os.path.exists(oldfile):
               i=i+1
               oldfile = file + ('.old%s') % i
          
          try: win32file.MoveFile(file,oldfile)
          except:
               print " ! Unable to rename old file"
               return False
               
          try: win32file.MoveFile(file+'.new',file)
          except:
               print " ! Unable to rename new file"
               return False
     
     return True
     

if __name__ == '__main__':

     print ""
     
     if len(sys.argv)>1: param = sys.argv[1].split(',')
     
     if len(sys.argv)<2 or len(param)<7:
          print "\Usage: source_server, sa_password, target_server, [sa_password], dbname,"
          print   "       [db_target_path], [log_target_path] | [*], [connect_file_path] | [*]\n"
          print   "       log_target_path = * : Do not copy transaction log file (SQL recreates)"
          print   "       connect_file_path = * : Do not update connection string file"
          sys.exit()

     source=string.lower(param[0])
     srcsa=string.lower(param[1])
     target=string.lower(param[2])
     tgtsa=string.lower(param[3])
     if tgtsa == '': tgtsa = srcsa
     dbname=string.lower(param[4])
     tgtpath1=string.lower(param[5])
     tgtpath2=string.lower(param[6])
     connectpath=string.lower(param[7])

     #If no connection string path is supplied, collect file paths from connect file catalog
     if connectpath == '':
          connectpath = []
          for line in open('connects.txt','r').readlines():
               line = string.lower(line)
               conninfo = string.split(string.strip(line),',')
               if conninfo[1]==source and conninfo[2]==dbname: connectpath.append(conninfo[3])
               
     sourcesql = clusterdetect(source)
     targetsql = clusterdetect(target)

     if (tgtpath1=='') or (tgtpath2==''):
          dbdirs = getdefaultdirs(target)
          if tgtpath1=='': tgtpath1 = dbdirs[0]
          if tgtpath2=='': tgtpath2 = dbdirs[1]

     if tgtpath1[-1]=='\\': tgtpath1=tgtpath1[:-1]
     if tgtpath2[-1]=='\\': tgtpath2=tgtpath2[:-1]
      

     print "\n%s.%s" % (source,dbname)
     
     failsafe = False
     srcfiles=getdbfileinfo(source,srcsa,dbname)
     if srcfiles: 
          if detachdb(sourcesql,srcsa,dbname):
               failsafe = True
               if tgtpath2 == '*':
                    if copydb(source,srcfiles[0],target,tgtpath1):
                         tgtpath1=tgtpath1+'\\'+string.split(string.strip(srcfiles[0]),'\\')[-1]
                         if attachsinglefiledb(targetsql, tgtsa, dbname, tgtpath1):
                              loginfix(targetsql,tgtsa, dbname, "aspuser")
                              if connectpath=='*': failsafe = False
                              else:failsafe = not fgrepcs(sourcesql, dbname, targetsql, connectpath)

               else:
                    if copydb(source,srcfiles[0],target,tgtpath1) and copydb(source,srcfiles[1],target,tgtpath2):
                         tgtpath1=tgtpath1+'\\'+string.split(string.strip(srcfiles[0]),'\\')[-1]
                         tgtpath2=tgtpath2+'\\'+string.split(string.strip(srcfiles[1]),'\\')[-1]
                         if attachdb(targetsql, tgtsa, dbname, tgtpath1, tgtpath2):
                              loginfix(targetsql,tgtsa, dbname, "aspuser")
                              if connectpath=='*': failsafe = False
                              else:failsafe = not fgrepcs(sourcesql, dbname, targetsql, connectpath)
     
     if failsafe: attachdb(sourcesql, srcsa, dbname, srcfiles[0],srcfiles[1])
     
     
print "\n*** Done ***"
