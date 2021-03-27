from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, SlideTransition

from screen_manager.screen_constants import SCRIPT_EDITOR_SCREEN, SCRIPT_LIST_VIEWER_SCREEN
from script_editor.editor_screen import ScriptEditorScreen
from script_viewer.script_list_viewer_screen import ScriptListViewerScreen


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

    def show_script_editor(self, *args):
        self.manager.add_widget(ScriptEditorScreen(name=SCRIPT_EDITOR_SCREEN))
        self.manager.transition = SlideTransition()
        self.manager.current = self.manager.next()

    def show_stored_scripts(self, *args):
        self.manager.add_widget(ScriptListViewerScreen(name=SCRIPT_LIST_VIEWER_SCREEN))
        self.manager.transition = SlideTransition()
        self.manager.current = self.manager.next()
