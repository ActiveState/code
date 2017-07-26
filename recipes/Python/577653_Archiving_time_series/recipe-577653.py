#WI Rapids DNR Fire Situations Unit backup script
#To be executed by double-clicking the file in the incident folder on Buffy
#(Buffy is a TeraStation portable file server)
#Will endlessly repeat, kill it by closing the window
#Tyler Grosshuesch - tyler.grosshuesch@co.adams.wi.us
#2011-04-13

import time, os, fnmatch, shutil

#Endless loop
while 1:
    #set up timestamp
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)

    #buffy backup directory with timestamp
    bu_dir = os.path.join(r'.\Folder_Backup', timestamp)

    #set up local backup directory
    proj_dir = os.getcwd()
    local_dir = os.path.join(r'C:\Share', os.path.basename(proj_dir))

    #set up mkdir Folder_Backup\timestamp command
    mkdir_cmd = r'mkdir ' + bu_dir
    #execute mkdir Folder_Backup\timestamp
    os.system(mkdir_cmd)

    #Copy files to Folder_Backup\timestamp directory on Buffy
    for d in os.listdir(proj_dir):
        if not fnmatch.fnmatch(d, '*Folder_Backup*'): #don't backup Folder_Backup
            #backup directories and subdirectories
            if os.path.isdir(d):
                print 'backing up ' + d
                shutil.copytree(d, os.path.join(bu_dir, d))
            #backup loose files in the project directory
            else:
                print 'backing up ' + d
                shutil.copy(d, os.path.join(bu_dir, d))

    #copy shell command - entire project folder to ranger mapper's local
    copy_c_cmd = r'xcopy . ' + local_dir + ' /D /E /Y /C'
    
    #execute shell commands
    mkdir_c_cmd = 'mkdir ' + local_dir
    if not os.path.exists(local_dir):
        os.system(mkdir_c_cmd)
    os.system(copy_c_cmd)

    #timer - repeats every 10 min
    print 'waiting to copy backup files...'    
    time.sleep(600) #units = seconds (10min = 600s, 30min = 1800s)
