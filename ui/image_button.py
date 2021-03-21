from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button


class ImageButton(Button):
    image_source = ObjectProperty()

    def __init__(self, image_source, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.image_source = image_source


Builder.load_string("""  
<ImageButton>:
    Image:
        source: root.image_source  
        center_x: self.parent.center_x
        center_y: self.parent.center_y
""")
