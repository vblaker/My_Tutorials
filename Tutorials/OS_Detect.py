import platform
import os
import sys

#Retrieves OS information
def os_detect(debug=0):


    if sys.platform.startswith('linux'):
        os_name = 'Linux'

        if debug != 0:
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

    elif sys.platform.startswith('win'):
        os_name = 'Windows'
        if debug != 0:
            print('Detected OS is {}'.format(os_name))
            print('Python release: {}'.format(platform.python_build()))

    else:
        print("Unknown OS")

    if debug != 0:
        print(os_name)

    return os_name

os_detect(debug=1)