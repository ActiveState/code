import re
import sys
import string
import os.path
import time

"""
Reads the content of the two md5 files in two lists.

The lists content 'll be [md5, path, filename] :
* md5 : the md5, untouched
* path : the path, normalized (only forward slashes), filtered with the selected regular expression
* filename : the filename, untouched
"""

# re_compiled = re.compile('^\.svn|/\.svn')     # re to exclude all .svn directory (subversion administrative dirs)
re_compiled = re.compile('^$')     # re to exclude nothing

list_tmp = [line[:-1] for line in open(sys.argv[1],mode='rU').readlines()]      # reading first file
list_one = []    # initializing the first list
for x in list_tmp:      # writing the first list
    if x[0:1] <> '#' and x[0:1] <> ';' and x.strip() <> '' :   # skip comment lines (starting with '#' or ';') and empty lines
        str_md5 = x[:32]    # extract the md5
        str_path = string.replace(os.path.dirname(x[34:]),'\\','/')    # extract the path
        if str_path[0:1] == '/' : str_path = str_path [1:]    # remove the trailing '/' from the path
        str_filename = os.path.basename(x[34:])    # extract the filename
        if not re_compiled.search(str_path):    # exclude paths matching the re
            list_one.append((str_md5, str_path, str_filename))

list_tmp = [line[:-1] for line in open(sys.argv[2],mode='rU').readlines()]      # reading second file
list_two = []    # initializing the first list
for x in list_tmp:      # writing the first list
    if x[0:1] <> '#' and x[0:1] <> ';' and x.strip() <> '' and not re_compiled.search(x):   # skip comment lines (starting with '#' or ';') and empty lines
        str_md5 = x[:32]    # extract the md5
        str_path = string.replace(os.path.dirname(x[34:]),'\\','/')    # extract the path
        if str_path[0:1] == '/' : str_path = str_path [1:]    # remove the trailing '/' from the path
        str_filename = os.path.basename(x[34:])    # extract the filename
        if not re_compiled.search(str_path):    # exclude paths matching the re
            list_two.append((str_md5, str_path, str_filename))

list_tmp = []   # erasing the temp list

"""
Diff the two lists, obtaining two list 'list_xxx_diff' (md5, flag, path, filename) :
* flag :
** '==' equal (md5 =, path =, filename =)
** '<>' different (md5 <>, path =, filename =)
** '>>' new dx (md5 n/a, path <>, filename <>)
** '<<' new sx (md5 n/a, path <>, filename <>)
** 'm>' moved dx (md5 =, path <>, filename =)
** '<m' moved sx (md5 =, path <>, filename =)
** 'r>' renamed dx (md5 =, path =, filename <>)
** '<r' renamed sx (md5 =, path =, filename <>)
* first md5 : the md5 of the first md5 file
* second md5 : the md5 of the second md5 file
* path : path
* filename : filename
"""
# creating the two list containing the result of the diff'ing
list_one_diff = []
list_two_diff = []

# searching for '==' equal (md5 =, path =, filename =)
for x in range(len(list_one)):
    item_one = (list_one[x][0], list_one[x][1],list_one[x][2])
    for y in range(len(list_two)):
        item_two = (list_two[y][0], list_two[y][1],list_two[y][2])
        if item_one == item_two:
            list_one_diff.append([list_one[x][0], '==', list_one[x][1], list_one[x][2]])   # write in the first diff'ing result list
            list_two_diff.append([list_two[y][0], '==', list_two[y][1], list_two[y][2]])   # write in the second diff'ing result list
            list_one[x]=[]   # mark the first list element for removing
            del list_two[y]   # remove the current item from the second list
            break   # return to the upper for loop

list_one = [x for x in list_one if x <> []]   # remove marked items from the first list


# searching for '<>' different (md5 <>, path =, filename =)
for x in range(len(list_one)):
    item_one = (list_one[x][1],list_one[x][2])
    for y in range(len(list_two)):
        item_two = (list_two[y][1],list_two[y][2])
        if item_one == item_two:
            list_one_diff.append([list_one[x][0], '<>', list_one[x][1], list_one[x][2]])   # write in the first diff'ing result list
            list_two_diff.append([list_two[y][0], '<>', list_two[y][1], list_two[y][2]])   # write in the second diff'ing result list
            list_one[x]=[]   # mark the first list element for removing
            del list_two[y]   # remove the current item from the second list
            break   # return to the upper for loop

list_one = [x for x in list_one if x <> []]   # remove marked items from the first list


# searching for 'm>' moved dx and '<m' moved sx (md5 =, path <>, filename =)
for x in range(len(list_one)):
    item_one = (list_one[x][0],list_one[x][2])
    for y in range(len(list_two)):
        item_two = (list_two[y][0],list_two[y][2])
        if item_one == item_two:
            list_one_diff.append([list_one[x][0], '<m', list_one[x][1], list_one[x][2]])   # write in the first diff'ing result list
            list_two_diff.append([list_two[y][0], 'm>', list_two[y][1], list_two[y][2]])   # write in the second diff'ing result list
            list_one[x]=[]   # mark the first list element for removing
            del list_two[y]   # remove the current item from the second list
            break   # return to the upper for loop

list_one = [x for x in list_one if x <> []]   # remove marked items from the first list


# searching for 'r>' renamed dx and '<r' renamed sx (md5 =, path =, filename <>)
for x in range(len(list_one)):
    item_one = (list_one[x][0],list_one[x][1])
    for y in range(len(list_two)):
        item_two = (list_two[y][0],list_two[y][1])
        if item_one == item_two:
            list_one_diff.append([list_one[x][0], '<r', list_one[x][1], list_one[x][2]])   # write in the first diff'ing result list
            list_two_diff.append([list_two[y][0], 'r>', list_two[y][1], list_two[y][2]])   # write in the second diff'ing result list
            list_one[x]=[]   # mark the first list element for removing
            del list_two[y]   # remove the current item from the second list
            break   # return to the upper for loop

list_one = [x for x in list_one if x <> []]   # remove marked items from the first list


# searching for '>>' new dx and '<<' new sx (md5 n/a, path <>, filename <>)
for x in range(len(list_one)):
    list_one_diff.append([list_one[x][0], '<<', list_one[x][1], list_one[x][2]])   # write in the first diff'ing result list

for y in range(len(list_two)):
    list_two_diff.append([list_two[y][0], '>>', list_two[y][1], list_two[y][2]])   # write in the second diff'ing result list


"""
Printing the diff'ing list and some stats
"""

# printing the first diff'ed md5
print "#\n# diff'ed md5 '" + sys.argv[1] +"' (" +time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + ")\n#"  # prints the header of the first diff'ed md5 file

for x in range(len(list_one_diff)):   # loops on the first diff'ing list, and print each element
    print list_one_diff[x][0] + list_one_diff[x][1] + list_one_diff[x][2] + '/' + list_one_diff[x][3]


# printing the second diff'ed md5
print "\n\n#\n# diff'ed md5 '" + sys.argv[2] +"' (" +time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + ")\n#"  # prints the header of the second diff'ed md5 file

for x in range(len(list_two_diff)):   # loops on the first diff'ing list, and print each element
    print list_two_diff[x][0] + list_two_diff[x][1] + list_two_diff[x][2] + '/' + list_two_diff[x][3]


# printing stats of the first list
list_stats = [x for (a,x,b,c) in list_one_diff]    # create a list containing only flag from the first diff list, used to create stats
print "\n\n\n#   *** stats of '" + sys.argv[1] +"' ***\n#"   # print stats header
print '#   ==  equal      ', list_stats.count('==')
print '#   <>  different  ', list_stats.count('<>')
print '#   <<  new sx     ', list_stats.count('<<')
print '#   <r  renamed sx ', list_stats.count('<r')
print '#   <m  moved sx   ', list_stats.count('<m')
print '#   --  total      ', len(list_stats)


# printing stats of the second list
list_stats = [x for (a,x,b,c) in list_two_diff]    # create a list containing only flag from the second diff list, used to create stats
print "\n\n#   *** stats of '" + sys.argv[2] +"' ***\n#"   # print stats header
print '#   ==  equal      ', list_stats.count('==')
print '#   <>  different  ', list_stats.count('<>')
print '#   >>  new dx     ', list_stats.count('>>')
print '#   r>  renamed dx ', list_stats.count('r>')
print '#   m>  moved dx   ', list_stats.count('m>')
print '#   --  total      ', len(list_stats)
