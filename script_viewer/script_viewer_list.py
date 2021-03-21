from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, SlideTransition

from assets.asset_util import resource_path
from screen_manager.screen_constants import SCRIPT_EDITOR_SCREEN
from screen_manager.utils import remove_screen
from script_editor.editor_screen import ScriptEditorScreen
from script_viewer.script_recycle_view_item import build, ScriptRecycleViewItem
from storage.database.repository.script_repository import get_scripts
from ui.image_button import ImageButton


class ScriptViewRecycleView(Screen):
    def __init__(self, **kwargs):
        super(ScriptViewRecycleView, self).__init__(**kwargs)

        layout = FloatLayout()
        root = build()
        root.data = self.load_stored_scripts()

        layout.add_widget(root)

        back_button_image = resource_path('assets/back_button.png')
        back_button = ImageButton(
            size_hint=(.11, .11),
            pos_hint={'center_x': .08, 'center_y': .08},
            image_source=back_button_image
        )
        back_button.bind(on_press=self.go_back)

        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, *args):
        remove_screen(self.manager, self)

    def load_stored_scripts(self):
        list_items = []
        scripts = get_scripts()
        for script in scripts:
            list_items.append(ScriptRecycleViewItem().build(root_widget=self, script_id=script.id, text=script.name))
        return list_items

    def on_script_chosen(self, script_id):
        self.manager.add_widget(ScriptEditorScreen(name=SCRIPT_EDITOR_SCREEN, script_id=script_id))
        self.manager.transition = SlideTransition()
        self.manager.current = self.manager.next()
