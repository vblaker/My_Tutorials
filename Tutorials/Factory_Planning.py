import random
import statistics
import math
import sys


def genGaussian(tests, testNum):
    values = tests[testNum]
    mu = statistics.mean(values)
    sigma = statistics.stdev(values, mu)
    x = random.gauss(mu, sigma)
    return x


def doOneProgram(tests, numTests):
    test = 0
    builds = buildArray(40)
    while test < numTests:
        build = genGaussian(tests, test)
        buildNo = int(math.floor(build))
        if buildNo > 0:
            builds[buildNo] += 1
            test += 1
    return builds


if __name__ == '__main__':
    try:
        type = sys.argv[1]
        testsInBuild = int(sys.argv[2])
        iterations = int(sys.argv[3])
    except:
        print("ERROR: MonteCarlo [SW|TI|TC] testsInBuild iterations")
        sys.exit(1)

    if type == 'SW':
        tests = SWtests
    elif type == 'TI':
        tests = TItests
    elif type == 'TC':
        tests = TCtests
    counter = 0

    totBuilds = buildArray(40)
    while counter < iterations:
        tmpB = doOneProgram(tests, testsInBuild)
        totBuilds = addArrays(totBuilds, tmpB)
        counter += 1
    build = 1
    while build < (len(totBuilds)-1):
        print("Build %d: %d" % (build, int(round(float(totBuilds[build])/float(iterations), 0))))
        build += 1
        if totBuilds[build] == 0:
            break