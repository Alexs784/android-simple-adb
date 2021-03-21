from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from home.home_screen import HomeScreen
from sdk_setter.utils import store_sdk_directory as store_sdk
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

    def store_sdk_directory(self, *args):
        stored_successfully = store_sdk(self.sdk_location_text_input.text)
        if stored_successfully:
            self.manager.add_widget(HomeScreen(name="Home"))
            self.manager.current = self.manager.next()
