#!/usr/bin/env python

def run_async(func):
	"""
		run_async(func)
			function decorator, intended to make "func" run in a separate
			thread (asynchronously).
			Returns the created Thread object

			E.g.:
			@run_async
			def task1():
				do_something

			@run_async
			def task2():
				do_something_too

			t1 = task1()
			t2 = task2()
			...
			t1.join()
			t2.join()
	"""
	from threading import Thread
	from functools import wraps

	@wraps(func)
	def async_func(*args, **kwargs):
		func_hl = Thread(target = func, args = args, kwargs = kwargs)
		func_hl.start()
		return func_hl

	return async_func

if __name__ == '__main__':
	from time import sleep

	@run_async
	def print_somedata():
		print 'starting print_somedata'
		sleep(2)
		print 'print_somedata: 2 sec passed'
		sleep(2)
		print 'print_somedata: 2 sec passed'
		sleep(2)
		print 'finished print_somedata'

	def main():
		print_somedata()
		print 'back in main'
		print_somedata()
		print 'back in main'
		print_somedata()
		print 'back in main'

	main()
