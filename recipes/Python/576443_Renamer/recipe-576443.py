#!       /usr/bin/python
#        -*- coding: utf-8 -*-
#        Credits to Adolfo González Blázquez <code@infinicode.org>, the author of pyRenamer , as I copied some code from it
#        Dependencies - zenity

import os
import re
import sys
import time

choice      = ""
pattern     = ""
replace     = ""
replaceWith = ""
prefix      = ""
suffix      = ""
count       = 1

def choiceDialog():
        
        global choice,pattern,replace,replaceWith,prefix,suffix
        
        #Main DialogBox
        choice = os.popen('zenity --list --title "Renamer"\
                           --radiolist --column " " --column "Choose One"\
                           FALSE "Patternize" FALSE "Substitute" FALSE "Misc" FALSE "Undo Last Operation ( INSIDE THIS FOLDER )"').read().split('\n')[0]
                           
        #SubDialogBoxs
        if choice == "Patternize":
                pattern = os.popen('zenity --title "Renamer" --entry --text "For more infomation on patterns, read readme.txt.\nEnter the pattern:"').read().split('\n')[0]
    
        
        elif choice == "Substitute":
                choice = os.popen('zenity --list --title "Renamer"\
                           --radiolist --column " " --column "Choose One"\
                           FALSE "SPACE to UNDERSCORE" FALSE "UNDERSCORE to SPACE" FALSE "DASH to SPACE" FALSE "SPACE to DASH" \
                           FALSE "Replace Manually"').read().split('\n')[0]
                if choice == "Replace Manually":
                        replace = os.popen('zenity --title "Renamer" --entry --text "Enter the word (phrase) you want to replace"').read().split('\n')[0]
                        replaceWith = os.popen('zenity --title "Renamer" --entry --text "Replace that word With ?"').read().split('\n')[0]
    
        elif choice == "Misc":
                choice = os.popen('zenity --list --title "Renamer"\
                           --radiolist --column " " --column "Choose One"\
                           FALSE "ALL CAPITAL" FALSE "all lower" FALSE "First letter uppercase" FALSE "First Letter Uppercase In Each Word"\
                           FALSE "Add a Prefix" FALSE "Add a Suffix"').read().split('\n')[0]
                if choice == "Add a Prefix":
                        prefix = os.popen('zenity --title "Renamer" --entry --text "Enter the prefix:"').read().split('\n')[0]
                elif choice == "Add a Suffix":
                        suffix = os.popen('zenity --title "Renamer" --entry --text "Enter the suffix:"').read().split('\n')[0]
        
        elif choice == "Undo Last Operation in this Folder":
                #Undo
                undo()
        
        else:
                raise SystemExit
        
def getNewName(oldname,path,first):
    
    global prefix,suffix,replace,count,replaceWith,pattern
    
    if choice   == "SPACE to UNDERSCORE":
            newname = oldname.replace(' ', '_')
    
    elif choice == "UNDERSCORE to SPACE":
            newname = oldname.replace('_',' ')
    
    elif choice == "DASH to SPACE":
            newname = oldname.replace('-',' ')
    
    elif choice == "SPACE to DASH":
            newname = oldname.replace(' ','-')
     
    elif choice == "Replace Manually":
            newname = oldname.replace(replace,replaceWith)
               
    elif choice == "ALL CAPITAL":
            newname = oldname.upper()
    
    elif choice == "all lower":
            newname = oldname.lower()
    
    elif choice  == "First letter uppercase":
            newname = oldname.capitalize()
    
    elif choice == "First Letter Uppercase In Each Word":
            newname = oldname.title()
    
    elif choice == "Add a Prefix":
            newname = prefix + oldname
    
    elif choice == "Add a Suffix":        
        #Place suffix before the extension if it got ...
        if oldname.find('.') != -1:
            newname = oldname.split('.')[0] + suffix  + '.' + oldname.split('.')[1]
        else:
            newname = oldname + suffix
            
    elif choice == "Patternize":
            
            newname = pattern

            #for number substiution
            c = re.compile(r'(\{num\d*\}|(\{num\d*\+\d*\}))')
            if c.search(newname):
                tmp = c.search(newname).group()
                
                #if it is a directory just set count 0 and pass
                if os.path.isdir(path) and first == 1:
                   newname = c.sub("",newname)
                   count = 1              
                #if {num3}
                elif len(tmp)== 6:
                    substitute = str(count).zfill(int(tmp[4]))
                    newname = c.sub(substitute, newname)
                    count = count + 1
                #if {num3+3}
                elif len(tmp) > 7:
                    substitute = str(count+int(tmp[6:(len(tmp)-1)])).zfill(int(tmp[4]))
                    newname    = c.sub(substitute, newname)
                    count = count + 1
                else:
                    pass
                    
            #replace {dir} with the parent dir name
            dir = os.path.dirname(path)
            dir = os.path.basename(dir)
            newname = newname.replace('{dir}', dir)
            
            #replace {orig} with the  original name
            newname = newname.replace('{orig}',oldname)   
            
            #Some Time/Date Replacement
            newname = newname.replace('{date}', time.strftime("%d%b%Y", time.localtime()))
            newname = newname.replace('{year}', time.strftime("%Y", time.localtime()))
            newname = newname.replace('{month}', time.strftime("%m", time.localtime()))
            newname = newname.replace('{monthname}', time.strftime("%B", time.localtime()))
            newname = newname.replace('{monthsimp}', time.strftime("%b", time.localtime()))
            newname = newname.replace('{day}', time.strftime("%d", time.localtime()))
            newname = newname.replace('{dayname}', time.strftime("%A", time.localtime()))
            newname = newname.replace('{daysimp}', time.strftime("%a", time.localtime()))       
  
    else:
        raise SystemExit
    return newname 

def rename(path,oldpath,first):
    oldname = os.path.split(path)[1]
    newname = getNewName(oldname,path,first)
    newpath = os.path.join(os.path.split(path)[0],newname)
    if first == 1:
        undolog.write('%s Converted To %s\n' %(oldpath,newpath))
    else:
        undolog.write('%s Converted To %s\n' %(os.path.join(oldpath,oldname),newpath))
    os.rename(path,newpath)
    #print "Replacing %s with %s" %(path,newpath)        For Debugging
    if os.path.isdir(newpath):
            #if the choice is Patternize, skip the subfolers
            if choice == "Patternize" and first != 1:
                pass
            else:
                if first != 1:
                    oldpath = os.path.join(oldpath,oldname)
                for name in os.listdir(newpath):
                    rename(os.path.join(newpath,name),oldpath,0)
                
def undo():
    log = open('.Renamer.log','r')
    for line in log:
        oldpath, newpath = line.split('\n')[0].split(' Converted To ')
        os.rename(os.path.join(os.path.dirname(oldpath),os.path.basename(newpath)),oldpath)
    log.close()    
    raise SystemExit

choiceDialog()
undolog = open('.Renamer.log','w')                  
for i in sys.argv[1:]:
    dirs.append(i)
for dir in dirs:
    oldpath = dir
    rename(dir,oldpath,1)
undolog.close()
