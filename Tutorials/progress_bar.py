from __future__ import print_function
import time

# status generator
def range_with_status(total):
    """ iterate from 0 to total and show progress in console """
    n=0
    while n < total:
        done = '#'*(n+1)
        todo = '-'*(total-n-1)
        s = '<{0}>'.format(done+todo)
        if not todo:
            s+='\n'
        if n > 0:
            s = '\r'+s
        print(s, end='')
        yield n
        n+=1

# example for use of status generator
for i in range_with_status(10):
    time.sleep(0.1)



from time import sleep
import sys

for i in range(21):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-20s] %d%%" % ('#'*i, 5*i))
    sys.stdout.flush()
    sleep(0.25)


class Printer:
    """
    Print things to stdout on one line dynamically
    """

    def __init__(self, data):
        sys.stdout.write("\r\x1b[K" + data.__str__())
        sys.stdout.flush()


fileList = [i for i in range(100)]
totalFiles = len(fileList)
currentFileNum = 1.0

for f in fileList:
    #ProcessFile(f)
    currentPercent = currentFileNum / totalFiles * 100
    output = "%.2f of %d completed." % (currentPercent, totalFiles)
    Printer(output)
    time.sleep(0.1)
    currentFileNum += 1
