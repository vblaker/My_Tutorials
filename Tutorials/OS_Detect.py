import platform
import os
import sys

print(os.__file__)


# import antigravity


# Retrieves OS information
def os_detect(debug=0):
    if sys.platform.startswith('linux'):
        os_name = 'Linux'
        python_version = sys.version.split('\n')
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
        python_version = platform.python_build()[0]
        if debug != 0:
            print('Detected OS is {}'.format(os_name))
            print('Python release: {}'.format(platform.python_build()))
    else:
        print("Unknown OS")
        os_name = 'Unknown'
        python_version = 'Unknown'

    if debug != 0:
        print(os_name)

    platform_architecture = platform.architecture()
    return os_name, python_version, platform_architecture


def get_curr_directory():
    print(os.getcwd())
    curr_dir = str(os.getcwd())
    return curr_dir


for dirpath, dirnames, filemanes in os.walk('.'):
    print('Current path: ', dirpath)
    print('Directories: ', dirnames)
    print('Files: ', filemanes)

if __name__ == '__main__':
    os_name, python_version, platform_architecture = os_detect(debug=1)
    print(python_version, os_name, platform_architecture)
    curr_dir = get_curr_directory()
    print('Current dir is {}'.format(curr_dir))
    pass
