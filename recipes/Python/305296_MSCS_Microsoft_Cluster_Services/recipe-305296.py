# clusterdetect() - M.Keranen (mksql@yahoo.com) [11/24/2003]
# ----------------------------------------------------------
# Detect the presence of a clustered MS SQL Server virtual instance,
# and return the proper SQL Server network name of the server

from _winreg import *

def clusterdetect(server):
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
