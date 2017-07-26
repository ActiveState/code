'****************************************************'
'Created by C. Nichols #B0)~                         '
'E-mail: oldnich@digitaldarknet.net                  '
'Website: www.digitaldarknet.net                     '
'Created: 10/25/2002                                 '
'Version: 0.1.4                                      '
'Desc: Slither for Micro$oft Windoze                 '
'Searches your hard drive for all files specified    '
'and generates an HTML web page list of the          '
'files found and links to the file itself.           '
'****************************************************'
'                                                    '
'                        #                           '
'                       0 0                          '
'~~~~~~~~~~~~~~~~~uuu~~~~U~~~~uuu~~~~~~~~~~~~~~~~~~~~'
"!!!!!!!!!!!!HERE'S LOOKING AT YOU KID!!!!!!!!!!!!!!!"
'****************************************************'
# Libs ----------------------------------------------
import sys,os,string,time
#Globals---------------------------------------------
Search_path = ''
Report_path = ''
File_type = ''
#----------------------------------------------------

def htmlGen(path, rpath):
    dirs = [path]
    F_path = rpath
    dir_list=[] 
    file_list=[]
    fCount=0
    print 'Building list, please wait...'
    while dirs:
        dir_list=dirs.pop(0)
        try:
            for items in os.listdir(dir_list+'\\'):
                if os.path.isdir(dir_list+'\\'+items):
                    dirs+=[dir_list+'\\'+items]
                elif os.path.isfile(dir_list+'\\'+items):
                    if items[-4:].lower()=='.'+File_type:
                        file_list.append(str(dir_list+'\\'+items))
        except:
            pass #Filters non-accessable directories.

    fCount=len(file_list) # Get file count        
    file_list.sort()
    
    #Create HTML-------------------------------------
    open(F_path,'w').write('<html>\n<title>Search Results</title>\n<body bgcolor="#ffffff" text="#000000">\n<table align="left" bgcolor="#ffffff" border="0">\n<th align="left"><h1><u>'+File_type+' file list - total files: '+str(fCount)+'</u></h1><th><tr>\n')           
    for files in file_list:
        open(F_path,'a').write('<td><a href="'+files+'">'+files.upper()+'</a></td><tr>\n')
    open(F_path,'a').write('\n</table>\n</body>\n</html>')
    print F_path+' file created successfully...'
    
#RUN AND GEN YOUR HTML FILE--------------------------    
try:
    if __name__ == '__main__':
        print 'Slither 0.1.4 by Mohawke #B0)~\n' 
        Search_p = raw_input('Enter drive to search (letter only): ')
        Search_p=Search_p.strip()
        Search_path = str(Search_p+':')
        Report_path = str(Search_path+'\\Slither Report')
        
        File_t=raw_input('Enter file extension (txt, etc): ')
        File_type=File_t.strip()
        
        if not os.path.exists(Report_path): os.mkdir(Report_path)
            
        File_p=raw_input('Enter file name without .ext: ')
        File_p=File_p.strip()
        File_path = str(Report_path+'\\'+File_p+'.html')
        
        htmlGen(Search_path, File_path)
        raw_input('Done... Hit <Return> to end.')

except:
    raw_input('Error, try again... Hit <Return> to end.')
