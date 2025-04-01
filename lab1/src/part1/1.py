import threading
import queue
import time

"""
When a thread finishes executing a task, it will automatically go back to the thread pool's 
thread queue to wait for the next task to be assigned to it. This is because the thread is 
still running the worker method, which is a loop that repeatedly checks the task queue for new tasks.
"""

class ThreadPool:
    def __init__(self, no_of_threads):
        self.no_of_threads = no_of_threads
        self.task_queue = queue.Queue()
        self.threads = []
        self.lock = threading.Lock()
        # flag for threads to check new tasks in the task queue
        self.is_running = True

        # create threads and assign a job that checks for new tasks in the task queue
        for i in range(no_of_threads):
            thread = threading.Thread(target=self.check_task_queue)
            thread.start()
            self.threads.append(thread)
    
    # pushes the task into the task queue for threads to execute the task
    def push_task(self, task):
        # self.lock.acquire()
        self.task_queue.put(task)
        # self.lock.release()

    """
    when a thread is created, we are assigning this job to the thread such that the thread always checks the task queue for
    any new tasks pushed into the queue. This is done for every 100ms (see time.sleep at the end). And, also when a thread 
    finishes executing the task, it will automatically go back to threadpool to check for the new task as the thread is still
    running this job. This method can be treated as a event loop.
    """
    def check_task_queue(self):
        while self.is_running:
            try:
                """
                we are locking the queue such that single thread accesses the task queue at a time to avoid race conditions
                and releasing the lock after the task is executed
                """
                self.lock.acquire()
                print("queue in thread ", list(self.task_queue.queue))
                task = self.task_queue.get()
                
                task()
                self.lock.release()
            except queue.Empty:
                pass
            # sleep for sometime before checking the task queue again for any new tasks
            # commenting the below line to compare latency with gRPC call. Otherwise the comparison wont be fair
            # time.sleep(0.1)

    # stop the threadpool
    def stop(self):
        # make it false to stop the threads to look for new tasks in the queue (see the check_task_queue method )
        self.is_running = False

        for thread in self.threads:
            thread.join()
