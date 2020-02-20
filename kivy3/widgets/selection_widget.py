import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.uix.widget import Widget
import copy
from kivy3 import Renderer
_this_path = os.path.dirname(os.path.realpath(__file__))
select_mode_shader = os.path.join(_this_path, 'select_mode.glsl')

class SelectionWidget(Widget):
    def __init__(self, renderer, **kw):
        super(SelectionWidget, self).__init__()
        self.object_dict = {}
        self.renderer = renderer

    def register(self, id, widget):
        tuple(id)
        self.object_dict[tuple(id)] = widget

    def on_touch_down(self, touch):
        widget = self.get_clicked_object(touch)
        if widget is not None:
            return widget.on_object_touch_down(touch)

    def on_touch_move(self, touch):
        widget = self.get_clicked_object(touch)
        if widget is not None:
            return widget.on_object_touch_move(touch)

    def on_touch_up(self, touch):
        widget = self.get_clicked_object(touch)
        if widget is not None:
            return widget.on_object_touch_up(touch)

    def get_clicked_object(self, touch):

        original_shader = self.renderer.fbo.shader.source
        original_clear_color = self.renderer.fbo.clear_color
        self.renderer.fbo.shader.source = select_mode_shader
        self.renderer.set_clear_color((0., 0., 0., 0.))
        self.renderer.fbo.ask_update()
        self.renderer.fbo.draw()
        color = tuple(self.renderer.fbo.get_pixel_color(touch.x, touch.y)[0:3])

        self.renderer.fbo.shader.source = original_shader
        self.renderer.set_clear_color(original_clear_color)
        self.renderer.fbo.ask_update()
        self.renderer.fbo.draw()

        if color in self.object_dict:
            return self.object_dict[color]
        else:
            return None
