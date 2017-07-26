import threading

class myWorker:
	
	def _threadProc( self):
		"""This is where the work gets done"""
		while 1:
			if self._threadShouldStop():
				break 
			"""
			If you're waiting on an event in doSomeWorkOrWait that is not expected
			  to return with no activity, then set a largish (~1 second) timeout.
			 If you're using Python 2.2x, you could use generators and yield out
			   every so often.
			"""
			obj.doSomeWorkOrWait( TIMEOUT)
			if obj.workIsFinished()
				break
			 
	def watchdog( self):
		"""
		If used, this fn should be called "often" - if not, it could be a sign that
		  the calling code has stopped operating as expected.
		  Some time.time() logic could be used in _threadShouldStop 
		   to extend the amount of time available. 
		"""
		self._pingCount += 1
	def _threadShouldStop( self):
		""" Return true if there's a reason the thread should stop"""
		manualStop = self.stopThread 
		mainThreadGone = not self.callingThread.isAlive() 
		somethingStalled = self._pingCount == 0
		self._pingCount = 0

		return manualStop or mainThreadGone or somethingStalled
		
	def startNewThread( self):
		"""
		Start a new thread, executing the code in _threadProc.
		We're assuming the main thread, or whichever we want 
		   to depend on being alive, is calling this function.
		"""
		self.callingThread = threading.currentThread()
		self.stopThread = 0
		self.thread = threading.Thread( target=self._threadProc)
		self.thread.setDaemon( 0)
		self.thread.start()
