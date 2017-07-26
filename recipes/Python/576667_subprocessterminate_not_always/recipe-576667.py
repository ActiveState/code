# ----------------------------------------------------------------------------
# subprocess.terminate is not implemented on some Windows python versions.
# This workaround works on both POSIX and Windows.
def subprocess_terminate( proc ) :
	try:
		proc.terminate()
	except AttributeError:
		print " no terminate method to Popen.."
		try:
			import signal
			os.kill( proc.pid , signal.SIGTERM)
		except AttributeError:
			print "  no os.kill, using win32api.."
			try:
				import win32api
				PROCESS_TERMINATE = 1
				handle = win32api.OpenProcess( PROCESS_TERMINATE, False, proc.pid)
				win32api.TerminateProcess(handle,-1)
				win32api.CloseHandle(handle)
			except ImportError:
				print "  ERROR: could not terminate process."
