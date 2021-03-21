import uuid

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from assets.asset_util import resource_path
from commands.placeholder_constants import PARAMETER_PLACEHOLDER, DEVICE_SERIAL_NUMBER_PLACEHOLDER
from screen_manager.screen_constants import SCRIPT_EDITOR_SCREEN
from screen_manager.utils import remove_screen, get_screen_by_name
from step_picker.step_recycle_view_item import build, StepRecycleViewItem
from storage.database.model.command import Command
from storage.database.model.user_step import get_user_step
from storage.database.repository.step_repository import get_steps, get_step_by_id
from storage.database.repository.user_step_repository import save_user_steps_in_database
from ui.image_button import ImageButton


class SetPickerRecycleView(Screen):
    def __init__(self, script_id, device_id, **kwargs):
        super(SetPickerRecycleView, self).__init__(**kwargs)

        self.script_id = script_id
        self.device_id = device_id
        self.params_names = None
        self.params_set = []
        self.step_chosen = None

        layout = FloatLayout()
        root = build()
        root.data = [StepRecycleViewItem().build(root_widget=self, text=item.name, step_id=item.id)
                     for item in get_steps()]

        layout.add_widget(root)

        back_button_image = resource_path('assets/back_button.png')
        back_button = ImageButton(
            size_hint=(.11, .11),
            font_size=50,
            pos_hint={'center_x': .08, 'center_y': .08},
            image_source=back_button_image
        )
        back_button.bind(on_release=self.go_back)

        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, *args):
        editor_screen = get_screen_by_name(self.manager, SCRIPT_EDITOR_SCREEN)
        if editor_screen is not None:
            editor_screen.update_user_steps_list()
        remove_screen(self.manager, self)

    def on_step_chosen(self, step_id):
        self.step_chosen = get_step_by_id(step_id)
        self.params_names = self.step_chosen.parameters_names
        self.check_if_param_needs_to_be_chosen()
        print(self.step_chosen.name)

    def check_if_param_needs_to_be_chosen(self):
        if len(self.params_names) > 0:
            param_name = self.params_names.pop(0)
            self.show_pop_up_layout_for_parameter(param_name)
        else:
            self.check_if_all_params_set()

    def check_if_all_params_set(self):
        param_index = 1
        param_placeholder = PARAMETER_PLACEHOLDER + str(param_index)
        user_steps = []
        # TODO: set command_id equals for commands belinging to the same step
        command_id = uuid.uuid4().__repr__()

        for command in self.step_chosen.commands:
            command_to_save = command.value.replace(DEVICE_SERIAL_NUMBER_PLACEHOLDER, self.device_id)
            while param_placeholder in command_to_save:
                param_to_set = self.params_set.pop(0)
                command_to_save = command_to_save.replace(param_placeholder, param_to_set)
                param_index += 1
                param_placeholder = PARAMETER_PLACEHOLDER + str(param_index)

            command_to_save = Command(command_to_save, command.is_adb)
            user_step = get_user_step(self.step_chosen.name, command_to_save, command_id, self.script_id)
            user_steps.append(user_step)

        save_user_steps_in_database(user_steps)

    def show_pop_up_layout_for_parameter(self, param_name):
        layout = FloatLayout()

        popup = Popup(
            title='Add asked parameter',
            content=layout,
            size_hint=(0.5, 0.5),
            title_align="center",
            title_size="20sp"
        )

        param_name_label = Label(
            text=param_name,
            font_size=40,
            halign="center",
            valign="top",
            size_hint=(.5, .4),
            pos_hint={'center_x': .5, 'center_y': .9}

        )
        layout.add_widget(param_name_label)

        # TODO: add info toast (if present)

        param_input = TextInput(
            font_size=40,
            halign="center",
            multiline=True,
            size_hint=(.8, .4),
            padding=[10, 10, 10, 10],
            pos_hint={'center_x': .5, 'center_y': .6}
        )
        layout.add_widget(param_input)

        cancel_button = Button(
            text="Cancel",
            size_hint=(.3, .25),
            font_size=35,
            pos_hint={'center_x': .3, 'center_y': .2}
        )
        cancel_button.bind(on_press=lambda x: popup.dismiss())
        layout.add_widget(cancel_button)

        add_button = Button(
            text="Add",
            size_hint=(.3, .25),
            font_size=35,
            pos_hint={'center_x': .7, 'center_y': .2}
        )
        add_button.bind(on_press=lambda x: self.on_save_param(param_input.text, popup))
        layout.add_widget(add_button)

        popup.open()

    def on_save_param(self, param_input, popup):
        self.params_set.append(param_input)
        popup.dismiss()
        self.check_if_param_needs_to_be_chosen()
