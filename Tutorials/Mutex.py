import time
from threading import Thread
from threading import Lock

def myfunc(i, mutex):
    mutex.acquire(1)
    time.sleep(1)
    print("Thread: %d" %i)
    mutex.release()


mutex = Lock()
for i in range(0,10):
    t = Thread(target=myfunc, args=(i,mutex))
    t.start()
    print("main loop %d" %i)