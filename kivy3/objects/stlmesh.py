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
import numpy as np
from kivy.graphics import Mesh as KivyMesh
from kivy3 import Vector3
from kivy3.core.object3d import Object3D

DEFAULT_VERTEX_FORMAT = [
    (b'v_pos', 3, 'float'),
    (b'v_normal', 3, 'float'),
    (b'v_tc0', 2, 'float')
]
DEFAULT_MESH_MODE = 'triangles'


class STLMesh(Object3D):

    def __init__(self, stl_mesh, material, **kw):
        super(STLMesh, self).__init__(**kw)
        self.geometry = stl_mesh
        self.material = material
        self.mtl = self.material  # shortcut for material property
        self.vertex_format = kw.pop('vertex_format', DEFAULT_VERTEX_FORMAT)
        self.mesh_mode = kw.pop('mesh_mode', DEFAULT_MESH_MODE)
        self.create_mesh()

    def create_mesh(self):
        """ Create real mesh object from the geometry and material """
        max = 65535
        indices = list(range(0, len(self.geometry.v0) * 3))[0:max]

        v0 = self.geometry.v0.astype(np.float32)[0:max]
        v1 = self.geometry.v1.astype(np.float32)[0:max]
        v2 = self.geometry.v2.astype(np.float32)[0:max]
        normals = self.geometry.normals.astype(np.float32)[0:max]
        uvs = np.zeros((len(v0), 2)).astype(np.float32)[0:max]
        vertices = np.block([v0, normals, uvs, v1, normals, uvs, v2, normals, uvs]).flatten()

        kw = dict(
            vertices=vertices,
            indices=indices,
            fmt=self.vertex_format,
            mode=self.mesh_mode
        )
        if self.material.map:
            kw['texture'] = self.material.map
        self._mesh = KivyMesh(**kw)

    def custom_instructions(self):
        yield self.material
        yield self._mesh
