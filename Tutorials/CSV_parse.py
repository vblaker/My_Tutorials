import platform
import sys
import os
import csv


def IdentifyColumnHeaders(RowString):
#Time (s),VBUS Voltage (V),VBUS Current (A),VCONN Voltage (V),VCONN Current (A),CC1 Voltage (V),CC1 Current (A),CC2 Voltage (V),CC2 Current (A)
    headers_list = ['Time (s)', 'VBUS Voltage (V)', 'VBUS Current (A)', 'VCONN Voltage (V)',
                    'VCONN Current (A)', 'CC1 Voltage (V)', 'CC1 Current (A)', 'CC2 Voltage (V)',
                    'CC2 Current (A)']

    try:
        for header in headers_list:
            time_stamp_idx = row.index(header)
            vbus_vols_idx = row.index('VBUS Voltage (V)')
            vbus_amps_idx = row.index('VBUS Current (A)')
            vconn_volts_idx = row.index('VCONN Voltage (V)')

    except ValueError:
        print('header Parsing Error')

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
    readCSV = csv.reader(csvfile, delimiter=',')

    Time_stamp = []
    VBUS_vols = []
    VBUS_curr = []
    VCONN_volt = []
    VCONN_curr = []
    CC1_volt = []
    CC1_curr = []
    CC2_volt = []
    CC2_curr = []

    i = 0
    for row in readCSV:
        #print(row)

        try:
            if any('VBUS') in row:
                IdentifyColumnHeaders(row)


            f = float(row[0])
            #print(f)
            Time_stamp.append(float(row[0]))
            VBUS_vols.append(float(row[1]))
            VBUS_curr.append(float(row[2]))
            VCONN_volt.append(float(row[3]))
            VCONN_curr.append(float(row[4]))
            CC1_volt.append(float(row[5]))
            CC1_curr.append(float(row[6]))
            CC2_volt.append(float(row[7]))
            CC2_curr.append(float(row[8]))
            i += 1
        except ValueError:
            print('Skipping row {}'.format(row))


print('The size of data is {} rows'.format(i))
print('Time Stamps:{}'.format(Time_stamp))
print('VBUS MAX Voltage: {}'.format(max(VBUS_vols)))
print('VBUS Voltages:{}'.format(VBUS_vols))