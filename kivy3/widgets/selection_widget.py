import os
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
import copy
from kivy3 import Renderer
_this_path = os.path.dirname(os.path.realpath(__file__))
select_mode_shader = os.path.join(_this_path, 'select_mode.glsl')

class SelectionWidget(RelativeLayout):
    def __init__(self, renderer, **kw):
        super(SelectionWidget, self).__init__()
        self.object_dict = {}
        self.renderer = renderer

    def register(self, id, widget):
        id = tuple(id)
        self.object_dict[tuple(id)] = widget
        self.add_widget(widget)

    def unregister(self, id):
        id = tuple(id)
        if id in self.object_dict.keys():
            self.remove_widget(self.object_dict[id])
            self.object_dict.pop(id)

    def get_available_id(self, reserve = True):
        """Get an Id that is unused. there is an option to reserve that address"""
        for i in range(200,256):
            for j in range(256):
                for k in range(256):
                    color_id = tuple([i, j, k])
                    if color_id not in self.object_dict.keys() and color_id != (0, 0, 0):
                        if reserve:
                            self.object_dict[color_id] = None
                        return color_id

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            widget = self.get_clicked_object(touch)
            if widget is not None:
                # print("Touched down")
                return widget.on_object_touch_down(touch)


    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            widget = self.get_clicked_object(touch)
            if widget is not None:
                return widget.on_object_touch_move(touch)


    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
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
        pos = self.parent.to_parent(touch.x,touch.y)
        color = tuple(self.renderer.fbo.get_pixel_color(pos[0]-self.parent.pos[0],pos[1]-self.parent.pos[1])[0:3])
        # print(color)
        self.renderer.fbo.shader.source = original_shader
        self.renderer.set_clear_color(original_clear_color)
        self.renderer.fbo.ask_update()
        self.renderer.fbo.draw()

        if color in self.object_dict:
            if self.object_dict[color] is not None:
                return self.object_dict[color]
        return None
