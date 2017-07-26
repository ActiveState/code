'''
Created on Jun 25, 2009
this script reads from a txt file having folder names , where each folder name is a  new line
and take owner ship of the folder , then deletes the folder with all its sub directories and files
@author: Mohamed Garrana
'''
import os
fv=open("folders.txt","r")
for line in fv:
    folder=line.strip()
    print folder
    takeown="takeown /f %s /r /d y" %(folder,)
    deletefolder="rd /s /q %s" %(folder,)
    try:
        tk=os.popen(takeown)
        dl=os.popen(deletefolder)
    except:
        pass
