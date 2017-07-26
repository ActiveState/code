def backupSave(fileName, prefix='', suffix='bk', count=5):
     ''' backupSave: backup a file to up to number of versions defined by count.
    
     Let fileName = 'c:/tmp/myfile.txt'
         prefix   = 'x_'
         suffix   = 'BAK'
         count    = 5 
    
     This function will check if 
    
        x_myfile.txt.BAKi

    exists in the same folder, where 1<=i<=count
    
    If found, save it to x_myfile.txt.BAKi+1
    
     version: 04b43
     module : panTools    
     author : Runsun Pan
     '''
     import os, shutil
     folder, fileName = os.path.split(fileName)
     if not folder.strip(): folder = '.'
     files = os.listdir(folder)
     
     for i in range(count):
        j = count-i-1
        fn  = prefix + fileName  + '.' + suffix + str(j)
        if j == 0: fn = fileName
        nfn = prefix + fileName +  '.' + suffix + str(j+1)
        fn = os.path.join(folder, fn)
        if os.path.exists(fn):
           shutil.copy(fn, nfn) 
