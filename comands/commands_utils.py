import subprocess

from sdk_setter.utils import get_adb


def execute_adb_command_getting_result(adb_command, device_id):
    command_to_execute = f"{get_adb()} -s {device_id} {adb_command}"
    execute_command_getting_result(command_to_execute)


def execute_command_getting_result(command):
    print("Command to execute:\n{}".format(command))
    return subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
