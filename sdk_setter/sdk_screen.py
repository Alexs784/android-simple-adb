from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from screen_manager.screen_constants import HOME_SCREEN
from screen_manager.utils import navigate_to_screen
from sdk_setter.utils import trigger_store_sdk_directory, check_default_android_sdk_location
from sdk_setter.utils import get_stored_sdk_directory


class SdkScreen(Screen):
    def __init__(self, **kwargs):
        super(SdkScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        sdk_label = Label(
            text="Where is your Android SDK located?",
            size_hint=(.3, .1),
            font_size=50,
            pos_hint={'center_x': .5, 'center_y': .7}
        )
        layout.add_widget(sdk_label)

        self.sdk_location_text_input = TextInput(
            text=get_stored_sdk_directory(),
            size_hint=(.7, .08),
            font_size=50,
            halign='center',
            multiline=False,
            padding=[3, 3, 3, 3],
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        layout.add_widget(self.sdk_location_text_input)

        save_sdk_button = Button(
            text="Save",
            size_hint=(.3, .1),
            font_size=50,
            pos_hint={'center_x': .5, 'center_y': .3}
        )
        layout.add_widget(save_sdk_button)
        save_sdk_button.bind(on_press=self.store_sdk_directory)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        if check_default_android_sdk_location():
            navigate_to_screen(self.manager, HOME_SCREEN)

    def store_sdk_directory(self, *args):
        stored_successfully = trigger_store_sdk_directory(self.sdk_location_text_input.text)
        if stored_successfully:
            navigate_to_screen(self.manager, HOME_SCREEN)
