"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

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

from kivy.graphics import Mesh as KivyMesh
from kivy3 import Object3D, Mesh, Material, Vector2

import numpy as np

DEFAULT_VERTEX_FORMAT = [
    (b'v_pos', 3, 'float'),
    (b'v_normal', 3, 'float'),
    (b'v_tc0', 2, 'float')
]
DEFAULT_MESH_MODE = 'triangles'


class STLMesh(Object3D):
    def __init__(self, v0, v1, v2, normals, material, **kw):
        super(STLMesh, self).__init__(**kw)
        self.vertex_format = kw.pop('vertex_format', DEFAULT_VERTEX_FORMAT)
        self.mesh_mode = kw.pop('mesh_mode', DEFAULT_MESH_MODE)
        self.material = material
        self.normals = normals
        indices = list(range(0, len(v0)*3))
        uvs = np.zeros((len(v0), 2)).astype(np.float32)
        vertices = list(np.block([v0.astype(np.float32),normals.astype(np.float32),uvs,v1.astype(np.float32),normals.astype(np.float32),uvs,v2.astype(np.float32),normals.astype(np.float32),uvs]).flatten())
        kw2=dict(vertices=vertices,
                indices=indices,
                fmt=self.vertex_format,
                mode=self.mesh_mode)

        # if self.material.map:
        #     kw2['texture'] = self.material.map
        self._mesh = KivyMesh(**kw2)

    def custom_instructions(self):
        yield self.material
        yield self._mesh

    def set_material(self, mat):
        idx = 0
        for instr in self._instructions.children:
            if instr.__class__.__name__ == "Material":
                self._instructions.children[idx] = mat
                return
            idx += 1

    def get_material(self):
        idx = 0
        for instr in self._instructions.children:
            if instr.__class__.__name__ == "Material":
                return self._instructions.children[idx]
            idx += 1
