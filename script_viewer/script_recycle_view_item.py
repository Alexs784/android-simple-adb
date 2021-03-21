from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button


class ScriptRecycleViewItem(Button):
    root_widget = ObjectProperty()

    def __init__(self):
        super(ScriptRecycleViewItem, self).__init__()

    def build(self, **kwargs):
        root_widget = kwargs.get("root_widget")
        self.script_id = kwargs.get("script_id")
        text = kwargs.get("text")
        return {"text": text, "font_size": "20sp", 'root_widget': root_widget, 'script_id': self.script_id}

    def on_release(self, **kwargs):
        super().on_release()
        self.root_widget.on_script_chosen(self.script_id)


KV = '''

RecycleView:
    data: []
    size_hint: 1, 0.8
    pos_hint: {'y': 0.2}
    viewclass: 'ScriptRecycleViewItem'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: dp(4)

'''


def build():
    return Builder.load_string(KV)
