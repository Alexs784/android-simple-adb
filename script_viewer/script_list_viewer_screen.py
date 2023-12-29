from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from assets.asset_util import resource_path
from screen_manager.screen_constants import SCRIPT_EDITOR_SCREEN
from screen_manager.utils import navigate_to_screen, go_back
from script_viewer.script_recycle_view_item import build, ScriptRecycleViewItem
from storage.database.repository.script_repository import get_scripts
from ui.image_button import ImageButton


class ScriptListViewerScreen(Screen):
    def __init__(self, **kwargs):
        super(ScriptListViewerScreen, self).__init__(**kwargs)

        layout = FloatLayout()
        self.root = build()

        layout.add_widget(self.root)

        back_button_image = resource_path('assets/back_button.png')
        back_button = ImageButton(
            size_hint=(.11, .11),
            pos_hint={'center_x': .08, 'center_y': .08},
            image_source=back_button_image
        )
        back_button.bind(on_press=self.go_back)

        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self, *args):
        self.update_scripts_list()

    def go_back(self, *args):
        go_back(self.manager)

    def on_script_chosen(self, script_id):
        script_editor_screen = self.manager.get_screen(SCRIPT_EDITOR_SCREEN)
        script_editor_screen.script_id = script_id
        navigate_to_screen(self.manager, SCRIPT_EDITOR_SCREEN)

    def update_scripts_list(self):
        self.root.data = self.load_stored_scripts()

    def load_stored_scripts(self):
        list_items = []
        scripts = get_scripts()
        for script in scripts:
            list_items.append(ScriptRecycleViewItem().build(root_widget=self, script_id=script.id, text=script.name))
        return list_items
