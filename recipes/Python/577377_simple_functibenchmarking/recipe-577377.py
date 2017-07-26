'''
Created on Sep 21, 2009

@author: tcezard
This module enable its user to monitor the amount of time spend in between two commands start and stop.
The module is fairly imprecise if the monitored task is quick as the start and stop commands are fairly slow (2e-07 - 5e-07)
'''
from time import time
from math import sqrt
import logging

total = {}
started = {}

        
def start(key):
    started[key]=time()


def stop(key):
    stop=time()
    start=started.pop(key,None)
    if start:
        if total.has_key(key):
            total[key].append(stop-float(start))
        else:
            total[key]=[stop-float(start)]
    else:
        logging.error("stopping non started timer: %s"%key)
    


def print_all():
    header = [ 'title', 'N', 'sum (s)', 'min (s)', 'max (s)', 'mean (s)','std dev (s)' ]
    line_array=[]
    for key in total.keys():
        values=total.get(key)
        n = len(values)
        s=sum(values)
        mean = s / n
        sd = sqrt(sum((x-mean)**2 for x in values) / n)
        line_array.append([key, n,s,min(values),max(values),mean,sd])
        #logging.info("%s: n=%s\tsum=%s\tmin=%s\tmax=%s\tmean=%s\tstd_dev=%s"%(key,n,s,min(values),max(values),mean,sd))
    print format_array_line(line_array, header)


def format_array_line(line_array, column_header):
    """This function creates a array formated string of all the job provided."""
    #get the column length
    column_length=[]
    for header in column_header:
        column_length.append(len(header))
    for sp_line in line_array:
        for pos in range(len(sp_line)):
            column_length[pos]
            length = len(str(sp_line[pos]))
            if column_length[pos]<length:
                column_length[pos]=length
                
    line_length=0
    # get the total length of the line
    for i in range(len(column_length)):
        column_length[i]+=0
        line_length+=column_length[i]
    line_length+=(len(column_length)*3) + 1
    return_string=[]
    #print the Text
    seperation_line='-'*line_length
    return_string.append(seperation_line)
    outString=' '
    headers_str=[]
    for i in range(len(column_header)):
        headers_str.append(' %-*s '%(column_length[i],column_header[i]))
    return_string.append(outString+outString.join(headers_str)+outString)
    return_string.append(seperation_line)
    for sp_line in line_array:
        values_str=[]
        for i,header in enumerate(column_header):
            values_str.append(' %-*s '%(column_length[i],sp_line[i]))
        return_string.append(outString+outString.join(values_str)+outString)
    return_string.append(seperation_line)
    return '\n'.join(return_string)

if __name__=='__main__':
    for i in range(100):
        start('sleep')
        time.sleep(0.1)
        stop('sleep')
    print_all()
    
if __name__=='1__main__':
    for i in range(100000):
        start('Test')
        stop('Test')
    print_all()
