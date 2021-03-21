import subprocess

from sdk_setter.utils import get_adb
from strings.strings_utils import remove_string_first_line


def get_connected_devices():
    result = subprocess.run([get_adb(), "devices", "-l"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    devices_info = remove_string_first_line(result)
    devices_list = {}
    for device in devices_info:
        device_id = device.split(' ', 1)[0]
        string_starting_with_device_name = device.partition('model:')[2]
        device_name = string_starting_with_device_name.split(" ", 1)[0]
        devices_list[device_id] = device_name

    print(devices_list)
    return devices_list
