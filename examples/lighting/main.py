
import os

from kivy.core.window import Window

import kivy3
from kivy.app import App
from kivy.clock import Clock
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJMTLLoader, OBJLoader
from kivy.uix.floatlayout import FloatLayout

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./blinnphong.glsl")
obj_file = os.path.join(_this_path, "./MQ-27.obj")


class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer(shader_file=shader_file)
        scene = Scene()
        camera = PerspectiveCamera(90, 1, 1, 10000)

        # loader = OBJMTLLoader()
        # obj = loader.load(obj_file, mtl_file)

        loader = OBJLoader()
        obj = loader.load(obj_file)

        self.renderer.main_light.pos = 1, 20, 50
        self.renderer.main_light.intensity = 1000

        camera.pos = 0, 0, 50
        camera.look_at((0, 0, 0))

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -0.
            obj.scale = 0.1, 0.1, 0.1

        self.renderer.render(scene, camera)
        self.orion = scene.children

        root.add_widget(self.renderer)
        self.renderer.bind(size=self._adjust_aspect)
        Clock.schedule_interval(self._rotate_obj, 1 / 20)
        # Clock.schedule_interval(self.print_color, 2)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def _rotate_obj(self, dt):
        # self.renderer.main_light.pos = 1, 20, 50
        for child in self.orion:
            child.rot.x += 2


if __name__ == '__main__':
    MainApp().run()
