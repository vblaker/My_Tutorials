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


#PD Data Center SW

# open(u'C:/Users/ra7621/Downloads/9V charging from Anker PD charger.tdc', True)        # Open File
# export_iv(u'C:/Users/ra7621/Downloads/export.csv', {'session_id': 1L}, True)          # Export to CSV file

with open('export.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=' ')

    Time_stamp = []
    VBUS_vols = []
    VBUS_curr = []
    VCONN_volt = []
    VCONN_curr = []
    CC1_volt = []
    CC1_curr = []
    CC2_volt = []
    CC2_curr = []

    for row in readCSV:
        print(row)
        Time_stamp.append(row[0])
        VBUS_vols.append(row[1])
        #print(VBUS_vols)