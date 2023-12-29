from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from home.home_screen import HomeScreen
from screen_manager.screen_constants import SDK_SCREEN, HOME_SCREEN, SCRIPT_LIST_VIEWER_SCREEN, SCRIPT_EDITOR_SCREEN, \
    STEP_PICKER_SCREEN, STEP_VIEWER_SCREEN
from screen_manager.utils import navigate_to_screen
from script_editor.editor_screen import ScriptEditorScreen
from script_viewer.script_list_viewer_screen import ScriptListViewerScreen
from sdk_setter.sdk_screen import SdkScreen
from sdk_setter.utils import get_stored_sdk_directory, android_sdk_location_is_valid
from step_picker.step_picker_list_screen import StepPickerListScreen
from user_step_viewer.user_step_viewer_screen import UserStepViewerScreen


def should_ask_for_android_sdk_location():
    stored_sdk_location = get_stored_sdk_directory()
    return not android_sdk_location_is_valid(stored_sdk_location) or stored_sdk_location.__contains__('~')


class ScreenManagerApp(App):

    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(HomeScreen(name=HOME_SCREEN))
        screen_manager.add_widget(ScriptListViewerScreen(name=SCRIPT_LIST_VIEWER_SCREEN))
        screen_manager.add_widget(ScriptEditorScreen(name=SCRIPT_EDITOR_SCREEN))
        screen_manager.add_widget(StepPickerListScreen(name=STEP_PICKER_SCREEN))
        screen_manager.add_widget(UserStepViewerScreen(name=STEP_VIEWER_SCREEN))

        if should_ask_for_android_sdk_location():
            screen_manager.add_widget(SdkScreen(name=SDK_SCREEN))
            navigate_to_screen(screen_manager, SDK_SCREEN)
        else:
            navigate_to_screen(screen_manager, HOME_SCREEN)

        screen_manager.transition = SlideTransition()

        self.title = "Android automation"

        return screen_manager
