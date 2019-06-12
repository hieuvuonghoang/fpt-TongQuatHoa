import threading
import math

class WorkerThread(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data # Initiliaze data for thread

    def run(self):
        # This method is invoked when starting a thread
        # Do the work of thread here.
        print('Thread {} is running with data: {}'.format(self.ident, self.data))

if __name__ == '__main__':
    a = 'goodkat'
    b = 'godfather'

    # Create thread by passing target_func to target param
    #thread1 = threading.Thread(target=target_func, args=(a,))

    # Or by using CheckPrimeThread
    thread1 = WorkerThread(a)
    thread2 = WorkerThread(b)

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for thread1, thread2 to terminate
    thread1.join()
    thread2.join()

    print('Main thread exited')