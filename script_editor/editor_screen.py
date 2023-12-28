import time
import uuid

from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, SlideTransition

from assets.asset_util import resource_path, image_buttons_width, image_buttons_height, negative_button_background, \
    positive_button_background, buttons_bottom_alignment_value, neutral_button_background
from comands.commands_utils import execute_adb_command_getting_result, execute_command_getting_result
from devices.device_manager import get_connected_devices
from popup.confirmation_popup import show_confirmation_popup
from popup.input_popup import show_input_popup
from screen_manager.screen_constants import STEP_PICKER_SCREEN, SCRIPT_LIST_VIEWER_SCREEN, STEP_VIEWER_SCREEN
from screen_manager.utils import remove_screen, get_screen_by_name
from script_editor.editor_recycle_view_item import build, EditorRecycleViewItem, ITEM_HEIGHT_DP
from step_picker.step_picker_list_screen import StepPickerListScreen
from storage.database.repository.script_repository import create_script_in_database, update_script_name, delete_script
from storage.database.repository.user_step_repository import get_grouped_user_steps_for_script, \
    get_user_steps_for_script, save_user_steps_in_database, update_user_step_position
from ui.image_button import ImageButton
from user_step_viewer.user_step_viewer_screen import UserStepViewerScreen


class ScriptEditorScreen(Screen):
    def __init__(self, script_id=None, **kwargs):
        super(ScriptEditorScreen, self).__init__(**kwargs)
        self.script_id = script_id
        self.user_steps_list_size = 0

        if script_id is None:
            created_script = create_script_in_database()
            self.script_id = created_script.id

        self.selected_device_id = None

        layout = FloatLayout()

        buttons_right_alignment_value = .85
        buttons_width = .23
        buttons_height = .13
        buttons_font_size = 45

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

        delete_script_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            background_color=negative_button_background,
            pos_hint={'center_x': .56, 'center_y': buttons_bottom_alignment_value},
            image_source=resource_path('assets/delete_button.png')
        )
        delete_script_button.bind(on_release=self.optionally_delete_script)
        layout.add_widget(delete_script_button)

        duplicate_script_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            background_color=neutral_button_background,
            pos_hint={'center_x': .68, 'center_y': buttons_bottom_alignment_value},
            image_source=resource_path('assets/duplicate_button.png')
        )
        duplicate_script_button.bind(on_release=self.on_duplicate_button_click)
        layout.add_widget(duplicate_script_button)

        self.run_script_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            background_color=positive_button_background,
            pos_hint={'center_x': .80, 'center_y': buttons_bottom_alignment_value},
            image_source=resource_path('assets/run_button.png')
        )
        self.run_script_button.bind(on_release=self.run_script)
        layout.add_widget(self.run_script_button)

        save_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            background_color=positive_button_background,
            pos_hint={'center_x': .92, 'center_y': buttons_bottom_alignment_value},
            image_source=resource_path('assets/save_button.png')
        )
        save_button.bind(on_release=self.on_save_button_click)
        layout.add_widget(save_button)

        back_button_image = resource_path('assets/back_button.png')
        back_button = ImageButton(
            size_hint=(image_buttons_width, image_buttons_height),
            pos_hint={'center_x': .08, 'center_y': buttons_bottom_alignment_value},
            image_source=back_button_image
        )
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)

        self.user_steps_list = build()
        self.update_user_steps_list()
        layout.add_widget(self.user_steps_list)

        self.add_widget(layout)

    def notify_drop_position(self, user_step_id, new_position):
        # Implement the logic to handle the drop
        item_height = int(ITEM_HEIGHT_DP)
        x_position, y_position = new_position
        new_index = int(y_position / item_height)
        reversed_index = (self.user_steps_list_size - 1) - new_index
        update_user_step_position(user_step_id, reversed_index)
        self.update_user_steps_list()

    def go_back(self, *args):
        remove_screen(self.manager, self)

    def on_save_button_click(self, *args):
        show_input_popup(self, "Script name", self.save_script)

    def on_duplicate_button_click(self, *args):
        show_input_popup(self, "New script name", self.duplicate_script)

    def show_steps_list(self, *args):
        self.manager.add_widget(StepPickerListScreen(name=STEP_PICKER_SCREEN, script_id=self.script_id))
        self.manager.transition = SlideTransition()
        self.manager.current = self.manager.next()

    def show_connected_devices(self, *args):
        dropdown_view = DropDown()

        for device_id, device_name in get_connected_devices().items():
            device = (device_id, device_name)
            device_button = Button(text=device_name, size_hint_y=None, height=80)
            device_button.bind(on_release=lambda button, selected_device=device: dropdown_view.select(selected_device))
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

    def update_user_steps_list(self):
        user_steps_for_script = get_grouped_user_steps_for_script(self.script_id)
        self.user_steps_list_size = len(user_steps_for_script)
        self.update_run_script_button_state(user_steps_for_script)
        self.user_steps_list.data = [
            EditorRecycleViewItem().build(root_widget=self, text=item.name, user_step_id=item.id,
                                          user_step_command_id=item.command_id)
            for item in user_steps_for_script
        ]

    def run_script(self, *args):
        user_steps_for_script = get_user_steps_for_script(self.script_id)
        for user_step in user_steps_for_script:
            retry_count = 0
            result = self.execute_user_step(user_step)

            while result is not None and result.returncode != 0 and retry_count < 2:
                print("Retrying command")
                time.sleep(2)
                retry_count += 1
                self.execute_user_step(user_step)

    def execute_user_step(self, user_step):
        if user_step.command.is_adb:
            result = execute_adb_command_getting_result(user_step.command.value, self.selected_device_id)
        else:
            result = execute_command_getting_result(user_step.command.value)
        print(result)
        return result

    def optionally_delete_script(self, *args):
        show_confirmation_popup(
            "Deleting script",
            "Are you sure you want to delete this script?",
            self.delete_script
        )

    def delete_script(self, *args):
        delete_script(self.script_id)
        script_viewer_screen = get_screen_by_name(self.manager, SCRIPT_LIST_VIEWER_SCREEN)
        if script_viewer_screen is not None:
            script_viewer_screen.update_scripts_list()
        self.go_back()

    def duplicate_script(self, script_name):
        new_script = create_script_in_database()
        if script_name:
            update_script_name(new_script.id, script_name)
        user_steps_for_current_script = get_user_steps_for_script(self.script_id)
        duplicated_user_steps = []
        for step in user_steps_for_current_script:
            command_id = str(uuid.uuid1())
            duplicated_step = step.duplicate(command_id, new_script.id)
            duplicated_user_steps.append(duplicated_step)
        save_user_steps_in_database(duplicated_user_steps)
        script_viewer_screen = get_screen_by_name(self.manager, SCRIPT_LIST_VIEWER_SCREEN)
        if script_viewer_screen is not None:
            script_viewer_screen.update_scripts_list()
        self.go_back()

    def save_script(self, script_name):
        update_script_name(self.script_id, script_name)
        self.go_back(self)

    def on_user_step_click(self, user_step_command_id):
        self.manager.add_widget(
            UserStepViewerScreen(name=STEP_VIEWER_SCREEN, user_step_command_id=user_step_command_id))
        self.manager.transition = SlideTransition()
        self.manager.current = self.manager.next()
