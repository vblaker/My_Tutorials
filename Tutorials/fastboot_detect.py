import os
import logging
import time
import fnmatch
import threading
import subprocess
import sys
from xml.dom import minidom

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
            if result == '':
                err.set_fail('File {} not found'.format(pattern))
                logging.debug('File {} not found'.format(pattern))
            return result

        # Get the first occurrence on the returned results list

        pattern = product + '*bootloader'
        bootloader = find(pattern, filepath)[0]
        if bootloader == '':
            err.set_fail('Could not find bootloader')
            raise IOError

        pattern = product.replace('_', '') + '*loader.efi'
        efi_bootloader = find(pattern, filepath)[0]
        if efi_bootloader == '':
            err.set_fail('Could not find efi_bootloader')
            raise IOError

        pattern = product + '*.zip'
        flash_image = find(pattern, filepath)[0]
        if flash_image == '':
            err.set_fail('Could not find AOS flash image')
            raise IOError

        sequencer_xml = find('*cfg.xml', filepath)[0]
        if sequencer_xml == '':
            err.set_fail('Could not find sequencer_xml')
            raise IOError

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
        cmd = 'fastboot -s ' + fastboot_device + ' reboot'
        response = os.popen(cmd).readlines()
        if debug == 1:
            logging.debug('Rebooting {} to idle'.format(fastboot_device))

        if "Rebooting" not in response and "Finished" not in response:
            print('Device {} failed reboot to idle'.format(fastboot_device))
            err.set_fail('Device {} failed reboot to idle'.format(fastboot_device))

        # Set passing flag to be returned by the function
        err.set_pass()

    except IOError:
        err.set_fail('Device {} failed reboot to idle'.format(fastboot_device))

    return err


def fastboot_flash_efi_bootloader(fastboot_device, efi_bootloader, time_out=60, debug=0):
    err = Error()
    try:
        cmd = ["fastboot", "-s", fastboot_device, "boot", efi_bootloader]
        response = subprocess.check_output(cmd)
        if debug == 1:
            logging.debug('Flashing {} '.format(efi_bootloader))
        time.sleep(1)

        i = 0
        result = []
        while i < time_out and (fastboot_device not in result):
            err, result = get_fastboot_devices()
            time.sleep(1)
            i += 1

        if i >= time_out:
            logging.debug('Device {} EFI bootloader flash timed out, exiting...'.format(fastboot_device))
            err.set_fail('Device {} EFI bootloader flash timed out, exiting...'.format(fastboot_device))
        elif len(response) != 0:
            raise IOError('Fastboot EFI bootloader error!')
        else:
            if debug == 1:
                logging.debug('Device {} rebooted in {} seconds'.format(fastboot_device, i))
            err.set_pass()

    except IOError:
        print('Fastboot EFI bootloader error for device {}'.format(fastboot_device))
        err.set_fail('Fastboot EFI bootloader error for device {}'.format(fastboot_device))

    return err


def fastboot_flash_aos_image(fastboot_device, flash_image, debug=0):
    time_out = 120
    err = Error()
    err.set_pass()
    response = ''

    try:
        cmd = ["fastboot", "-s", fastboot_device, "update", flash_image, "--skip-reboot"]
        if debug == 1:
            logging.debug('Flashing {} image into fastboot device {}'.format(flash_image, fastboot_device))

        # Start the process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        i = 0
        status = None
        while i < time_out and status is None:
            status = process.poll()
            time.sleep(1)
            i += 1

        stdout, stderr = process.communicate()
        print('Completed device {} flash in {} seconds'.format(fastboot_device, i))
        print('Exit status {} (0 = SUCCESS)'.format(status))

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
        if debug == 1:
            logging.debug('Erasing userdata on {} device'.format(fastboot_device))

        i = 0
        result = []
        while i < time_out and ("OKAY" not in response) and (fastboot_device not in result):
            err, result = get_fastboot_devices()
            i += 1

        # Erase cache
        cmd = ["fastboot", "-s", fastboot_device, "erase", "cache"]
        response = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if debug == 1:
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


def update_worker(fastboot_device, product, debug=0):
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
    err, sequencer_list = read_sequencer_xml_file(sequencer_xml)

    try:
        i = 0
        while i < len(sequencer_list) and err.error_flag is not True:
            if sequencer_list[i] == 'fastboot_reboot_bootloader':
                if debug == 1:
                    logging.debug('Envoking fastboot_reboot_bootloader')
                err = fastboot_reboot_bootloader(fastboot_device, debug=debug)
            elif sequencer_list[i] == 'fastboot_flash_efi_bootloader':
                if debug == 1:
                    logging.debug('Envoking fastboot_flash_efi_bootloader')
                err = fastboot_flash_efi_bootloader(fastboot_device, efi_bootloader, debug=debug)
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
        logging.debug(e.args)
        logging.debug('Error message: {}'.format(err.error_string))
        logging.debug('Unexpected exception in the thread - exiting... \n{}'.format(e.args))
        exit()


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
    debug = 1
    print(sys.argv[1:])

    param_list = ['product', 'battery-voltage', 'battery-capacity', 'version-bootloader']

    try:
        # Get all connected fastboot devices
        err, devices = get_fastboot_devices(debug=debug)

        # Get fastboot device parameters before flash
        fastboot_dev_dict = get_fastboot_dev_params(devices, param_list)

        if err.error_flag is True:
            raise IOError

        print('PRE_FLASH Detected fastboot devices: {}'.format(fastboot_dev_dict))

        # Spawn a worker update thread for every connected fastboot device
        threads = []
        for device in fastboot_dev_dict:
            product = fastboot_dev_dict[device]['product'].replace(' ', '')
            t = threading.Thread(name=device, target=update_worker, args=[device, product, debug])
            threads.append(t)
            t.start()
            if debug == 1:
                logging.debug('Starting thread for serial number {}'.format(device))

        # Join threads  - determine if needed in this case
        for thread in threads:
            thread.join()

        # Get fastboot device parameters AFTER flash
        fastboot_dev_dict = get_fastboot_dev_params(devices, param_list)
        print('POST_FLASH Detected fastboot devices: {}'.format(fastboot_dev_dict))

        # Reboot to idle
        for device in devices:
            fastboot_reboot_to_idle(device, debug=debug)

    except IOError as e:
        logging.debug('{}'.format(err.error_string))


if __name__ == "__main__":
    main()

