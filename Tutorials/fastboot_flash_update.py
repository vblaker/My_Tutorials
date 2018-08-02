from __future__ import print_function
__author__ = 'Vadim Blaker'
__copyright__ = 'Verifone 2018'
__version__ = '0.0.0'
__email__ = 'VadimB1@verifone.com'
__status__ = 'Pre-production'


import os
import logging
import time
import fnmatch
import threading
import subprocess
import sys
from xml.dom import minidom
import argparse


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


class Error:
    def __init__(self, error_code=1, error_string='Failed', error_flag=True):
        self.error_code = error_code
        self.error_string = error_string
        self.error_flag = error_flag

    def set_pass(self):
        self.error_code = 0
        self.error_flag = False
        self.error_string = ''
        return self.error_code, self.error_string, self.error_flag

    def set_fail(self, error_message):
        self.error_code = 1
        self.error_flag = True
        self.error_string = error_message
        return self.error_code, self.error_string, self.error_flag


def read_flash_image_filenames(filepath, product, debug=0):
    err = Error()
    err.set_pass()

    try:
        # Recursive search for files matching patterns
        def find(pattern, filepath):
            result = []
            for root, dirs, files in os.walk(filepath):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        result.append(os.path.join(root, name))
            if len(result) == 0:
                err.set_fail('File {} not found'.format(pattern))
                print('ERROR: File {} not found'.format(pattern))
                result = []
            return result

        # Get the first occurrence on the returned results list

        # Find bootloader
        pattern = product + '*bootloader'
        tmp_list = find(pattern, filepath)
        if tmp_list == []:
            err.set_fail('Could not find bootloader')
            raise IOError
        else:
            bootloader = tmp_list[0]

        # Find efi loader
        # pattern = product.replace('_', '') + '*loader.efi'
        # tmp_list = find(pattern, filepath)
        # if tmp_list == []:
        #     err.set_fail('Could not find {}'.format(pattern))
        #     raise IOError
        # else:
        #     efi_bootloader = tmp_list[0]
        efi_bootloader = ''

        # Find AOS image
        pattern = product + '*.zip'
        tmp_list = find(pattern, filepath)
        if tmp_list == []:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            flash_image = tmp_list[0]

        # Find XML config file
        pattern = '*cfg.xml'
        tmp_list = find(pattern, filepath)
        if tmp_list == []:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            sequencer_xml = tmp_list[0]

        # Check if all the images are there
        if debug == 1:
            logging.debug(efi_bootloader)
            logging.debug(bootloader)
            logging.debug(flash_image)
            err.set_pass()

        # Raise an exception and pass the error message
        if err.error_flag is True:
            raise IOError

    except IOError as e:
        logging.debug(e)
        err.set_fail(err.error_string)
        efi_bootloader = ''
        bootloader = ''
        flash_image = ''
        sequencer_xml = ''

    return err, efi_bootloader, bootloader, flash_image, sequencer_xml


def read_sequencer_xml_file(filename, debug=0):
    err = Error()
    sequencer_list = []
    try:
        xmldoc = minidom.parse(filename)
        itemlist = xmldoc.getElementsByTagName('item')
        for item in itemlist:
            sequencer_list.append(str(item.attributes['name'].value))
        if debug == 1:
            logging.debug('Loaded sequencer from XML file: {}'.format(sequencer_list))

        # Build error reporting
        err.set_pass()

    except IOError:
        if debug == 1:
            logging.debug('Cannot open file ' + filename + ' for reading')
        # Build error reporting
        err.set_fail('Cannot open file ' + filename + ' for reading')

    return err, sequencer_list


def get_fastboot_devices(debug=0):
    err = Error()

    try:
        output = subprocess.check_output(["fastboot", "devices"])
        fastboot_output = output.replace('\tfastboot', '').strip()
        if len(fastboot_output) == 0:
            raise IOError('No fastboot devices connected!')

        fastboot_devices_list = (fastboot_output.split('\r\n'))
        if debug == 1:
            logging.debug('{} detected devices: {}'.format(len(fastboot_devices_list), fastboot_devices_list))
        err.set_pass()

    except IOError:
        # Build error reporting
        err.set_fail('No fastboot devices detected')
        fastboot_devices_list = []

    return err, fastboot_devices_list


def get_adb_devices(debug=0):
        err = Error()

        try:
            adb_devices_raw_list = os.popen("adb devices").readlines()
            if len(adb_devices_raw_list) <= 2:
                raise IOError('No adb devices connected!')

            adb_devices_list = []
            i = 0
            # Split strings
            for device in adb_devices_raw_list:
                adb_devices_list.append(device.split()[0])
                i += 1

            if debug == 1:
                logging.debug('Detected devices:', adb_devices_list)
                print('{} devices detected: {}'.format(len(adb_devices_list), adb_devices_list))

            err.set_pass()

        except IOError as e:
            if debug == 1:
                print('Failed to get adb devices!\n {}'.format(e.args))
            err.set_fail('No adb devices detected!')
            adb_devices_list = []

        return err, adb_devices_list


def fastboot_reboot_bootloader(fastboot_device, time_out=60, debug=0):
    err = Error()
    try:
        cmd = 'fastboot -s ' + fastboot_device + ' reboot-bootloader'
        response = os.popen(cmd).readlines()
        if debug == 1:
            logging.debug('Rebooting {} to bootloader'.format(fastboot_device))

        i = 0
        result = []
        while i < time_out and (fastboot_device not in result):
            err, result = get_fastboot_devices()
            time.sleep(1)
            i += 1

        if i >= time_out:
            print('Device {} reboot to bootloader timed out, exiting...'.format(fastboot_device))
        else:
            if debug == 1:
                logging.debug('Device {} rebooted in {} seconds'.format(fastboot_device, i))

        if len(response) != 0:
            raise IOError('Fastboot reboot-bootloader error!')

        # Set passing flag to be returned by the function
        err.set_pass()

    except IOError:
        print('Fastboot reboot-bootloader error for device {}'.format(fastboot_device))
        # Build error reporting
        err.set_fail('Failed to reboot bootloader')

    return err


def fastboot_reboot_to_idle(fastboot_device, time_out=60, debug=0):
    err = Error()
    try:
        cmd = ["fastboot", "-s", fastboot_device, "reboot"]
        if debug == 1:
            logging.debug('Rebooting {} fastboot device to idle...'.format(fastboot_device))

        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        i = 0
        status = None
        while i < time_out and status is None:
            status = process.poll()
            time.sleep(1)
            i += 1

        stdout, stderr = process.communicate()

        # Check if command errored out
        if ("Finished" in stderr) and ("Rebooting" in stderr):
            if debug == 1:
                logging.debug('Device {} rebooting to idle'.format(fastboot_device))
            # print('Exit status: {} (0 = PASS)'.format(status))
        else:
            print('Exit status: {} (FAILED)'.format(status))
            raise IOError

        # Set passing flag to be returned by the function
        err.set_pass()

    except IOError:
        err.set_fail('Device {} failed reboot to idle'.format(fastboot_device))
        logging.debug('Device {} failed reboot to idle'.format(fastboot_device))

    return err


def fastboot_flash_bootloader(fastboot_device, bootloader, time_out=60, debug=0):
    err = Error()
    err.set_pass()
    try:
        cmd = ["fastboot", "-s", fastboot_device, "flash", "bootloader", bootloader]
        logging.debug('Flashing {} bootloader image into fastboot device {}'.format(bootloader, fastboot_device))

        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        i = 0
        status = None
        while i < time_out and status is None:
            status = process.poll()
            time.sleep(1)
            i += 1

        stdout, stderr = process.communicate()
        # print('Exit status {} (0 = SUCCESS)'.format(status))

        if debug == 1:
            logging.debug('Completed device {} bootloader flash in {} seconds'.format(fastboot_device, i))

        if i > time_out:
            print('Flashing device {} timed out'.format(fastboot_device))
            err.set_fail('Flashing device {} timed out'.format(fastboot_device))
            logging.debug('Flashing device {} timed out'.format(fastboot_device))
            raise IOError

        if "Finished" not in stderr or status is not 0:
            print('Flashing device {} was not completed successfully'.format(fastboot_device))
            err.set_fail('Flashing device {} was not completed successfully, returned status  '
                         '= {}'.format(fastboot_device, status))
            logging.debug('Flashing device {} was not completed successfully'.format(fastboot_device))
            raise IOError

        print('Completed device {} flash in {} seconds'.format(fastboot_device, i))

        if debug == 1:
            logging.debug(stderr)

    except IOError:
        logging.debug('Fastboot error for device {}'.format(fastboot_device))

    return err


def fastboot_flash_aos_image(fastboot_device, flash_image, debug=0):
    time_out = 120
    err = Error()
    err.set_pass()

    try:
        cmd = ["fastboot", "-s", fastboot_device, "update", flash_image, "--skip-reboot"]
        logging.debug('Flashing {} image into fastboot device {}'.format(flash_image, fastboot_device))

        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        i = 0
        status = None
        while i < time_out and status is None:
            # Print progress bar
            sys.stdout.write('\r')
            # the exact output you're looking for:
            print("[%-20s] %.2f%%" % ('#' * i, i * 100 / 85), end=''),
            sys.stdout.flush()

            status = process.poll()
            time.sleep(1)
            i += 1

        stdout, stderr = process.communicate()
        #print('Exit status {} (0 = SUCCESS)'.format(status))

        if debug == 1:
            logging.debug('Completed device {} flash in {} seconds'.format(fastboot_device, i))

        if i > time_out:
            print('Flashing device {} timed out'.format(fastboot_device))
            err.set_fail('Flashing device {} timed out'.format(fastboot_device))
            logging.debug('Flashing device {} timed out'.format(fastboot_device))
            raise IOError

        if "Finished" not in stderr or status != 0:
            print('Flashing device {} was not completed successfully'.format(fastboot_device))
            err.set_fail('Flashing device {} was not completed successfully, returned status  '
                         '= {}'.format(fastboot_device, status))
            logging.debug('Flashing device {} was not completed successfully'.format(fastboot_device))
            raise IOError

        print('Completed device {} flash in {} seconds'.format(fastboot_device, i))

        if debug == 1:
            logging.debug(stderr)

    except IOError:
        logging.debug('Fastboot error for device {}'.format(fastboot_device))

    return err


def fastboot_erase_userdata(fastboot_device, time_out=60, debug=0):
    err = Error()
    try:

        # Erase userdata
        cmd = ["fastboot", "-s", fastboot_device, "erase", "userdata"]
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        logging.debug('Erasing userdata on {} device'.format(fastboot_device))

        i = 0
        result = []
        while i < time_out and ("OKAY" not in response) and (fastboot_device not in result):
            err, result = get_fastboot_devices()
            i += 1

        # Erase cache
        cmd = ["fastboot", "-s", fastboot_device, "erase", "cache"]
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        logging.debug('Erasing cache on {} device'.format(fastboot_device))

        i = 0
        result = []
        while i < time_out and ("OKAY" not in response) and (fastboot_device not in result):
            err, result = get_fastboot_devices()
            i += 1

        if i >= time_out:
            logging.debug('Device {} timed out to erase userdata in {} seconds, exiting...'.format(fastboot_device, i))
            raise IOError('Fastboot erase userdata timeout error!')
        elif len(response) == 0:
            if debug == 1:
                logging.debug('No response returned from the {} device'.format(fastboot_device))
                raise IOError('Fastboot erase userdata error!')
        else:
            err.set_pass()
            if debug == 1:
                logging.debug('Erased {} device in {} seconds'.format(fastboot_device, i))

    except IOError as e:
        logging.debug(e.args)
        logging.debug('Fastboot userdata erase error for device {}'.format(fastboot_device))
        # Build error reporting
        err.set_fail('Failed to erase userdata')

    return err


def update_worker(fastboot_device, product, error_dict, debug=0):
    """thread update worker function"""

    err = Error()

    if (product != 'Carbon_8') and (product != 'Carbon_10'):
        err.set_fail('Unknown product, exiting...')
        logging.debug('Unknown product {}, exiting...'.format(product))
        exit()
    else:
        err.set_pass()

    file_path = os.getcwd()
    err, efi_bootloader, bootloader, flash_image, sequencer_xml = read_flash_image_filenames(file_path, product, debug=debug)

    if err.error_flag:
        error_dict[fastboot_device] = err
        # raise IOError
        exit()      # Exit if required flash image is missing

    # Retrieve sequence of functions to execute
    err, sequencer_list = read_sequencer_xml_file(sequencer_xml)

    try:
        i = 0
        while i < len(sequencer_list) and err.error_flag is not True:
            if sequencer_list[i] == 'fastboot_reboot_bootloader':
                if debug == 1:
                    logging.debug('Envoking fastboot_reboot_bootloader')
                err = fastboot_reboot_bootloader(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_reboot_to_idle':
                if debug == 1:
                    logging.debug('Envoking fastboot_reboot_to_idle')
                err = fastboot_reboot_to_idle(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_bootloader':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_bootloader')
                err = fastboot_flash_bootloader(fastboot_device, bootloader, debug=debug)
            elif sequencer_list[i] == 'get_fastboot_devices':
                if debug == 1:
                    logging.debug('Envoking get_fastboot_devices')
                err = fastboot_reboot_bootloader(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_erase_userdata':
                if debug == 1:
                    logging.debug('Envoking fastboot_erase_userdata')
                err = fastboot_erase_userdata(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_aos_image':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_aos_image')
                err = fastboot_flash_aos_image(fastboot_device, flash_image, debug=debug)

            else:
                logging.debug('Unknown function call {}'.format(sequencer_list[i]))
                exit()

            if err.error_flag:
                raise IOError

            i += 1

    except IOError as e:
        logging.debug('Error message: {}'.format(err.error_string))
        logging.debug('Unexpected exception in the thread - exiting... \n{}'.format(e.args))
        error_dict[fastboot_device] = err


def fastboot_getvar(fastboot_device, param):

    err = Error()

    param_dict = {}
    try:
        cmd = ["fastboot", "-s", fastboot_device, "getvar", param]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).split('\r\n')
        param_list = output[0].replace(' ', '').split(':')
        param_dict[param_list[0]] = param_list[1]

        if len(param_list) == 0:
            raise IOError('No fastboot devices connected!')
        err.set_pass()

    except Exception as e:
        param_dict = {}
        logging.debug('Failed to get fastboot properties\s {}'.format(e.args))
        err.set_fail('Failed to get fastboot properties')

    return err, param_dict


def get_fastboot_dev_params(devices, param_list):
    fastboot_dev_dict = dict()
    for device in devices:

        # Execute first read to populate fastboot_dev_dict with first value
        err, temp = fastboot_getvar(device, param_list[0])
        fastboot_dev_dict[device] = temp

        # Iterate through the rest of the list starting with elem[1]
        for i in range(1, len(param_list)):
            err, temp = fastboot_getvar(device, param_list[i])
            fastboot_dev_dict[device].update(temp)
            i += 1
    return fastboot_dev_dict


def main():
    err = Error()
    err.set_pass()

    # Set debug parameter from the command prompt
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", type=int, default=0, help="set debug level: \"-d 0\" for NONE, \"-d 1\" for enhanced")
    args = parser.parse_args()

    if args.debug == 0:
        debug = 0
    else:
        debug = 1
        if args.debug is not 1:
            logging.debug('Unsupported debug level {}, defaulting to 1'.format(args.debug))
        else:
            logging.debug("The debug level is set to {}".format(debug))

    # Set fastboot parameter list to be extracted
    param_list = ['product', 'battery-capacity', 'battery-voltage', 'version-bootloader']

    try:
        # Get all connected fastboot devices
        err, devices = get_fastboot_devices(debug=debug)

        # Initialize error cluster to be returned from the worker function
        error_dict = {device: err for device in devices}

        # Get fastboot device parameters before flash
        fastboot_dev_dict = get_fastboot_dev_params(devices, param_list)

        if err.error_flag is True:
            raise IOError

        print('PRE_FLASH Detected fastboot devices: {}'.format(fastboot_dev_dict))

        # Spawn a worker update thread for every connected fastboot device
        threads = []
        for device in fastboot_dev_dict:
            product = fastboot_dev_dict[device]['product'].replace(' ', '')
            t = threading.Thread(name=device, target=update_worker, args=[device, product, error_dict, debug])
            threads.append(t)
            t.start()
            if debug == 1:
                logging.debug('Starting thread for serial number {}'.format(device))

        # Join threads  - determine if needed in this case
        for thread in threads:
            thread.join()

        if debug == 1:
            print(error_dict)

        # Get fastboot device parameters AFTER flash
        fastboot_dev_dict = get_fastboot_dev_params(devices, param_list)
        print('POST_FLASH Detected fastboot devices: {}'.format(fastboot_dev_dict))

        # Reboot to idle all the devices that flashed successfully
        for device in error_dict:
            if not error_dict[device].error_flag:
                if debug == 1:
                    logging.debug('Device {} flashed successfully, rebooting...'.format(device))
                fastboot_dev_dict[device]['fail_flag'] = 'PASS'
                if debug is 1:
                    print('Device {} PASSED'.format(device))
                fastboot_reboot_to_idle(device, debug=debug)
            else:
                fastboot_dev_dict[device]['fail_flag'] = 'FAIL'
                if debug is 1:
                    print('Device {} FAILED'.format(device))

        ############### Generate Final report ###############
        # Print report header
        print('-' * 113)
        print("| {:<2} | {:<16} | {:<12}| {:<18}| {:<18}| {:<23} | {:<4} |"
              .format('Seq', 'Serial Number', 'Product', 'Battery Capacity', 'Battery Voltage', 'Bootloader Version',
                      'P/F'))
        print('-' * 113)

        idx = 1
        k = 0
        for device in fastboot_dev_dict:
            print("|{:<4} | {:<16} | {:<11} | {:<18}| {:<18}| {:<22} | {:<4} |"
                  .format(idx, device,
                          fastboot_dev_dict[device][param_list[0]],
                          fastboot_dev_dict[device][param_list[1]],
                          fastboot_dev_dict[device][param_list[2]],
                          fastboot_dev_dict[device][param_list[3]],
                          fastboot_dev_dict[device]['fail_flag']))
            idx += 1
        print('-' * 113)
        ######################################################

    except IOError:
        logging.debug('{}'.format(err.error_string))


if __name__ == "__main__":
    main()
