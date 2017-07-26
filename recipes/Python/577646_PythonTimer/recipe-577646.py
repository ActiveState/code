#!/usr/bin/python

#(c) 2011 , Narendra Sisodiya , narendra@narendrasisodiya.com 
#    Saturday, 09 April 2011

#
#   Released under MIT License
#

import time

class TickTockTimer:

	def StartTimer(self):
		self.TimerOffset = time.time()
		self.LastTicked = 0
		self.TimeWhenItWasPaused = 0
		self.paused = False
	
	def Tick(self):
		if self.paused is False:
			NewTicked = time.time() - self.TimerOffset
			diff = NewTicked - self.LastTicked
			self.LastTicked = NewTicked
			return diff
		else:
			print "Cannot Tick, Timer is paused"

	def GetTime(self):
		if self.paused is True:
			return self.TimeWhenItWasPaused
		else:
			return time.time() - self.TimerOffset
		
	def Pause(self):
		self.TimeWhenItWasPaused = time.time() - self.TimerOffset
		self.paused = True

	def UnPause(self):
		self.TimerOffset = time.time() - self.TimeWhenItWasPaused
		self.paused = False
