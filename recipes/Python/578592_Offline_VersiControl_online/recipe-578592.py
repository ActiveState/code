# Basic Version Control
# Author: commentator8

# Takes the given file and tag as argument, 
# and saves a copy to run dir/VC with incremental number and tag
# Input: c:/dir1/dir2/file.py "tag"
# Saved Output: c:/dir1/dir2/VC/file_0001_tag.py
# Can add extra argument as follows -v to increment first number of series.

# files example (notepad++ F5): python c:\users\user\dropbox\txt\versionControl\versioner.py "$(FULL_CURRENT_PATH)" "Threading Working" -v
# folder example: python c:\users\user\dropbox\txt\versionControl\versioner.py "C:\Users\user\Dropbox\txt\Downloader" "Initial backup"

import os, sys
import time
import shutil
import zipfile

def list_dir(path, zip):
    files_to_zip = []
    for root, dirs, files in os.walk(path):
        if root.split('\\')[-1] in ['index']:
            continue
            
        for file in files:
            if file.split('.')[-1] != 'zip' or root.split('\\')[-1] != 'VC':
                files_to_zip.append(os.path.join(root, file))
            
    return files_to_zip

version_up = False
if '-v' in sys.argv:
    version_up = True
    sys.argv.remove('-v')

if len(sys.argv) != 3:  
    print 'Wrong number of arguments passed in. Please try again.'
    print sys.argv
    time.sleep(4)
    exit()    

file = sys.argv[1].replace('\'"', '')
file_tag = sys.argv[2].replace('\'"', '')

file_name = os.path.split(file)[-1].split('.')[0]
file_ext = os.path.split(file)[-1].split('.')[-1]

if file_name == '' or os.path.isdir(file):
    folder_name = os.path.split(file.strip('\\'))[-1]
    if file[-1] not in ['\\', '/']:
        file += '\\'
    folder = file

if '/' not in file and '\\' not in file:
    print 'Check if this is a file passed in'
    time.sleep(4)
    exit()

vc_path = os.path.split(file)[0]  + '/VC/'

highest_ver = 0
for dirname, dirnames, filenames in os.walk(vc_path):
    for f in filenames:
        file_name_vc = f.partition('_')[0]
        number = (f.partition('_')[-1]).partition('_')[0]
        tag = ((f.partition('_')[-1]).partition('_')[-1]).partition('_')[0]
        
        # allow for multiple backed up files in single dir
        if file_name:
            if file_name_vc != file_name:
                continue
        elif file_name_vc != folder_name:
            continue
        if number > highest_ver:
            highest_ver = int(number)
            

    
series_number = (str(highest_ver + 1).zfill(4))  
            
if version_up:
    series_number = str(int(series_number[0]) + 1) + '001'

if os.path.isdir(file):
    print 'Copy folder:\n"%s"\n\nto destination:\n"%s"\n\nwith version:\n"%s"\n\nand tag:\n"%s"\n' % (folder_name, vc_path, series_number, file_tag)
else:    
    print 'Copy file:\n"%s"\n\nto destination:\n"%s"\n\nwith version:\n"%s"\n\nand tag:\n"%s"\n' % (file_name, vc_path, series_number, file_tag)

answer = raw_input('\nDo you want to continue?\n')

if answer.lower() in ['y', 'yes']:
    pass
else:
    exit()

if not os.path.exists(vc_path):
    os.makedirs(vc_path)
    
if os.path.isdir(file):
    new_file = vc_path + folder_name + '_' + series_number + "_" + file_tag + '.zip'
    zip = zipfile.ZipFile(new_file, 'w')
    files_to_zip = list_dir(folder, zip)

    for i in files_to_zip:
        zip.write(i, arcname = i.replace(folder.rpartition(folder_name)[0], ''))  
             
    zip.close()
else:
    new_file = vc_path + file_name + '_' + series_number + "_" + file_tag + '.' + file_ext     
    shutil.copyfile(file, new_file)

print     
print 'All Done'      
time.sleep(2)
