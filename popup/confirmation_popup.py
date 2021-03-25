from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from popup.popup_utils import dismiss_popup


def show_confirmation_popup(title, message, positive_callback, negative_callback=None):
    layout = FloatLayout()

    popup = Popup(
        title=title,
        content=layout,
        size_hint=(0.5, 0.5),
        title_align="center",
        title_size="20sp"
    )

    message_label = Label(
        text=message,
        font_size=35,
        halign="center",
        valign="top",
        text_size=(dp(350), dp(150)),
        pos_hint={'center_x': .5, 'center_y': .6}
    )
    layout.add_widget(message_label)

    cancel_button = Button(
        text="Cancel",
        size_hint=(.3, .25),
        font_size=35,
        pos_hint={'center_x': .3, 'center_y': .2}
    )
    cancel_button.bind(on_press=lambda x: dismiss_popup(negative_callback, popup))
    layout.add_widget(cancel_button)

    positive_button = Button(
        text="Yes",
        size_hint=(.3, .25),
        font_size=35,
        pos_hint={'center_x': .7, 'center_y': .2}
    )
    positive_button.bind(on_press=lambda x: dismiss_popup(positive_callback, popup))
    layout.add_widget(positive_button)

    popup.open()
