import threading

class MyMessenger(threading.Thread):
    def run(self):
        for _ in range(10):
            print(threading.current_thread().getName())


x = MyMessenger(name='Send out messages')
y = MyMessenger(name='Receive Messages')

x.start()
y.start()
