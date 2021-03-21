from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button


class EditorRecycleViewItem(Button):
    root_widget = ObjectProperty()

    def __init__(self):
        super(EditorRecycleViewItem, self).__init__()

    def build(self, **kwargs):
        root_widget = kwargs.get("root_widget")
        self.user_step_id = kwargs.get("user_step_id")
        text = kwargs.get("text")
        return {"text": text, "font_size": "20sp", 'root_widget': root_widget, 'user_step_id': self.user_step_id}

    def on_release(self, **kwargs):
        super().on_release()
        # TODO: do something on click? Offer remove option?
        # self.root_widget.on_user_step_click(self.user_step_id)


KV = '''

RecycleView:
    data: []
    size_hint: .6, .8
    pos_hint: {'x': .025, 'y': .2}
    viewclass: 'EditorRecycleViewItem'
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
