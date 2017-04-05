import os
import string

file_list = os.listdir(r".")
print("Current Path is %s" % os.getcwd())
print(file_list)
print("There are %d files in this directory" % len(file_list))

for file_name in file_list:
    os.renames(file_name, file_name.translate("0123456789"))