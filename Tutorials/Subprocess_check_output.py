import os
from subprocess import check_output, CalledProcessError

try:
    dir_output = check_output(["dir"])
    dir_str_list = (dir_output.split('\r\n'))
    print(dir_str_list)
    print(dir_str_list[1].split('\t'))
    print(dir_output)

except CalledProcessError as e:
    print(e.returncode)
    print(e)