
import os
import kivy3
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy3 import Mesh, Material
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.widgets import OrbitControlWidget
from kivy3.extras.geometries import BoxGeometry, CylinderGeometry, SphereGeometry
from kivy3.loaders import OBJLoader, STLLoader
from kivy.uix.widget import Widget

from kivy.graphics import Color, Rectangle

import math


_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./blinnphong.glsl")
obj_file = os.path.join(_this_path, "./monkey.obj")
stl_file = os.path.join(_this_path, "./test.stl")


class SceneApp(App):

    def build(self):
        root = FloatLayout()

        self.renderer = Renderer(shader_file=shader_file)
        self.renderer.set_clear_color((.16, .30, .44, 1.))

        scene = Scene()
        # geometry = CylinderGeometry(0.5, 2)
        geometry = SphereGeometry(1)
        # geometry = BoxGeometry(1, 1, 1)
        material = Material(color=(0.3, 0., 0.3), diffuse=(0.3, 0.3, 0.3),
                            specular=(0.1, 0.1, 0.1))

        loader = STLLoader()
        obj = loader.load(stl_file, material)
        self.item = obj
        self.theta = 0.

        scene.add(self.item)

        self.cube = Mesh(geometry, material)
        self.item.pos.z = 0

        # self.cube.pos.z=-5
        self.camera = PerspectiveCamera(75, 0.3, 0.5, 1000)
        self.camera.pos.z = 1.5
        self.camera.look_at((0, 0, 0))
        # camera = OrthographicCamera()

        # scene.add(self.cube)
        self.camera.bind_to(self.renderer)
        self.renderer.render(scene, self.camera)

        root.add_widget(self.renderer)

        orbit = OrbitControlWidget(self.renderer, 4.)

        root.add_widget(orbit)

        Clock.schedule_interval(self._rotate_cube, 1 / 20)
        self.renderer.bind(size=self._adjust_aspect)

        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def _rotate_cube(self, dt):
        # self.cube.rotation.x += 1
        # self.cube.rotation.y += 1
        # self.cube.rotation.z += 1
        # self.item.rotation.x += 1
        # self.item.rotation.y += 1
        # self.item.rotation.z += 1
        # self.camera.look_at((0,1,0))

        # self.camera.pos.x = math.sin(self.theta) * 1.
        # self.camera.pos.z = math.cos(self.theta) * 1.

        # self.theta += 0.05

        pass
        # self.camera.update()


if __name__ == '__main__':

    from kivy.config import Config
    # Config.set('input', 'mouse', 'mouse,disable_multitouch')

    SceneApp().run()
