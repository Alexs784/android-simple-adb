import shelve
from os import path

from kivy.uix.label import Label
from kivy.uix.popup import Popup


def android_sdk_location_is_valid(directory_path):
    directory_path = optionally_expand_user_directory(directory_path)

    if path.exists(directory_path):
        platform_tools_directory = path.join(directory_path, "platform-tools")
        adb_file = path.join(platform_tools_directory, "adb")
        return path.isfile(adb_file)
    else:
        return False


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
        adb_file = path.join(platform_tools_directory, "adb")
        return adb_file


def store_sdk_directory(sdk_location):
    location_to_check = optionally_expand_user_directory(sdk_location)
    if android_sdk_location_is_valid(location_to_check):
        with shelve.open("settings") as storage:
            storage["sdk_directory"] = location_to_check
        return True
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
