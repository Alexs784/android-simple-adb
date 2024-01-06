import os
import platform
import shelve
from os import path

from kivy.uix.label import Label
from kivy.uix.popup import Popup


def android_sdk_location_is_valid(directory_path):
    directory_path = optionally_expand_user_directory(directory_path)
    return is_valid_adb_file(directory_path)


def check_default_android_sdk_location():
    # Define default paths for different OS
    os_default_paths = {
        'Windows': 'C:\\Users\\%USERNAME%\\AppData\\Local\\Android\\Sdk\\',
        'Darwin': '/Users/$USER/Library/Android/sdk/',  # macOS
        'Linux': '/home/$USER/Android/Sdk/'
    }

    current_os = get_current_platform()
    default_android_sdk_path = os_default_paths.get(current_os)
    if default_android_sdk_path:
        # Replace placeholders with actual environment variables
        default_android_sdk_path = os.path.expandvars(default_android_sdk_path)
        if is_valid_adb_file(default_android_sdk_path):
            return store_sdk_directory(default_android_sdk_path)


def is_valid_adb_file(android_sdk_directory):
    if path.exists(android_sdk_directory):
        platform_tools_directory = path.join(android_sdk_directory, "platform-tools")
        adb_file = path.join(platform_tools_directory, "adb")
        return path.isfile(adb_file)


def optionally_expand_user_directory(directory_path):
    if directory_path.__contains__("~"):
        directory_path = path.expanduser(directory_path)
    return directory_path


def get_stored_sdk_directory():
    with shelve.open("settings") as storage:
        return storage.get("sdk_directory", "")


def get_adb():
    with shelve.open("settings") as storage:
        directory_path = storage.get("sdk_directory", "")
        platform_tools_directory = path.join(directory_path, "platform-tools")

        if get_current_platform() == 'Windows':
            adb_filename = "adb.exe"
        else:
            adb_filename = "adb"

        adb_file = path.join(platform_tools_directory, adb_filename)
        return adb_file


def trigger_store_sdk_directory(sdk_location):
    sdk_location = optionally_expand_user_directory(sdk_location)
    if android_sdk_location_is_valid(sdk_location):
        return store_sdk_directory(sdk_location)
    else:
        Popup(
            title='Error',
            content=Label(
                text="The inserted path doesn't seem to contain the Android SDK",
                font_size=30,
                halign="center",
                valign="top",
                size_hint=(.4, .4),
                pos_hint={'center_x': .5, 'center_y': 0.8}
            ),
            size_hint=(0.5, 0.5),
            title_align="center",
            title_size="20sp"
        ).open()
        return False


def store_sdk_directory(sdk_location):
    with shelve.open("settings") as storage:
        storage["sdk_directory"] = sdk_location
    return True


def get_current_platform():
    return platform.system()
