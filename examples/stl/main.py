"""
The MIT License (MIT)

Copyright (c) 2014 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
from kivy.app import App
from kivy3 import Scene, Renderer, PerspectiveCamera, Material, Mesh
from kivy3.extras.stlgeometry import STLGeometry
from kivy3.loaders import OBJLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from stl import mesh

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
# shader_file = os.path.join(_this_path, "./simple.glsl")
# obj_file = os.path.join(_this_path, "./monkey.obj")

stl_file = "D:/TheBlueprintLab/Projects/ReachControl/kivy3_repo/examples/urdf/RS2-1021-segmented-def-urdf/meshes/base_link.STL"


class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer()
        scene = Scene()
        # load stl file
        mesh_a = mesh.Mesh.from_file(stl_file)
        geo = STLGeometry(mesh_a)
        material = Material(color=(0., 0., 1.), diffuse=(0., 0., 0.1),
                            specular=(.1, .1, .1))
        obj = Mesh(geo, material)

        # obj.position.z = 10
        self.my_obj = obj

        # load obj file
        # loader = OBJLoader()
        # obj = loader.load(obj_file)
        # self.monkey = obj.children[0]
        #
        scene.add(obj)
        camera = PerspectiveCamera(15, 1, 1, 1000)

        self.renderer.render(scene, camera)
        root.add_widget(self.renderer)
        Clock.schedule_interval(self._update_obj, 1. / 20)
        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _update_obj(self, dt):
        obj = self.my_obj
        if obj.pos.z > -2:
            obj.pos.z -= 0.5
        else:
            obj.rotation.y += 1
            obj.rotation.x += 0.5

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == '__main__':
    MainApp().run()
