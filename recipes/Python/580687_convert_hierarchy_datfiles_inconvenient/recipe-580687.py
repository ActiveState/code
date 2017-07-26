#!/usr/bin/env python3
# Author: Brian Fiedler 29 June 2016
# Converts the CRUTEM text data files into a convenient Python dictionary.
# Go to http://www.metoffice.gov.uk/hadobs/crutem4/data/download.html and you should see
# a link to http://www.metoffice.gov.uk/hadobs/crutem4/data/station_files/CRUTEM.4.4.0.0.station_files.zip
# Download that and unzip it, and set path_crutem below.
# Then: python CRUTEM_to_pkl.py 
# And: python CRUTEM_to_pkl.py mini
# Example of using the pkl files that were produced:
# inpkl = open('/data/crutem4/crutem44_mini.pkl','rb')
# crutem = pickle.load(inpkl)
# sitename = crutem['723530']['Name'] 
# monthAvgTemp = crutem['723530']['obs'][2011][6] 
# print("July 2011 temperature at",sitename,":",monthAvgTemp)
import glob,sys,pickle

path_crutem = "/data/crutem4/CRUTEM.4.4.0.0.station_files" # Configure for your computer

outpklname='crutem44_all.pkl'
if len(sys.argv)>1 and sys.argv[1]=='mini':
    outpklname='crutem44_mini.pkl' #note: mini in name triggers filter below

files=glob.glob(path_crutem+'/*/*')
print(files)
files.sort()
##############
def crutemread(fn,verbose=False):
    ''' for reading hadcrut station data files'''
    inf = open(fn,'r',encoding="ISO-8859-1") # open fn for reading
    lines = inf.readlines()#
    h={} # data file will be converted to a dictionary and store here
    doingObs = False # this changes to True when 'Obs.' is encountered in a line
    h['obs']={} # will have integer years as keys, to hold list of monthly temperatures
    for line in lines: 
        if line[0:4]=='Obs:':
            doingObs=True
            continue
        if not doingObs: # parameter values are put in dictionary
            s = line.strip().split('=') 
            parts = [x.capitalize() for x in s[0].split()]
            key = ''.join(parts)
            v = s[-1].strip()
            if v.isdigit():
                value = int(v)
            else:
                try:
                    value = float(v)
                except:
                    value = v
            if verbose: print(key,value)
            h[key] = value
        else: #process the line the begins with a year number
            s = line.strip().split()
            key = int(s[0])
            values = [float(x) for x in s[1:]] # 12 temperature numbers, and 12 code numbers
            h['obs'][key] = values
    return h 


# When making a minature pkl file with just 12 sites, only these values for filenames are retained
minikeep = '724830 725300 722230 225500 724210 756039 719360 702000 723530 040300 725460 014920'.split()
qall = {} # will be a master dictionary of dictionaries, to be pickled
count = 0
for filename in files:
    z = filename.split('/')
    if 'mini' in outpklname and z[-1] not in minikeep: continue 
    print(filename)
    q = crutemread(filename,verbose=False) # The file is put into a Python dictionary
    recn = z[-1] # dictionary key is the file name
    qall[recn] = q  # add dictionary to the master dictionary that will be pickled
    count += 1

poufa = open(outpklname,'wb')
pickle.dump(qall,poufa,-1)
poufa.close()
print("wrote",outpklname,"number of sites=",count)
