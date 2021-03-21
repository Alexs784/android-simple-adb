from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button


class StepRecycleViewItem(Button):
    root_widget = ObjectProperty()

    def __init__(self):
        super(StepRecycleViewItem, self).__init__()

    def build(self, **kwargs):
        root_widget = kwargs.get("root_widget")
        self.step_id = kwargs.get("step_id")
        text = kwargs.get("text")
        return {"text": text, "font_size": "20sp", 'root_widget': root_widget, 'step_id': self.step_id}

    def on_release(self, **kwargs):
        super().on_release()
        self.root_widget.on_step_chosen(self.step_id)


KV = '''

RecycleView:
    data: []
    size_hint: 1, 0.8
    pos_hint: {'y': 0.2}
    viewclass: 'StepRecycleViewItem'
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
