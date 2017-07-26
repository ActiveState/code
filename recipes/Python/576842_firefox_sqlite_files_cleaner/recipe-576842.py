# -*- coding: utf-8 -*- 

import os, sqlite3
"""Walks through the all the Firefox profiles in current user account and cleans all
*.sqlite files with "vacuum". It makes firefox faster then often. Should work on Linux, too,
when properly changed constants."""

# -------------- constants -----------------------------------------

systemEncoding="mbcs"

profileUser= unicode(os.environ["USERPROFILE"], systemEncoding)
profileApp = unicode(os.environ["APPDATA"], systemEncoding) + ur"\Mozilla\Firefox\Profiles"


# -------------- functions -----------------------------------------

def searchProfil(profileApp):
    "all firefox profiles"
    for profile in os.listdir(profileApp):
        profileFull=os.path.join(profileApp, profile)
        searchSqlite(profileFull)
        

def searchSqlite(profile):
    "all sqlite file in each firefox profile"
    sq=[os.path.join(profile,s) for s in os.listdir(profile) if s.endswith(".sqlite")]
    print "\n..."+profile[len(profileUser):]
    for s in  sq:
        dirName, fileName=os.path.split(s)
        conn = sqlite3.connect(s)
        oldSize=os.path.getsize(s)
        print fileName+":",
        try: 
            c=conn.cursor()
            c.execute("VACUUM")  # this is the thing
            c.close()
            print "done.",
            print "%.1f%%" % (os.path.getsize(s)*1.0/oldSize*100)
            
        except:
            print "error."

# ----------------- main -------------------------------------------     

if __name__=="__main__":

    if os.path.isdir(profileApp):
        searchProfil(profileApp)
    else:
        print "Not exists:", profileApp
