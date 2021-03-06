from __future__ import print_function
__author__ = 'Vadim Blaker'
__copyright__ = 'Verifone 2019, All rights reserved'
__version__ = '1.0.0'
__email__ = 'VadimB1@verifone.com'
__status__ = 'Pre-production'

import os
from sys import exit
from sys import argv
import logging
import time
import datetime
import fnmatch
import threading
import subprocess
import sys
from xml.dom import minidom
import argparse
import tarfile
import zipfile


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


class Error:
    # New ERROR class to pass error messages through execution flow
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
    image_dict = {}

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

        # Find bootloader
        pattern = product + '*bootloader'
        tmp_list = find(pattern, filepath)
        if not tmp_list:
            err.set_fail('Could not find bootloader')
            raise IOError
        else:
            bootloader = tmp_list[0]
            image_dict['bootloader'] = bootloader

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
        tmp_list = find(pattern, os.path.dirname(bootloader))
        if tmp_list is []:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            flash_image = tmp_list[0]
            image_dict['flash_image'] = flash_image

        # Find recovery image
        pattern = 'recovery.img'
        tmp_list = find(pattern, os.path.dirname(bootloader))
        if tmp_list is []:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            recovery_image = tmp_list[0]
            image_dict['recovery_image'] = recovery_image

        # Find cache image
        pattern = 'cache.img'
        tmp_list = find(pattern, os.path.dirname(bootloader))
        if tmp_list is []:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            cache_image = tmp_list[0]
            image_dict['cache_image'] = cache_image

        # Find boot image
        pattern = 'boot.img'
        tmp_list = find(pattern, os.path.dirname(bootloader))
        if not tmp_list:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            boot_image = tmp_list[0]
            image_dict['boot_image'] = boot_image

        # Find system image
        pattern = 'system.img'
        tmp_list = find(pattern, os.path.dirname(bootloader))
        if tmp_list is []:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            system_image = tmp_list[0]
            image_dict['system_image'] = system_image

        # Find XML config file
        pattern = '*cfg.xml'
        tmp_list = find(pattern, filepath)
        if tmp_list is []:
            err.set_fail('Could not find {}'.format(pattern))
            raise IOError
        else:
            sequencer_xml = tmp_list[0]
            image_dict['sequencer_xml'] = sequencer_xml

        # Check if all the images are there
        if debug == 1:
            logging.debug(efi_bootloader)

            logging.debug(bootloader)
            write_to_datalog(bootloader)

            logging.debug(flash_image)
            write_to_datalog(flash_image)

            logging.debug(recovery_image)
            write_to_datalog(recovery_image)

            logging.debug(cache_image)
            write_to_datalog(cache_image)

            logging.debug(boot_image)
            write_to_datalog(boot_image)

            logging.debug(system_image)
            write_to_datalog(system_image)

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
        recovery_image = ''
        cache_image = ''
        boot_image = ''
        system_image = ''

    return err, efi_bootloader, bootloader, flash_image, sequencer_xml, recovery_image, cache_image, boot_image, system_image


def read_sequencer_xml_file(filename, debug=0):
    # Build error reporting
    err = Error()
    err.set_pass()

    sequencer_list = []
    try:
        xmldoc = minidom.parse(filename)
        itemlist = xmldoc.getElementsByTagName('item')
        for item in itemlist:
            sequencer_list.append(str(item.attributes['name'].value))
        if debug == 1:
            logging.debug('Loaded sequencer from XML file: {}'.format(sequencer_list))
            write_to_datalog('Loaded sequencer from XML file: {}'.format(sequencer_list))

    except IOError:
        if debug == 1:
            logging.debug('Cannot open file ' + filename + ' for reading')
            write_to_datalog('Cannot open file ' + filename + ' for reading')
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
            write_to_datalog('{} detected devices: {}'.format(len(fastboot_devices_list), fastboot_devices_list))
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
                write_to_datalog('{} devices detected: {}'.format(len(adb_devices_list), adb_devices_list))

            err.set_pass()

        except IOError as e:
            if debug == 1:
                print('Failed to get adb devices!\n {}'.format(e.args))
                write_to_datalog('Failed to get adb devices!\n {}'.format(e.args))
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
            write_to_datalog('Rebooting {} to bootloader'.format(fastboot_device))

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
                write_to_datalog('Device {} rebooted in {} seconds'.format(fastboot_device, i))

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
            write_to_datalog('Rebooting {} fastboot device to idle...'.format(fastboot_device))

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
                write_to_datalog(stderr)
                logging.debug('Device {} rebooting to idle'.format(fastboot_device))
                write_to_datalog('Device {} rebooting to idle'.format(fastboot_device))

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
            write_to_datalog('Completed device {} bootloader flash in {} seconds'.format(fastboot_device, i))

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
            write_to_datalog(stderr)

    except IOError:
        logging.debug('Fastboot error for device {}'.format(fastboot_device))
        write_to_datalog('Fastboot error for device {}'.format(fastboot_device))

    return err


def fastboot_flash_update_aos_image(fastboot_device, flash_image, debug=0):
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
            write_to_datalog('Completed device {} flash in {} seconds'.format(fastboot_device, i))

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
            write_to_datalog('Flashing device {} was not completed successfully'.format(fastboot_device))

            raise IOError

        print('Completed device {} flash in {} seconds'.format(fastboot_device, i))

        if debug == 1:
            logging.debug(stderr)
            write_to_datalog(stderr)

    except IOError:
        logging.debug('Fastboot error for device {}'.format(fastboot_device))
        write_to_datalog('Fastboot error for device {}'.format(fastboot_device))

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
                write_to_datalog('No response returned from the {} device'.format(fastboot_device))
                raise IOError('Fastboot erase userdata error!')
        else:
            err.set_pass()
            if debug == 1:
                logging.debug('Erased {} device in {} seconds'.format(fastboot_device, i))
                write_to_datalog(response)
                write_to_datalog('Erased {} device in {} seconds'.format(fastboot_device, i))

    except IOError as e:
        logging.debug(e.args)
        logging.debug('Fastboot userdata erase error for device {}'.format(fastboot_device))
        # Build error reporting
        err.set_fail('Failed to erase userdata')

    return err


def fastboot_flash_partition(fastboot_device, partition_image, partition, time_out=120, debug=0):
    err = Error()
    err.set_pass()

    if partition == 'system':
        time_to_flash = 80
        poll_interval = 1
    else:
        time_to_flash = 1
        poll_interval = 1
    try:
        cmd = ["fastboot", "-s", fastboot_device, "flash", partition, partition_image]
        logging.debug('Flashing {} image into fastboot device {}'.format(partition_image, fastboot_device))

        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        i = 0
        status = None
        while i < time_out / poll_interval and status is None:
            # Print progress bar
            sys.stdout.write('\r')
            # the exact output you're looking for:
            print("[%-20s] %.2f%%" % ('#' * i, i * poll_interval * 100 / time_to_flash), end=''),
            sys.stdout.flush()

            status = process.poll()
            time.sleep(poll_interval)
            i += 1

        stdout, stderr = process.communicate()
        # print('Exit status {} (0 = SUCCESS)'.format(status))

        if debug == 1:
            logging.debug('Completed device {} flash in {} seconds'.format(fastboot_device, i*poll_interval))
            write_to_datalog('Completed device {} flash in {} seconds'.format(fastboot_device, i*poll_interval))

        if i > time_out / poll_interval:
            print('Flashing device {} timed out'.format(fastboot_device))
            err.set_fail('Flashing device {} timed out'.format(fastboot_device))
            logging.debug('Flashing device {} timed out'.format(fastboot_device))
            write_to_datalog('Flashing device {} timed out'.format(fastboot_device))
            raise IOError

        if "Finished" not in stderr or "OKAY" not in stderr or status != 0:
            print('Flashing device {} was not completed successfully'.format(fastboot_device))
            err.set_fail('Flashing device {} was not completed successfully, returned status  '
                         '= {}'.format(fastboot_device, status))
            logging.debug('Flashing device {} was not completed successfully'.format(fastboot_device))
            write_to_datalog('Flashing device {} was not completed successfully'.format(fastboot_device))
            raise IOError

        print('Completed device {} flash in {} seconds'.format(fastboot_device, i * poll_interval))

        if debug == 1:
            logging.debug(stderr)
            write_to_datalog(stderr)

    except IOError:
        logging.debug('Fastboot error for device {}'.format(fastboot_device))
        write_to_datalog('Fastboot error for device {}'.format(fastboot_device))
    return err


def update_worker(fastboot_device, product, error_dict, debug=0):
    """thread update worker function"""

    err = Error()
    if product == 'MSM8909_CARBON_E500':
        product = 'Carbon_CM5'

    if (product != 'Carbon_8') and (product != 'Carbon_10') and (product != 'Carbon_CM5'):
        err.set_fail('Unknown product, exiting...')
        logging.debug('Unknown product {}, exiting...'.format(product))
        raise IOError

    else:
        err.set_pass()

    file_path = os.getcwd()
    err, efi_bootloader, bootloader, flash_image, sequencer_xml, recovery_image, cache_image, boot_image, system_image\
        = read_flash_image_filenames(file_path, product, debug=debug)

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
                    write_to_datalog('Envoking fastboot_reboot_bootloader')
                err = fastboot_reboot_bootloader(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_reboot_to_idle':
                if debug == 1:
                    logging.debug('Envoking fastboot_reboot_to_idle')
                    write_to_datalog('Envoking fastboot_reboot_to_idle')
                err = fastboot_reboot_to_idle(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_bootloader':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_bootloader')
                    write_to_datalog('Envoking fastboot_flash_bootloader')
                err = fastboot_flash_bootloader(fastboot_device, bootloader, debug=debug)
            elif sequencer_list[i] == 'get_fastboot_devices':
                if debug == 1:
                    logging.debug('Envoking get_fastboot_devices')
                    write_to_datalog('Envoking get_fastboot_devices')
                err = fastboot_reboot_bootloader(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_erase_userdata':
                if debug == 1:
                    logging.debug('Envoking fastboot_erase_userdata')
                    write_to_datalog('Envoking fastboot_erase_userdata')
                err = fastboot_erase_userdata(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_recovery':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_recovery')
                    write_to_datalog('Envoking fastboot_flash_recovery')
                err = fastboot_flash_partition(fastboot_device, recovery_image, partition='recovery', debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_cache':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_cache')
                    write_to_datalog('Envoking fastboot_flash_cache')
                err = fastboot_flash_partition(fastboot_device, cache_image, partition='cache', debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_boot':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_boot')
                    write_to_datalog('Envoking fastboot_flash_boot')
                err = fastboot_flash_partition(fastboot_device, boot_image, partition='boot', debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_system':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_system')
                    write_to_datalog('Envoking fastboot_flash_system')
                err = fastboot_flash_partition(fastboot_device, system_image, partition='system', debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_update_aos_image':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_update_aos_image')
                    write_to_datalog('Envoking fastboot_flash_update_aos_image')
                err = fastboot_flash_update_aos_image(fastboot_device, flash_image, debug=debug)

            else:
                logging.debug('Unknown function call {}'.format(sequencer_list[i]))
                write_to_datalog('Unknown function call {}'.format(sequencer_list[i]))
                exit()

            if err.error_flag:
                raise IOError

            i += 1

    except IOError as e:
        logging.debug('Error message: {}'.format(err.error_string))
        logging.debug('Unexpected exception in the thread {} \nExiting...\n'.format(err.error_string))
        write_to_datalog('Unexpected exception in the thread {} \nExiting...\n'.format(err.error_string))
        error_dict[fastboot_device] = err
        write_to_datalog(error_dict)


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


def unzip_tar_image(flash_image):
    err = Error()
    try:
        tar_ref = tarfile.open(flash_image, 'r')
        untar_path, tar_file = os.path.split(flash_image)
        for item in tar_ref:
            tar_ref.extract(item, untar_path)
            if item.path.endswith('zip'):
                unzip_flash_image(os.path.join(untar_path, item.path))
        err.set_pass()
    except IOError as e:
        err.set_fail('Failed to unzip {} file:'.format(flash_image))
    return err


def unzip_flash_image(flash_image):
    err = Error()
    try:
        zip_ref = zipfile.ZipFile(flash_image, 'r')
        unzip_path, filename = os.path.split(flash_image)
        zip_ref.extractall(unzip_path)
        zip_ref.close()
        err.set_pass()
    except IOError as e:
        err.set_fail('Failed to unzip {} file:'.format(flash_image))
    return err


def write_to_datalog(string):
    with open('datalog.txt', 'a') as datalog_file:
        datalog_file.write(string + '\n')


def main():
    err = Error()
    err.set_pass()

    # Set debug parameter from the command prompt
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="display version of the update utility and exit", action="store_true")
    parser.add_argument("-d", "--debug", help="set debugging output ON", action="store_true")

    # parser.add_argument("-c", "--prod_config", default='c8_10',
    #                   help="product config: \"-c c8_10\" for Carbon 8/10, \"-c cm5\" for CM5")
    args = parser.parse_args()

    start_time = datetime.datetime.now().strftime('%Y-%b-%d %H:%M:%S:%f')

    if args.version:
        print('#'*59, end='\n')
        print('###\t Flash Utility Version:\t{}\t\t\t###'.format(__version__, end='\n'))
        print('### \t {}\t\t###'.format(__copyright__, end='\n'))
        print('###\t Status:\t{}\t\t\t###'.format(__status__, end='\n'))
        print('###\t Author:\t{}\t\t\t###'.format(__author__, end='\n'))
        print('###\t Current Time:\t{}\t###'.format(start_time, end='\n'))
        print('#'*59, end='\n')
        sys.exit(0)

    if args.debug is False:
        debug = 0
    else:
        debug = 1

    logging.debug('\n\n' + '=' * 100)
    logging.debug('The debug level is set to {}'.format(debug))
    if debug == 1:
        write_to_datalog('\n\n' + '=' * 100)
        write_to_datalog('The debug level is set to {}'.format(debug))
        write_to_datalog('#'*59)
        write_to_datalog('###\t Flash Utility Version:\t{}\t\t\t###'.format(__version__, end='\n'))
        write_to_datalog('### \t {}\t\t###'.format(__copyright__, end='\n'))
        write_to_datalog('###\t Status:\t{}\t\t\t###'.format(__status__, end='\n'))
        write_to_datalog('###\t Author:\t{}\t\t\t###'.format(__author__, end='\n'))
        write_to_datalog('###\t Current Time:\t{}\t###'.format(start_time, end='\n'))
        write_to_datalog('#'*59 + '\n')

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
                write_to_datalog('Starting thread for serial number {}'.format(device))

        # Join threads  - determine if needed in this case
        for thread in threads:
            thread.join()

        if debug == 1:
            for item in error_dict:
                print('Device {}: Error Flag: {}, Error String: {}'
                                 .format(item, error_dict[item].error_flag, error_dict[item].error_string))
                write_to_datalog('Device {}: Error Flag: {}, Error String: {}'
                                 .format(item, error_dict[item].error_flag, error_dict[item].error_string))

        # Get fastboot device parameters AFTER flash
        fastboot_dev_dict = get_fastboot_dev_params(devices, param_list)
        print('POST_FLASH Detected fastboot devices: {}'.format(fastboot_dev_dict))

        # Reboot to idle all the devices that flashed successfully
        for device in error_dict:
            if not error_dict[device].error_flag:
                if debug == 1:
                    logging.debug('Device {} flashed successfully, rebooting...'.format(device))
                    write_to_datalog('Device {} flashed successfully, rebooting...'.format(device))
                fastboot_dev_dict[device]['fail_flag'] = 'PASS'
                if debug == 1:
                    print('Device {} PASSED'.format(device))
                    write_to_datalog('Device {} PASSED'.format(device))
                fastboot_reboot_to_idle(device, debug=debug)
            else:
                fastboot_dev_dict[device]['fail_flag'] = 'FAIL'
                if debug == 1:
                    print('Device {} FAILED'.format(device))
                    write_to_datalog('Device {} FAILED'.format(device))

        # Calculate total FLASH time
        end_time = datetime.datetime.now().strftime('%Y-%b-%d %H:%M:%S:%f')
        total_time = (datetime.datetime.strptime(end_time, '%Y-%b-%d %H:%M:%S:%f') -
                      datetime.datetime.strptime(start_time, '%Y-%b-%d %H:%M:%S:%f'))

        if debug == 1:
            write_to_datalog('Total FLASH time is {}'.format(total_time))
            logging.debug('Total FLASH time is {}'.format(total_time))

        ######################################################
        ############### Generate Final report ################
        ######################################################

        # Print report header
        print('-' * 113)
        print("| {:<2} | {:<16} | {:<12}| {:<18}| {:<18}| {:<23} | {:<4} |"
              .format('Seq', 'Serial Number', 'Product', 'Battery Capacity', 'Battery Voltage', 'Bootloader Version',
                      'P/F'))
        print('-' * 113)

        idx = 1
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

        # Output total flash time
        logging.debug('Total FLASH time is {}'.format(total_time))

    except IOError:
        logging.debug('{}'.format(err.error_string))


if __name__ == "__main__":
    main()
