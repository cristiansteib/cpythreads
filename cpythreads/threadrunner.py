import threading
from queue import Queue
from sonarqube_reviewer.threads.threadrunnable import ThreadRunnable
import logging
from time import sleep


class ThreadRunner(threading.Thread):
    TOTAL_THREADS = 0

    def __init__(self, queue: Queue, group=None, target=None, name=None, verbose=None):
        super(ThreadRunner, self).__init__(
            group=group,
            target=target,
            name=name
        )
        self.verbose = verbose
        self.queue = queue
        self.killed = False
        self._is_busy = False
        ThreadRunner.TOTAL_THREADS += 1

    def kill(self):
        self.killed = True

    def is_busy(self):
        return self._is_busy

    def is_idle(self):
        return not self._is_busy

    def run(self):
        logging.debug("Starting thread: %s" % self.name)
        while True:
            if self.killed:
                logging.debug("Stopping thread: %s" % self.name)
                break
            if not self.queue.empty():
                self._is_busy = True
                class_runnable: ThreadRunnable = self.queue.get()
                class_runnable.run()
                self._is_busy = False
            else:
                sleep(1)

    def __del__(self):
        ThreadRunner.TOTAL_THREADS -= 1