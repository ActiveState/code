# -*- coding: utf-8 -*-
"""
Assembled by : Peter Arwanitis (spex66)

Task: Administrative job to run in my case 2300 jobs in a scheduled manner
Restriction: Don't start two jobs at same schedule on same server

Problems to solve that for:
* align list of projects into batch of jobs with distinct servers
* templated job creation
* create a crontab 
** to start all this jobs from a starting schedule every hour
** respect some restrictions that on some days and some hours no jobs should be started
** thanks to standard-library time, datetime and timedelta to make that an ease at the end!

References:
* http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/410687
    Transposing a List of Lists with Different Lengths without Loosing Elements (by Zoran Isailovski)
* thanks to Gerhard Kalab for his excellent pycron (cause it runs on windows too :))
    http://www.kalab.com/freeware/pycron/pycron.htm

Targeted on windows and python23
"""

import os, time
from datetime import datetime, timedelta

report_ROOTDIR = r"/tmp/jobs"
crontabBuilderData = """
# list of jobnames with paramaters to run on a specific server
jobname1,server1,param1,param2,param3
jobname2,server1,param1,param2,param3
jobname3,server1,param1,param2,param3
jobname4,server2,param1,param2,param3
jobname5,server2,param1,param2,param3
jobname6,server3,param1,param2,param3
jobname7,server4,param1,param2,param3
jobname8,server4,param1,param2,param3
"""

def groupProjectsByUniqueServer():
    listOfJobs = [l.strip().split(',') 
                    for l in crontabBuilderData.split('\n') # or read this from file
                    if not l.startswith('#')                # skip comments
                    if l.strip()                            # skip empty lines
                    ]

    print listOfJobs

    # group by servername    
    dictByServer = {}
    _skip = [dictByServer.setdefault(i[1], []).append(i) for i in listOfJobs]
    
    # align them that way, that each server comes up only one time in a batch of job
    # background: to minimize server load on then same time
    
    # clean up the None's out of the lists got from map(None, list1, list2, list3) of different length
    # most elegant solution?-) kudos to Recipe/410687
    # for some more insights how to handle such mappings, I never fiddled out that *row part!
    alignedJobs = map(lambda *row: [elem for elem in row if elem is not None],*dictByServer.values())                            

    return alignedJobs
    
def reportcrontab(alignedprojects, year, month, day=1, hour=0, excludedays=[], excludehours=[]):
    
    # start from that date at default 0 o'clock
    # remember start for some statistics
    startschedule = schedule = datetime(year, month, day, hour)

    # prepare that folders for job creation
    
    report_logfile = os.path.join(report_ROOTDIR, 'logs', "%(scheduled_time)s_%(jobname)s.log")
    report_cmddir  = os.path.join(report_ROOTDIR, 'cmds')
    
    report_crontabname = os.path.join(report_ROOTDIR, "crontab_projects.txt")
    report_crontabheader = """
    # THIS CONFIGURATION IS AUTOMATICALLY GENERATED!!!
    # this version is from: %s
    """ % (time.strftime('%Y-%m-%d/%H:%M:%S', time.localtime()))

    # 0 13 15 6 * "test.cmd" 
    report_crontabtemplate = '''0 %(hour)s %(day)s %(month)s * "%(cmd)s"'''
    report_crontab = []
    
    # example template for commandfile generation
    report_commands   =  [
       "@echo SomeJobRunner --name %(jobname)s --server=%(server)s --p1 %(param1)s --p2 %(param2)s --p3 %(param3)s 1> " + report_logfile,
       r"c:", 
       r"cd c:\python23", 
       "python SomeJobRunner.py --name %(jobname)s --server=%(server)s --p1 %(param1)s --p2 %(param2)s --p3 %(param3)s 1>> " + report_logfile + " 2>&1",
       ]
    report_cmd_template = '\n'.join(report_commands)
    
    project_count = 0
    while alignedprojects:        
        if schedule.weekday() in excludedays:
            continue # SKIP
        if schedule.hour in excludehours:
            continue # SKIP
    
        actual = alignedprojects.pop(0) #reduce the stack, from TOP where the biggest projects are
        
        for (jobname, server, param1, param2, param3) in actual:
            project_count += 1
            # build a characteristic prefix
            scheduled_time = '%i%02i%02i_%02i' % (
                                             schedule.year, 
                                             schedule.month, 
                                             schedule.day, 
                                             schedule.hour
                                             )
            jobcmddfile = os.path.join(report_cmddir, '%s_%s.cmd' % ( scheduled_time,
                                                                     jobname))

            # write complete batch out
            # hint: the replace is only essential on windows, cause % is reserved!
            # locals() to feed right away parameters wia keywords into command template
            file(jobcmddfile,'w').write((report_cmd_template % locals()).replace('%', '%%')) 

            report_crontab.append( report_crontabtemplate % {
                                            'hour'  : schedule.hour,
                                            'day'   : schedule.day,
                                            'month' : schedule.month,
                                            'cmd'   : jobcmddfile,
                                            }
                                   )
        # jump to next time slice
        schedule += timedelta(hours=1) # next hour, place your stepping here
    
    
    file(report_crontabname, 'w').write('\n'.join([report_crontabheader]+report_crontab))
    
    print '%i projects scheduled starting from %s, ends up %s' % (project_count, startschedule, schedule)
    print 'no schedules at hours (%s) and days of week (%s) # Monday is 0 and Sunday is 6' % (excludehours, excludedays)
    
def buildReportCrontab():

    # configure startdate here
    year, month, day = (2007, 5, 26)

    # configure excludes to skip over here
    # Monday is 0 and Sunday is 6
    excludedays  = [6]   # for example: keep free backup day
    excludehours = [6,7] # for example: keep free administrative window

    # build for every hour a slice of jobs running on different fileshares
    reportcrontab(groupProjectsByUniqueServer(), year, month, day, excludedays=excludedays, excludehours=excludehours)
    
if __name__ == '__main__':
    # let it run
    buildReportCrontab()

""" example crontab, no fun to make that for 2300 jobs :)

    # THIS CONFIGURATION IS AUTOMATICALLY GENERATED!!!
    # this version is from: 2007-05-28/09:25:21
    
0 0 26 5 * "/tmp/jobs/cmds/20070526_00_jobname7.cmd"
0 0 26 5 * "/tmp/jobs/cmds/20070526_00_jobname1.cmd"
0 0 26 5 * "/tmp/jobs/cmds/20070526_00_jobname4.cmd"
0 0 26 5 * "/tmp/jobs/cmds/20070526_00_jobname6.cmd"
0 1 26 5 * "/tmp/jobs/cmds/20070526_01_jobname8.cmd"
0 1 26 5 * "/tmp/jobs/cmds/20070526_01_jobname2.cmd"
0 1 26 5 * "/tmp/jobs/cmds/20070526_01_jobname5.cmd"
0 2 26 5 * "/tmp/jobs/cmds/20070526_02_jobname3.cmd"
"""
