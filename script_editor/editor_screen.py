from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.textinput import TextInput

from commands.commands_utils import execute_adb_command_getting_result, execute_command_getting_result
from devices.device_manager import get_connected_devices
from screen_manager.screen_constants import STEP_PICKER_SCREEN
from screen_manager.utils import remove_screen
from script_editor.editor_recycle_view_item import build, EditorRecycleViewItem
from step_picker.step_picker_list import SetPickerRecycleView
from storage.database.repository.script_repository import create_script_in_database, update_script_name
from storage.database.repository.user_step_repository import get_user_steps_for_script
from ui.image_button import ImageButton


class ScriptEditorScreen(Screen):
    def __init__(self, script_id=None, **kwargs):
        super(ScriptEditorScreen, self).__init__(**kwargs)
        self.script_id = script_id

        if script_id is None:
            created_script = create_script_in_database()
            self.script_id = created_script.id

        self.selected_device_id = None

        layout = FloatLayout()

        buttons_right_alignment_value = .85
        buttons_bottom_alignment_value = .08
        buttons_width = .23
        buttons_height = .13
        buttons_font_size = 45
        image_buttons_width = .11
        image_buttons_height = .11
        positive_button_background = (0.38, 1.70, 0.38, 1)

        self.add_step_button = Button(
            text="Add step",
            size_hint=(buttons_width, buttons_height),
            font_size=buttons_font_size,
            pos_hint={'center_x': buttons_right_alignment_value, 'center_y': .9}
        )
        self.add_step_button.bind(on_release=self.show_steps_list)
        layout.add_widget(self.add_step_button)

        self.select_device_button = Button(
            text="Select device",
            size_hint=(buttons_width, buttons_height),
            font_size=buttons_font_size,
            pos_hint={'center_x': buttons_right_alignment_value, 'center_y': .75}
        )
        self.select_device_button.bind(on_release=self.show_connected_devices)
        self.update_add_step_button_state()
        layout.add_widget(self.select_device_button)

        self.run_script_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            background_color=positive_button_background,
            pos_hint={'center_x': .80, 'center_y': buttons_bottom_alignment_value},
            image_source="assets/run_button.png"
        )
        self.run_script_button.bind(on_release=self.run_script)
        layout.add_widget(self.run_script_button)

        save_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            background_color=positive_button_background,
            pos_hint={'center_x': .92, 'center_y': buttons_bottom_alignment_value},
            image_source="assets/save_button.png"
        )
        save_button.bind(on_release=self.on_save_button_click)
        layout.add_widget(save_button)

        back_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            pos_hint={'center_x': .08, 'center_y': buttons_bottom_alignment_value},
            image_source="assets/back_button.png"
        )
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)

        self.user_steps_list = build()
        self.update_user_steps_list()
        layout.add_widget(self.user_steps_list)

        self.add_widget(layout)

    def go_back(self, *args):
        remove_screen(self.manager, self)

    def on_save_button_click(self, *args):
        self.show_save_script_pop_up()

    def show_steps_list(self, *args):
        self.manager.add_widget(
            SetPickerRecycleView(name=STEP_PICKER_SCREEN, script_id=self.script_id, device_id=self.selected_device_id))
        self.manager.transition = SlideTransition()
        self.manager.current = self.manager.next()

    def show_connected_devices(self, *args):
        dropdown_view = DropDown()

        for device_id, device_name in get_connected_devices().items():
            device = (device_id, device_name)
            device_button = Button(text=device_name, size_hint_y=None, height=80)
            device_button.bind(on_release=lambda button: dropdown_view.select(device))
            dropdown_view.add_widget(device_button)

        dropdown_view.bind(on_select=lambda instance, device_data: self.on_device_selected(device_data))

        dropdown_view.open(self.select_device_button)

    def on_device_selected(self, *args):
        self.select_device_button.text = args[0][1]
        self.selected_device_id = args[0][0]
        self.update_add_step_button_state()

    def update_add_step_button_state(self):
        self.add_step_button.set_disabled(self.selected_device_id is None)

    def update_run_script_button_state(self, user_steps_for_script):
        disable = len(user_steps_for_script) == 0
        self.run_script_button.set_disabled(disable)

    def get_user_steps_for_this_script(self):
        return get_user_steps_for_script(self.script_id)

    def update_user_steps_list(self):
        user_steps_for_script = self.get_user_steps_for_this_script()
        self.update_run_script_button_state(user_steps_for_script)
        self.user_steps_list.data = [EditorRecycleViewItem().build(root_widget=self, text=item.name, step_id=item.id)
                                     for item in user_steps_for_script]

    def run_script(self, *args):
        user_steps_for_script = self.get_user_steps_for_this_script()
        for user_step in user_steps_for_script:
            if user_step.command.is_adb:
                result = execute_adb_command_getting_result(user_step.command.value)
            else:
                result = execute_command_getting_result(user_step.command.value)

            print(result)

    def show_save_script_pop_up(self):
        layout = FloatLayout()

        popup = Popup(
            title='Script name',
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
        cancel_button.bind(on_press=lambda x: popup.dismiss())
        layout.add_widget(cancel_button)

        save_button = Button(
            text="Save",
            size_hint=(.3, .25),
            font_size=35,
            pos_hint={'center_x': .7, 'center_y': .2}
        )
        save_button.bind(on_press=lambda x: self.save_script(script_name_input.text, popup))
        layout.add_widget(save_button)

        popup.open()

    def save_script(self, script_name, popup):
        update_script_name(self.script_id, script_name)
        popup.dismiss()
        self.go_back(self)
