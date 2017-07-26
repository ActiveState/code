#!/usr/bin/python

import os,time,sys

time_map = { 	"seconds"	: 1,
				"minutes"	: 60,
				"hours"		: 3600,
				"days"		: 86400
			}

def get_pid_status(pid):
	#True is running, False is not running
	ps_command = "ps -p " + str(pid)
	popen_results = os.popen4(ps_command)
	for line in popen_results[1]:
		contents = line.split()
		if contents[0] == str(pid):
			return True
	return False

def wallclock(command,lifetime=120,poll=1,repeat=0,time_unit="hours"):
	#This prevents zombie problems
	import signal
	signal.signal(signal.SIGCHLD, signal.SIG_IGN)
	if time_unit not in time_map.keys():
		print "This is not an accepted unit- treating as seconds. Acceptable units are:"
		for item in time_map.keys():
			print "\t" + item
	else:
		lifetime *= time_map[time_unit]
		poll *= time_map[time_unit]
	
	#The wallclock subroutine is written to run a command, but kill it and rerun it if doesn't finish in a certain time period (or after a given number of repeats
	#It is a "dumb" command- it should behave as a simple replacement for most "os.system()" calls, but with extra options
	pid = os.fork()
	if pid == 0:
		#child process- run the command and exit
		os.setpgrp() # Sets process session leader.
		os.system(command)
		#print "Child process command executed. I should exit"
		sys.stdout.flush()
		#This requires SIGCHLD to be set to SIG_IGN, to prevent a zombie process from appearing
		os._exit(0)
	else:
		current_time = 0
		while(current_time < lifetime):
			if get_pid_status(pid):
				#print "Child process " +str(pid) +" is running and I will sleep for " + str(poll) + " seconds"
				time.sleep(poll)
				current_time += poll
			else:
				#print "Parent process should now finish and return you"
				signal.signal(signal.SIGCHLD, signal.SIG_DFL)
				return 1
		#If you end up here, time has run out and the program has not finished: recurse & repeat (if required)
		#signal.signal(signal.SIGCHLD, signal.SIG_DFL)
		if repeat > 0:
			repeat -= 1
			os.kill(-pid,signal.SIGKILL)
			signal.signal(signal.SIGCHLD, signal.SIG_DFL)
			return wallclock(command,lifetime=lifetime,poll=poll,time_unit=time_unit,repeat=repeat)
		else:
			#give up, kill child and return 0
			os.kill(-pid,signal.SIGKILL)
			signal.signal(signal.SIGCHLD, signal.SIG_DFL)
			return 0
