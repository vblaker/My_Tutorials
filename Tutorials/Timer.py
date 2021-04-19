# timer.py

import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self, text="Elapsed time: {:0.4f} seconds"):
        self._start_time = None
        self.text = text

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(self.text.format(elapsed_time))


def main():
    t = Timer(text="You waited {:.1f} seconds")
    # t.start()
    # print('Hello World, sleeping 3 seconds')
    # time.sleep(3)
    # t.stop()
    with Timer('Vad1 timer is {}'):
        time.sleep(5)


if __name__ == "__main__":
    main()
