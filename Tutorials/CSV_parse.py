import platform
import sys
import os
import csv


if (platform.system() == "Linux"):
    #os_system = str(os.system("uname -a")).split(' ')
    print(os.system("uname -a"))
    print(sys.version)

    print("""Python version: %s
    system: %s
    machine: %s
    platform: %s
    uname: %s
    version: %s
    mac_ver: %s
    """ % (
        sys.version.split('\n'),
        platform.system(),
        platform.machine(),
        platform.platform(),
        platform.uname(),
        platform.version(),
        platform.mac_ver(),
    ))

elif (platform.system() == "Windows"):
    #os_system = str(os.system("uname -a")).split(' ')
    #print("Detected OS is %s" % platform.system())
    print('Detected OS is {}'.format(platform.system()))
    print('Python release: {}'.format(platform.python_build()))
    print(platform.uname())

else:
    print("unknown OS")