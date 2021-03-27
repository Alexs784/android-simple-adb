from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from assets.asset_util import resource_path, negative_button_background, image_buttons_width, image_buttons_height, \
    buttons_bottom_alignment_value
from popup.confirmation_popup import show_confirmation_popup
from screen_manager.utils import remove_screen
from storage.database.repository.user_step_repository import delete_user_steps, get_user_steps
from ui.image_button import ImageButton
from kivy.uix.label import Label


class UserStepViewerScreen(Screen):
    def __init__(self, user_step_command_id, **kwargs):
        super(UserStepViewerScreen, self).__init__(**kwargs)
        self.user_step_command_id = user_step_command_id

        layout = FloatLayout()

        steps_text = ""
        steps = get_user_steps(self.user_step_command_id)
        for step in steps:
            if step.command.is_adb:
                steps_text += "adb "
            steps_text += step.command.value + "\n\n"

        steps_label = Label(
            text=steps_text,
            font_size=40,
            halign="left",
            valign="top",
            text_size=(dp(750), dp(350)),
            pos_hint={'center_x': .5, 'center_y': .7}
        )
        layout.add_widget(steps_label)

        back_button_image = resource_path('assets/back_button.png')
        back_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            pos_hint={'center_x': .08, 'center_y': buttons_bottom_alignment_value},
            image_source=back_button_image
        )
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)

        delete_button_image = resource_path('assets/delete_button.png')
        delete_script_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            background_color=negative_button_background,
            pos_hint={'center_x': .9, 'center_y': buttons_bottom_alignment_value},
            image_source=delete_button_image
        )
        delete_script_button.bind(on_release=self.optionally_delete_user_step)
        layout.add_widget(delete_script_button)

        self.add_widget(layout)

    def go_back(self, *args):
        remove_screen(self.manager, self)

    def optionally_delete_user_step(self, *args):
        show_confirmation_popup(
            "Deleting step",
            "Are you sure you want to delete this step from the current script?",
            self.delete_script
        )

    def delete_script(self):
        print(self.user_step_command_id)
        delete_user_steps(self.user_step_command_id)
        self.go_back()
        # TODO refresh step list in editor screen
