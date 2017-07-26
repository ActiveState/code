###Synchronizing worker threads using a common input source

Originally published: 2010-08-09 16:24:38
Last updated: 2010-08-09 16:24:38
Author: Uri Sternfeld

This class is used to synchronize worker threads that get their input from a common source that changes over time, and may even be empty on some occasions.\n\nThe problem is that the threads are unaware of the existence of other threads, and have no way of knowing whether any new input will be inserted by other threads. Instead of using a separate 'control' thread, or having the threads exit needlessly each time the input source is empty, a WorkersLounge instance can be used to synchronize them.\n\nThe commonest example is using a shared Queue.Queue object, where each thread may put additional jobs into it depending on its current job. When the queue is empty, the other threads 'rest' in the 'lounge'. When the last thread with a job is trying to 'rest', all the threads exit. When a thread puts new jobs into the queue, it should wake up any resting thread by calling the 'back_to_work' method.