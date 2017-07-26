'''
BACK UP AND ARCHIVING TOOL by MoHaWke #B0)
http://www.digitaldarknet.net/
Date: December 2004
Install python 2.3 from http://www.python.org
Setup source and target paths, retention dates.
Setup to run in Windows Task Scheduler.
'''
import zlib, zipfile, os, time, sys
import win32api, win32file
#=================================================

#/////////////////////////////////////////////////
# FUNCTION; saves copy of original source zips
#/////////////////////////////////////////////////
def remote_Save(target, remote_target):
    bFailIfExists = 0
    for backups in os.listdir(target):
        if backups[-3:].lower() == 'zip':
            win32file.CopyFile(target+'\\'+backups, remote_target+'\\'+backups, bFailIfExists)
            
#/////////////////////////////////////////////////
# FUNCTION; Deletes remote and local zips based
#on user defined retention. 
#/////////////////////////////////////////////////   
def clean_dir(target, remote_target, target_count, remote_count):
    # Clean main backup directory.
    dict_trg = {}; flist=[]
    target_dir = os.listdir(target)
    for x in target_dir:
        timestamp=int(x.split('_')[0])
        filename=x.split('_')[-1]
        if not dict_trg.has_key(filename):
            dict_trg[filename]=[]
        dict_trg[filename].append(timestamp)
        
    for arch, flist in dict_trg.items():
        if len(flist)>target_count:
            flist.sort()
            sort_list=str(flist[0])
            os.remove(target+'/'+sort_list+'_'+arch)
       
    # Clean up remote location.
    dict_rmt = {}; flist=[]
    if remote_target:
        remote_dir = os.listdir(remote_target)
        for x in remote_dir:
            timestamp=x.split('_')[0]
            filename=x.split('_')[-1]
            if not dict_rmt.has_key(filename):
                dict_rmt[filename]=[]
            dict_rmt[filename].append(timestamp)
            
    for arch, flist in dict_rmt.items():
        if len(flist)>remote_count:
            flist.sort()
            sort_list=str(flist[0])
            os.remove(remote_target+'/'+sort_list+'_'+arch)

#/////////////////////////////////////////////////
# FUNCTION; Recusive directory zipping.
#/////////////////////////////////////////////////
def archive_dir(source, arcname, target, arc_time):
    # Set the filename and destination.
    arcname  = str(arc_time)+'_'+arcname+'.zip'  # Archive filename
    target   = str(target+'/'+arcname)           # Path to storage...
    
    dirs = [str(source)] # Set initial "root" directories to pop.
    zipObj = zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED)
    
    try:
        while dirs:
            # Loop through and get all sub dirs and files.
            dir_list=dirs.pop(0) # pop next dir.
            try:
                for items in os.listdir(dir_list+'/'):
                    if os.path.isdir(dir_list+'/'+items):
                        # Collect sub dirs for pop.
                        dirs+=[dir_list+'/'+items]
                    elif os.path.isfile(dir_list+'/'+items):
                        # Ignor the archive file if in the dir structure.
                        if items.lower() == arcname: continue
                        if items.lower()[:3] == 'ini': continue #task directory filter.
                        # Write to the zip.
                        zipObj.write(str(dir_list+'/'+items),None,None)
            except:
                pass # Ignor non-accessable directories!

        zipObj.close()
        return 1 # Success...
    
    except Exception, error:
        return error # Backup failed...
    
#//////////////////////////////////////////////////////>
# CONFIGURATION AND PATH SETUPS
#//////////////////////////////////////////////////////>

# SPECIFY SOURCE PATHS; add as many as you like.
# Don't forget to add these to the SOURCE_PATH list below.
path_a   = 'c:/somedir'             # Back up this directory
path_b   = 'c:/someotherdir'        # Back up that directory
path_c   = ''                       # empty...
path_d   = ''                       # empty...
all_drv  = 'c:/'                    # I wouldn't do this! 

# SPECIFY TARGET PATHS.
target = 'c:/backup'                   # save to path local.
remote_target = r'\\server\c$\backup'  # save to path remote; can be a mapped share or local store also.

# CLEAN UP SETTINGS: Removes oldest archive.
target_count = 7  # Days to keep
remote_count = 30 # Days to keep
clean_bu = 1      # 0 turns off cleaning.

# LOG FILE PATH
logpath=os.getcwd()
logfile = logpath+'\\archive_log.log'

# TURN ON OR OFF ? ****
all_drv  = 'off'                                       
#path_a = 'off'
#path_b = 'off'
#path_c = 'off'
#path_d = 'off'
remote = 1   # 0 - turn off remote copy/ 1 = on.

# SOURCE_PATH :: ADD NEW PATHS HERE...
source_paths = [path_a, path_b, path_c, path_d, all_drv]

#//////////////////////////////////////////////////////>
#YOU SHOULDN'T NEED TO CHANGE ANYTHING BELOW THIS LINE
#//////////////////////////////////////////////////////>

tm_stamp = time.ctime()
arc_time = int(time.time())
myname  = win32api.GetComputerName()

# Start Backups...
#========================================>
#========================================> 
# make sure the directories exist.
if not os.path.exists(target): os.mkdir(target)
if remote_target:
    if not os.path.exists(remote_target):
        os.mkdir(remote_target)  

# Run backup.
for source in source_paths:
    if os.path.exists(source):
        arcname = source.split('/')[-1] #strip the sub path for archive filename. 
        try:
            status = archive_dir(source, arcname, target, arc_time)

            # Report and log errors.
            if status != 1:
                open(logfile,'a').write('\n'+tm_stamp+':: '+myname+':: path='+source+'\n Archive unsuccessful - status returned 0') # log
                sys.exit(0) #Back up failed, no since in running the rest.
            open(logfile,'a').write('\n'+tm_stamp+': '+myname+':: '+source+' Successfully backed up.') # log
        except Exception, error:
            open(logfile,'a').write('\n'+tm_stamp+': '+myname+':: path='+source+'\n'+' Error:: '+str(error)) # log
            
#========================================>
# Save remote.
#========================================>
if not remote == 0:
    try:
        remote_Save(target, remote_target)
    except Exception, error:
        open(logfile,'a').write('\n'+tm_stamp+': Remote backup failed:: '+str(error))
        
#========================================>
# Clean up.
#========================================> 
if not clean_bu == 0:
    try:
        clean_dir(target, remote_target, target_count, remote_count)
    except Exception, error:
        open(logfile,'a').write('\n'+tm_stamp+': Clean up failed:: '+str(error))
