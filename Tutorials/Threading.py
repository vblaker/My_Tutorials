import threading
import time


def timer(name, delay, repeat):
    print('Timer:' + name + ' Starting')
    while repeat > 0:
        time.sleep(delay)
        print(name + ': ' + str(time.ctime(time.time())))
        repeat -= 1
    print('Timer: ' + name + ' Completed')


def main():
    t1 = threading.Thread(target=timer, args=('Timer1', 1, 5))
    t2 = threading.Thread(target=timer, args=('Timer2', 1, 5))
    t1.start()
    t2.start()

    # t1.join()
    # t2.join()

    print('Main complete')


if __name__ == '__main__':
    main()

"""
class MyMessenger(threading.Thread):
    def run(self):
        for _ in range(10):
            print(threading.current_thread().getName())


x = MyMessenger(name='Send out messages')
y = MyMessenger(name='Receive Messages')

x.start()
y.start()

"""