"""
I am P1.  I am not yet intelligent.
I will download all of the recipes from the Python Cookbook using
the URL http://aspn.activestate.com/ASPN/Cookbook/Python?query_start=????
and store them into the drive and directory you specify.
I extract the file names using the recipe number and the HTML <a></a> string;
replacing special characters with an underscore.  I also clean up the filename.
Several files have no recipe number, open them, if they are blank, delete them.
Several files have a recipe number, but no name, open them, if they are blank, delete them,
if they have content, rename them appropriately.
Several files that are 19K in length contain HTML only and should be deleted, some files
are 19K in length and are valid files.
These problems are due to the Cookbook having missing recipes or pointers to recipes
that are no longer found, or invalid pointers.  I am P1.  I am not yet intelligent.
"""
import urllib,re,sys,string
fileInName = raw_input('Enter the drive and the full path name, with trailing backslash where the Python .py files will end up-->')
for x in range(1,2100,20):
    url = 'http://aspn.activestate.com/ASPN/Cookbook/Python?query_start=' + str(x)
    f = urllib.urlopen(url)
    s = f.read()
    f.close()
    matches = re.findall("/ASPN/Cookbook/Python/Recipe/(\d*)",s)
    pattern = '/ASPN/Cookbook/Python/Recipe/.*.(?=<)'
    name_matches = re.findall(pattern,s)
    for z in range (len(name_matches)):
        try: 
            if int(matches[z]) < int(100000):
                end = 36
            else:
                end = 37
        except:
            end = 36
        name_matches[z] = '_' + str(re.sub("[\[\`\~\!\@\#\$\%\ \^\&\*\(\)\_\+\-\=\{\}\\\:\;\<\>\,\.\?\/\|\'\"\]]",'_',name_matches[z][end:]))
        name_matches[z] = string.rstrip(name_matches[z],'_a')
        while '__' in name_matches[z]:
            name_matches[z] = string.replace(name_matches[z], '__', '_')
        name_matches[z] = '_' + matches[z] + name_matches[z] + '.py'
        name_matches[z] = string.replace(name_matches[z], '_py.py', '.py')
        name_matches[z] = string.replace(name_matches[z], '_by.py', '.py')
        name_matches[z] = string.replace(name_matches[z], 'quot_', '')
        url = 'http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/' + str(matches[z]) + '/index_txt'
        f = urllib.urlopen(url)
        s = f.read()
        f.close()
        fileOutName = str(fileInName) + str(name_matches[z])
        fileOut = open(fileOutName, 'w')
        fileOut.write(s)
        fileOut.close()    
print "I'm finished.";
