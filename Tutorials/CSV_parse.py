import platform
import sys
import os
import csv


def identify_column_headers(header_row):

    header_list = ['Time (s)', 'VBUS Voltage (V)', 'VBUS Current (A)', 'VCONN Voltage (V)',
                    'VCONN Current (A)', 'CC1 Voltage (V)', 'CC1 Current (A)', 'CC2 Voltage (V)',
                    'CC2 Current (A)']
    header_dict = {}
    try:
        for k in range(0, len(header_row)):
            header_dict[header_list[k]] = header_row.index(header_list[k])
    except ValueError:
            print('header Parsing Error')

    print(header_dict)
    return header_dict


if platform.system() == 'Linux':
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

elif platform.system() == "Windows":
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
    VBUS_volts = []
    VBUS_curr = []
    VCONN_volts = []
    VCONN_curr = []
    CC1_volts = []
    CC1_curr = []
    CC2_volts = []
    CC2_curr = []

    col_header_dict = {}

    for row in readCSV:
        print(row)

        try:
            if row[0] == 'Time (s)':
                # Identify all the Column Headers
                col_header_dict = identify_column_headers(row)

            f = float(row[0])
            #print(f)

            for key, value in col_header_dict.items():
                Time_stamp.append(float(row[col_header_dict['Time (s)']]))
                VBUS_volts.append(float(row[col_header_dict['VBUS Voltage (V)']]))
                VBUS_curr.append(float(row[col_header_dict['VBUS Current (A)']]))
                VCONN_volts.append(float(row[col_header_dict['VCONN Voltage (V)']]))
                VCONN_curr.append(float(row[col_header_dict['VCONN Current (A)']]))
                CC1_volts.append(float(row[col_header_dict['CC1 Voltage (V)']]))
                CC1_curr.append(float(row[col_header_dict['CC1 Current (A)']]))
                CC2_volts.append(float(row[col_header_dict['CC2 Voltage (V)']]))
                CC2_curr.append(float(row[col_header_dict['CC2 Current (A)']]))

        except ValueError:
            print('Skipping row {}'.format(row))


print('The size of data is {}'.format(len(Time_stamp)))
print('VBUS MAX Voltage: {}'.format(max(VBUS_volts)))