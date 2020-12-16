import webbrowser
import time
import os


def print_while_sleep(sleep_seconds):
    for i in range(0, sleep_seconds):
        print(".")
        time.sleep(1)
    return 1


for i in range(2):
    print("Entered loop # %d" % i)
    print("Current time is %s" % time.ctime())
    print_while_sleep(5)
    webbrowser.open("https://www.youtube.com/watch?v=HBxCHonP6Ro&list=PL6gx4Cwl9DGAcbMi1sH6oAMk4JHw91mC_")
    print_while_sleep(5)
