from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from home.home_screen import HomeScreen
from screen_manager.screen_constants import SDK_SCREEN, HOME_SCREEN
from sdk_setter.sdk_screen import SdkScreen
from sdk_setter.utils import get_stored_sdk_directory, android_sdk_location_is_valid


def should_ask_for_android_sdk_location():
    stored_sdk_location = get_stored_sdk_directory()
    return not android_sdk_location_is_valid(stored_sdk_location) or stored_sdk_location.__contains__('~')


class ScreenManagerApp(App):

    def build(self):
        root = ScreenManager()

        self.title = "Android automation"

        if should_ask_for_android_sdk_location():
            root.add_widget(SdkScreen(name=SDK_SCREEN))
        else:
            root.add_widget(HomeScreen(name=HOME_SCREEN))

        return root
