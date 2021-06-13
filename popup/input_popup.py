from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from popup.popup_utils import dismiss_popup


def show_input_popup(self, title, positive_callback, negative_callback=None):
    layout = FloatLayout()

    popup = Popup(
        title=title,
        content=layout,
        size_hint=(0.5, 0.5),
        title_align="center",
        title_size="20sp"
    )

    script_name_input = TextInput(
        font_size=40,
        halign="center",
        multiline=True,
        size_hint=(.8, .4),
        padding=[10, 10, 10, 10],
        pos_hint={'center_x': .5, 'center_y': .7}
    )
    layout.add_widget(script_name_input)

    cancel_button = Button(
        text="Cancel",
        size_hint=(.3, .25),
        font_size=35,
        pos_hint={'center_x': .3, 'center_y': .2}
    )
    cancel_button.bind(on_press=lambda x: dismiss_popup(negative_callback, popup))
    layout.add_widget(cancel_button)

    save_button = Button(
        text="Save",
        size_hint=(.3, .25),
        font_size=35,
        pos_hint={'center_x': .7, 'center_y': .2}
    )
    save_button.bind(on_press=lambda x: dismiss_popup(positive_callback(script_name_input.text), popup))
    layout.add_widget(save_button)

    popup.open()
