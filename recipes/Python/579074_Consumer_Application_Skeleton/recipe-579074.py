"""This is very basic skeleton for data processing application implementing
consumer pattern.
"""

__author__ = 'vovanec@gmail.com'

from concurrent.futures import ThreadPoolExecutor

import functools
import logging
import signal
import threading


DEFAULT_NUM_WORKERS = 16


class ConsumerAppBase(object):
    """Base class for task consumer application.
    """

    sleep_timeout = 3

    def __init__(self, app_name, num_workers=DEFAULT_NUM_WORKERS):
        """Constructor.

        :param str app_name: application name.
        :param int num_workers: number of worker threads.
        """

        self._log = logging.getLogger(app_name)
        self._app_name = app_name
        self._stop_event = threading.Event()
        self._task_executor = ThreadPoolExecutor(max_workers=num_workers)
        self._task_limiter = threading.Semaphore(value=num_workers)

    def run(self):
        """Run application.
        """

        exit_status = 0
        self._install_signal_handlers()

        try:
            self._on_start()
            self._main_loop()
        except BaseException as exc:
            self._log.exception('Unrecoverable exception in %s main loop. '
                                'Exiting: %s', self._app_name, exc)
            exit_status = 1
        finally:
            self._stop_event.set()
            self._stop_task_executor()
            self._on_stop()

            self._log.info('Done.')

        return exit_status

    def stop(self):
        """Tell the main loop to stop and shutdown.
        """

        self._stop_event.set()

    def _get_next_task(self):
        """Get next task for processing. Subclasses MUST implement this method.

        :return: next task object. If None returned - framework assumes the
                 input queue is empty and waits for TaskProcessor.sleep_timeout
                 time before calling to _get_next_task() again.

        :rtype: object|None
        """

        raise NotImplementedError

    def _run_task(self, task):
        """Run task in separate worker thread of ThreadPoolExecutor.
        Subclasses MUST implement this method.

        :param object task: task item.

        :rtype: object|None
        :return: this method should return task execution result, that will be
                 available in _on_task_done() callback wrapped in
                 concurrent.futures.Future object.
        """

        raise NotImplementedError

    def _on_task_done(self, task, future):
        """This callback is being called after task finished.

        Subclasses may implement this method to handle tasks results,
        perform some cleanup etc.

        :param object task: task item.
        :param concurrent.futures.Future future: future that wraps
               task execution result.

        :rtype: None
        """

        pass

    def _on_start(self):
        """Subclasses may re-implement this method to add custom logic on
        application start, right before entering the main loop.
        """

        pass

    def _on_stop(self):
        """Subclasses may re-implement this method to add custom logic on
        application stop, right after exiting the main loop.
        """

        pass

    # Private methods

    def _install_signal_handlers(self):
        """Install signal handlers for the process.
        """

        self._log.info('Installing signal handlers')

        def handler(signum, _):
            """Signal handler.
            """

            self._log.info('Got signal %s', signum)
            self._stop_event.set()

        for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM,
                    signal.SIGQUIT, signal.SIGABRT):

            signal.signal(sig, handler)

    def _main_loop(self):
        """Main loop.
        """

        self._log.info('Entering the main loop')

        while not self._stop_event.is_set():

            # Try to get the next task. If exception occurred - wait and retry.
            try:
                task = self._get_next_task()
            except Exception as exc:
                self._log.exception(
                    'Failed to get next task for processing: %s. Sleeping '
                    'for %s seconds before retry.', exc, self.sleep_timeout)

                self._stop_event.wait(self.sleep_timeout)

                continue

            # If task is None - wait and retry to get the next task.
            if task is None:
                self._log.info(
                    'Task queue is empty. Sleeping for %s seconds before '
                    'retry.', self.sleep_timeout)

                self._stop_event.wait(self.sleep_timeout)

                continue

            self._log.debug('Got next task for processing: %s', task)
            if self._submit_task(task):
                self._log.debug('Successfully submitted task %s for processing',
                                task)
            else:
                # Submission was interrupted because application
                # has been told to stop. Exit the main loop.
                break

        self._log.info('%s has been told to stop. Exiting.', self._app_name)

    def _submit_task(self, task):
        """Submit task to the pool executor for processing.

        :param object task: task item.

        :return: True if submission was successful, False if submission was
                 interrupted because application is about to exit.

        :rtype: bool
        """

        while not self._stop_event.is_set():

            if self._task_limiter.acquire(blocking=False):
                try:
                    task_done_cb = functools.partial(self._task_done, task)
                    self._task_executor.submit(
                        self._run_task, task).add_done_callback(task_done_cb)

                    return True
                except Exception as exc:
                    self._task_limiter.release()
                    self._log.exception(
                        'Could not submit task for processing: %s. '
                        'Sleeping for %s seconds before next try.',
                        exc, self.sleep_timeout)
            else:
                self._log.info(
                    'No free workers. Sleeping for %s seconds before next try.',
                    self.sleep_timeout)

            self._stop_event.wait(self.sleep_timeout)

        return False

    def _task_done(self, task, future):
        """Called when task is done.

        :param object task: task item.
        :param concurrent.futures.Future future: future object.
        """

        self._task_limiter.release()
        self._on_task_done(task, future)

    def _stop_task_executor(self):
        """Stop task executor instance.
        """

        if self._task_executor:
            self._log.info('Stopping task executor')
            try:
                self._task_executor.shutdown(wait=True)
            except Exception as exc:
                self._log.exception(
                    'Exception while trying to stop task executor: %s', exc)



def main():
    """Example application.
    """

    class ExampleApp(ConsumerAppBase):
        """Example application.
        """

        def _get_next_task(self):

            import random
            import time

            time.sleep(.01)
            return random.randint(0, 1000)

        def _run_task(self, task):

            return task / 2

        def _on_task_done(self, task, future):

            self._log.info('Task done. Result: %s', future.result())

    logging.basicConfig(level=logging.DEBUG)

    ExampleApp('example').run()


if __name__ == '__main__':

    main()
