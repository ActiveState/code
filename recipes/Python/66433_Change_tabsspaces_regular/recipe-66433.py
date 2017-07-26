import re

def entab(temp, tab_width=4, all=0):

        #if all is true, every time tab_width number of spaces are found next
        #to each other, they are converted to a tab.  If false, only those at
        #the beginning of the line are converted.  Default is false.

        if all:
                temp = re.sub(r" {" + `tab_width` + r"}", r"\t", temp)
        else:
                patt = re.compile(r"^ {" + `tab_width` + r"}", re.M)
                temp, count = patt.subn(r"\t", temp)
                i = 1
                while count > 0:
                        #this only loops a few times, at most six or seven times on
                        #heavily indented code
                        subpatt = re.compile(r"^\t{" + `i` + r"} {" + `tab_width` + r"}", re.M)
                        temp, count = subpatt.subn("\t"*(i+1), temp)
                        i += 1
        return temp


def detab(temp, tab_width=4):

        #this code is lazy, but it gets the job done and it's what I use there
        #is no need for a only convert tabs to spaces at beginning of line
        #since if you are taking out tabs it is usually more than just an
        #indentation problem
       
        return temp.expandtabs(tab_width)
