# svcAdmin.py
# in principal this could be expanded to support linux operations
# such as the RedHat style: service <name> status|start|stop|restart
#
import os
import time
from types import *
if os.name == 'nt':
	import win32service
	import win32serviceutil
	RUNNING = win32service.SERVICE_RUNNING
	STARTING = win32service.SERVICE_START_PENDING
	STOPPING = win32service.SERVICE_STOP_PENDING
	STOPPED = win32service.SERVICE_STOPPED
	
	def svcStatus( svc_name, machine=None):
		return win32serviceutil.QueryServiceStatus( svc_name, machine)[1]	# scvType, svcState, svcControls, err, svcErr, svcCP, svcWH

	def svcStop( svc_name, machine=None):
		status = win32serviceutil.StopService( svc_name, machine)[1]
		while status == STOPPING:
			time.sleep(1)
			status = svcStatus( svc_name, machine)
		return status

	def svcStart( svc_name, svc_arg = None, machine=None):
		if not svc_arg is None:
			if type(svc_arg) in StringTypes:
				# win32service expects a list of string arguments
				svc_arg = [ svc_arg]
		win32serviceutil.StartService( svc_name, svc_arg, machine)
		status = svcStatus( svc_name, machine)
		while status == STARTING:
			time.sleep(1)
			status = svcStatus( svc_name, machine)
		return status

if __name__ == "__main__":
	svc = 'mysql'
	#machine = '192.168.0.4'	# no \\ prefix
	machine = None			# localhost
	test_arg = (None, r'--datadir=f:\mysql\data_playpark')
	modulus = len(test_arg)
	argndx = 0
	for i in range(2 * modulus):
		status = svcStatus( svc, machine=machine)
		if status == STOPPED:
			arg = test_arg[argndx % modulus]
			new_status = svcStart( svc, arg, machine=machine)
			argndx += 1
		elif status == RUNNING:
			arg = None
			new_status = svcStop( svc, machine=machine)
		else:
			arg = None
			new_status = "Not changed"
		print "Status changed from %s to %s (with arg: %s)" % (status, new_status, arg)
