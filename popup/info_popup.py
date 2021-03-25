from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def show_info_popup(title, message):
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
        size_hint=(.8, .4),
        pos_hint={'center_x': .5, 'center_y': .7}
    )
    layout.add_widget(message_label)

    positive_button = Button(
        text="Ok",
        size_hint=(.3, .25),
        font_size=35,
        pos_hint={'center_x': .5, 'center_y': .2}
    )
    positive_button.bind(on_release=lambda x: popup.dismiss())
    layout.add_widget(positive_button)

    popup.open()
