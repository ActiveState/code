## Consumer Application Skeleton  
Originally published: 2015-06-30 03:18:13  
Last updated: 2015-06-30 03:24:07  
Author: Vovan   
  
# Consumer Application Skeleton

This is very basic skeleton for data processing application implementing
consumer pattern:

    while is_running():
        task = get_next_task_from_queue()
        if task:
            submit_task_for_processing(task)
        else:
            sleep_for_a_moment()

Here's an example:

    class ExampleApp(ConsumerAppBase):
    
        def _get_next_task(self):
    
            # Get next task from the queue.
            return self._queue.next()
    
        def _run_task(self, task):
    
            # This code's being executed in separate worker thread of
            # ThreadPoolExecutor
            return task / 2
    
        def _on_task_done(self, task, future):
    
            # Once worker thread finished - task results are available
            # in _on_task_done() callback as a concurrent.futures.Future object.
            self._log.info('Task done. Result: %s', future.result())