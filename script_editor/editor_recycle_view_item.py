from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button

ITEM_HEIGHT_DP = dp(56)
ITEM_SPACING_DP = dp(4)
OPACITY_ANIMATION_DURATION=0.3


class EditorRecycleViewItem(DragBehavior, Button):
    root_widget = ObjectProperty()

    def __init__(self, **kwargs):
        super(EditorRecycleViewItem, self).__init__(**kwargs)
        self._drag_schedule = None
        self.shadow = None
        self.elevation = None
        self.user_step_id = None
        self.user_step_command_id = None
        self.drag_timeout = 10000000
        self.drag_distance = 0

    def build(self, **kwargs):
        root_widget = kwargs.get("root_widget")
        self.drag_rectangle = [root_widget.x, root_widget.y, root_widget.width, root_widget.height]
        self.user_step_id = kwargs.get("user_step_id")
        self.user_step_command_id = kwargs.get("user_step_command_id")
        text = kwargs.get("text")
        return {
            "text": text,
            "font_size": "20sp",
            'root_widget': root_widget,
            'user_step_id': self.user_step_id,
            'user_step_command_id': self.user_step_command_id
        }

    def on_click(self, **kwargs):
        super().on_release()
        self.root_widget.on_user_step_click(self.user_step_command_id)

    def on_drag_start(self):
        self._drag_schedule = None
        self.shadow = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        self.elevation = 10
        with self.canvas:
            Color(0, 0, 0, .4)
            self.shadow = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])

        # Smooth transition to semi-transparent
        Animation(opacity=0.7, d=OPACITY_ANIMATION_DURATION).start(self)
        # Lift the item slightly to indicate it's being picked up
        Animation(y=self.y + 10, t='out_quad', d=0.2).start(self)

    def on_drag_finish(self, new_position):
        self.shadow = None
        self.elevation = 0
        Animation(opacity=1, d=OPACITY_ANIMATION_DURATION).start(self)
        new_x, new_y = new_position
        self.x = 0
        self.y = new_y

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            # Schedule the start of the drag after a delay
            self._drag_schedule = Clock.schedule_once(lambda dt: self.on_drag_start(), 0)
            return True
        return super(EditorRecycleViewItem, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # Update the position of the item to follow the touch
            self.y = touch.y - self.height / 2
            return True
        return super(EditorRecycleViewItem, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if self._drag_schedule:
                # If the touch is released before the delay, cancel the scheduled drag and handle it as a click
                self._drag_schedule.cancel()
                self._drag_schedule = None
                self.on_click()
            else:
                # Calculate the new position based on the touch up position
                new_position = self.parent.to_local(*touch.pos)
                self.root_widget.notify_drop_position(self.user_step_id, new_position)
                self.on_drag_finish(new_position)
            return True
        return super(EditorRecycleViewItem, self).on_touch_up(touch)


KV = f'''

RecycleView:
    data: []
    size_hint: .6, .8
    pos_hint: {{'x': .025, 'y': .2}}
    viewclass: 'EditorRecycleViewItem'
    RecycleBoxLayout:
        default_size: None, {ITEM_HEIGHT_DP}
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: {ITEM_SPACING_DP}

'''


def build():
    return Builder.load_string(KV)
