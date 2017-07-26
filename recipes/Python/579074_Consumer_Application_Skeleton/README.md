###Consumer Application Skeleton

Originally published: 2015-06-30 03:18:13
Last updated: 2015-06-30 03:24:07
Author: Vovan 

# Consumer Application Skeleton\n\nThis is very basic skeleton for data processing application implementing\nconsumer pattern:\n\n    while is_running():\n        task = get_next_task_from_queue()\n        if task:\n            submit_task_for_processing(task)\n        else:\n            sleep_for_a_moment()\n\nHere's an example:\n\n    class ExampleApp(ConsumerAppBase):\n    \n        def _get_next_task(self):\n    \n            # Get next task from the queue.\n            return self._queue.next()\n    \n        def _run_task(self, task):\n    \n            # This code's being executed in separate worker thread of\n            # ThreadPoolExecutor\n            return task / 2\n    \n        def _on_task_done(self, task, future):\n    \n            # Once worker thread finished - task results are available\n            # in _on_task_done() callback as a concurrent.futures.Future object.\n            self._log.info('Task done. Result: %s', future.result())