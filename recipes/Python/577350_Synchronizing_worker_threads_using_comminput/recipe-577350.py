import threading

class WorkersLounge(object):
	
	def __init__(self, total_workers_number):
		"""
		@param total_workers_number: the maximum number of worker threads
		"""
		self.total_workers_number = total_workers_number
		self.waiting_place = threading.Condition()
		self.work_done_event = threading.Event()
		
	def rest(self):
		"""
		When a thread calls this method there are two possible options:
		 - either there are other active threads, in which case the current thread waits
		 - all other threads are already waiting, in which case they all exit
		
		@return: True if the caller thread should go back to work
			 False if the caller thread should exit
		"""
		with self.waiting_place:
			if (len(self.waiting_place._Condition__waiters) ==
                            self.total_workers_number-1):
				# This is the last worker, and it has nothing to do
				self.work_done_event.set()				
				self.waiting_place.notifyAll()				
				# Notify the caller there is no more work to do
				return False
			else:
				# Wait for a signal
				self.waiting_place.wait()				
				return not(self.work_done_event.isSet())			
		
	def back_to_work(self):
		"""
		Wake up all the waiting threads.
		Should be called whenever a thread puts new input into the common source.
		"""
		# Wake up everybody
		with self.waiting_place:
			self.waiting_place.notifyAll()

if __name__ == "__main__":
	# Run test code
	import Queue
	import time
	
	print_lock = threading.Lock()
	def sync_print(text):
		with print_lock:
			print text
	
	def _thread_proc(input_queue, workers_lounge):
		thread_name = threading.currentThread().name
		while 1:
			try:
				# Attempt to get input from the common queue
				input = input_queue.get(timeout=0.1)
				# Do something with the input, possibly inserting more jobs
				# back into the queue
				sync_print("%s got input %s"%(thread_name, input))	
				time.sleep(1)
				if (input < 5):
					input_queue.put(input+1)
					input_queue.put(input+1)
					# Wake up any waiting thread
					workers_lounge.back_to_work()
			except Queue.Empty:
				# The 'rest' method returns False if the thread should stop,
				# and blocks until someone wakes it up
				sync_print("%s is resting"%thread_name)
				if (workers_lounge.rest() == False):
					sync_print("%s finished working"%thread_name)
					break

	# Create an initial input source
	input_queue = Queue.Queue()
	input_queue.put(1)
	input_queue.put(1)
	# Run worker threads
	threads_number = 5
	workers_lounge = WorkersLounge(total_workers_number=threads_number)
	for _i in range(threads_number):
		threads.append(
                        threading.Thread(target=_thread_proc, args=(input_queue, workers_lounge)))
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
