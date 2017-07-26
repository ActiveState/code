import win32event
import pythoncom

TIMEOUT = 200 # ms

StopEvent = win32event.CreateEvent(None, 0, 0, None)
OtherEvent = win32event.CreateEvent(None, 0, 0, None)

class myCoolApp:
        def OnQuit(self):
		win32event.SetEvent(StopEvent) # exit msg pump


def _MessagePump():

	while 1:
		
		rc = win32event.MsgWaitForMultipleObjects(
			(StopEvent,OtherEvent), 
			0, # wait for all = false
			TIMEOUT,  #  (or win32event.INFINITE)
			win32event.QS_ALLEVENTS) # type of input

		# You can call a function here if it doesn't take too long.
		#   It will get executed *at least* every 200ms -- possibly
		#   a lot more, depending on the number of windows messages received.

		if rc == win32event.WAIT_OBJECT_0:
			# Our first event listed was triggered.
			# Someone wants us to exit.
			break
		elif rc == win32event.WAIT_OBJECT_0+1:
			# Our second event "OtherEvent" listed was set.
			# This is from some other component -
			#   wait on as many events as you need
		elif rc == win32event.WAIT_OBJECT_0+2:
			# A windows message is waiting - take care of it.
			# (Don't ask me why a WAIT_OBJECT_MSG isn't defined < WAIT_OBJECT_0)
			# Note: this must be done for COM and other windowsy
			#   things to work.
			if pythoncom.PumpWaitingMessages():
				break # wm_quit
		elif rc == win32event.WAIT_TIMEOUT:
			# Our timeout has elapsed.
			# Do some work here (e.g, poll something can you can't thread)
			#   or just feel good to be alive.
			# Good place to call watchdog(). (Editor's note: See my "thread lifetime" recepie.)
			pass
		else:
			raise RuntimeError( "unexpected win32wait return value")
