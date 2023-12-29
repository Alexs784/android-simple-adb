from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from screen_manager.screen_constants import SCRIPT_EDITOR_SCREEN, SCRIPT_LIST_VIEWER_SCREEN
from screen_manager.screen_titles import SCREEN_DEFAULT_NAME
from screen_manager.utils import navigate_to_screen, get_screen_by_name
from script_editor.editor_screen import NEW_SCRIPT


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        button_height = .18

        create_script_button = Button(
            text="Create new script",
            size_hint=(.3, button_height),
            font_size=50,
            pos_hint={'center_x': .5, 'center_y': .65}
        )
        create_script_button.bind(on_release=self.show_script_editor)
        layout.add_widget(create_script_button)

        saved_scripts_button = Button(
            text="Saved scripts",
            size_hint=(.3, button_height),
            font_size=50,
            pos_hint={'center_x': .5, 'center_y': .35}
        )
        saved_scripts_button.bind(on_release=self.show_stored_scripts)
        layout.add_widget(saved_scripts_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        App.get_running_app().title = SCREEN_DEFAULT_NAME

    def show_script_editor(self, *args):
        script_editor_screen = get_screen_by_name(self.manager, SCRIPT_EDITOR_SCREEN)
        script_editor_screen.script_id = NEW_SCRIPT
        navigate_to_screen(self.manager, SCRIPT_EDITOR_SCREEN)

    def show_stored_scripts(self, *args):
        navigate_to_screen(self.manager, SCRIPT_LIST_VIEWER_SCREEN)
