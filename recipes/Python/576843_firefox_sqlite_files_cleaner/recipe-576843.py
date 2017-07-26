#!/usr/bin/env python

import os, sqlite3                                                             

# -------------- constants -----------------------------------------

profilAppMain=os.path.join(os.environ["HOME"], ".mozilla/firefox")
profilUser= os.environ["USER"]                                    
profilApp = os.path.join(profilUser,profilAppMain)                

# -------------- functions -----------------------------------------

def searchProfil(profilApp):
    "all firefox profiles"  
    for profil in os.listdir(profilApp):
        profilFull=os.path.join(profilApp, profil)
        searchSqlite(profilFull)                  
                                                  

def searchSqlite(profil):
    "all sqlite file in each firefox profile"
                                             
    if not os.path.isdir(profil):            
        return

    sq=[os.path.join(profil,s) for s in os.listdir(profil) if s.endswith(".sqlite")]
    print "\n..."+profil[len(profilUser):]
    for s in  sq:
        dirName, fileName=os.path.split(s)
        conn = sqlite3.connect(s)
        old=os.path.getsize(s)
        print fileName+":",
        try:
            c=conn.cursor()
            c.execute("VACUUM")  # this is the thing
            c.close()
            print "done.",
            new=os.path.getsize(s)
            print new*1.0/old*100,"%"
        except:
            print "error."


# ----------------- main -------------------------------------------

if __name__=="__main__":

    if os.path.isdir(profilApp):
        searchProfil(profilApp)
    else:
        print "Not exist:", profilApp
